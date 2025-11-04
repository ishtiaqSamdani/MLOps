#!/usr/bin/env bash
set -euo pipefail

# Repo root (directory of this script)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

CONFIG_FILE="$REPO_DIR/.git-remotes.env"

die() { echo "[ERROR] $*" >&2; exit 1; }
info() { echo "[INFO]  $*" >&2; }
warn() { echo "[WARN]  $*" >&2; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

require_tools() {
  command_exists git || die "git not found. Install git."
  command_exists ssh || die "ssh not found. Install OpenSSH client."
}

# Load configuration
load_config() {
  if [[ ! -f "$CONFIG_FILE" ]]; then
    cat > "$CONFIG_FILE" <<'EOF'
# Fill these and re-run ./git.sh setup

# Remote URLs (SSH). Leave as-is if already correct.
GITHUB_SSH_URL="git@github.com:ishtiaqSamdani/MLOps.git"
GITLAB_SSH_URL="git@git.z-apps.io:nurture/user/IshtiaqSamdani/de-ml-learning.git"

# Identity to use when working under each provider in THIS repo
GITHUB_USER="Your GitHub Name"
GITHUB_EMAIL="you@github-email.example"
GITLAB_USER="Your GitLab Name"
GITLAB_EMAIL="you@gitlab-email.example"

# SSH key paths and host aliases (can keep defaults)
GITHUB_SSH_KEY="$HOME/.ssh/github_ishmart_ishtiaq_gmail"
GITLAB_SSH_KEY="$HOME/.ssh/gitlab"

# SSH Host aliases used by this script (do not need to be real domains)
GITHUB_SSH_HOST_ALIAS="github-mlops"
GITLAB_SSH_HOST_ALIAS="gitlab-mlops"

# Canonical hostnames (not the alias). GitLab here is self-hosted
GITHUB_HOSTNAME="github.com"
GITLAB_HOSTNAME="git.z-apps.io"
EOF
    warn "Created $CONFIG_FILE. Please review and adjust as needed."
  fi
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
}

normalize_provider() {
  local p="${1:-}"
  case "$p" in
    gh|github|GitHub) echo "github" ;;
    gl|gitlab|GitLab) echo "gitlab" ;;
    *) echo "" ;;
  esac
}

ensure_ssh_alias() {
  local alias_name="$1"      # e.g., github-mlops
  local host_name="$2"       # e.g., github.com or git.z-apps.io
  local identity_file="$3"   # e.g., ~/.ssh/github_...

  mkdir -p "$HOME/.ssh"
  chmod 700 "$HOME/.ssh"
  local cfg="$HOME/.ssh/config"
  touch "$cfg"
  chmod 600 "$cfg"

  # If an exact Host block already exists, do nothing
  if grep -Eiq "^Host[[:space:]]+$alias_name(\b|$)" "$cfg"; then
    info "SSH alias '$alias_name' already present in $cfg"
    return 0
  fi

  {
    echo ""
    echo "Host $alias_name"
    echo "  HostName $host_name"
    echo "  User git"
    echo "  IdentityFile $identity_file"
    echo "  IdentitiesOnly yes"
  } >> "$cfg"

  info "Added SSH alias '$alias_name' -> $host_name using key $identity_file"
}

url_with_alias() {
  local original_url="$1"   # git@host:path.git
  local alias_name="$2"     # github-mlops
  # Replace host part between 'git@' and ':' with alias_name
  echo "$original_url" | sed -E "s#^git@[^:]+:#git@${alias_name}:#"
}

ensure_remote() {
  local provider="$1" # github|gitlab
  local remote_name="$provider"
  local url=""
  local aliased_url=""

  if [[ "$provider" == "github" ]]; then
    url="${GITHUB_SSH_URL:?GITHUB_SSH_URL not set in $CONFIG_FILE}"
    aliased_url="$(url_with_alias "$url" "$GITHUB_SSH_HOST_ALIAS")"
  elif [[ "$provider" == "gitlab" ]]; then
    url="${GITLAB_SSH_URL:?GITLAB_SSH_URL not set in $CONFIG_FILE}"
    aliased_url="$(url_with_alias "$url" "$GITLAB_SSH_HOST_ALIAS")"
  else
    die "Unknown provider '$provider'"
  fi

  if git remote get-url "$remote_name" >/dev/null 2>&1; then
    git remote set-url "$remote_name" "$aliased_url"
    info "Updated remote '$remote_name' -> $aliased_url"
  else
    git remote add "$remote_name" "$aliased_url"
    info "Added remote '$remote_name' -> $aliased_url"
  fi
}

set_identity() {
  local provider="$1"
  if [[ "$provider" == "github" ]]; then
    git config user.name  "${GITHUB_USER}"
    git config user.email "${GITHUB_EMAIL}"
    info "Set identity to GitHub: $GITHUB_USER <$GITHUB_EMAIL>"
  elif [[ "$provider" == "gitlab" ]]; then
    git config user.name  "${GITLAB_USER}"
    git config user.email "${GITLAB_EMAIL}"
    info "Set identity to GitLab: $GITLAB_USER <$GITLAB_EMAIL>"
  else
    die "Unknown provider '$provider'"
  fi
}

test_ssh() {
  local provider="$1"
  local alias_name
  if [[ "$provider" == "github" ]]; then
    alias_name="$GITHUB_SSH_HOST_ALIAS"
  else
    alias_name="$GITLAB_SSH_HOST_ALIAS"
  fi
  set +e
  ssh -T -o StrictHostKeyChecking=accept-new "git@${alias_name}" >/dev/null 2>&1
  local rc=$?
  set -e
  if [[ $rc -eq 1 || $rc -eq 255 || $rc -eq 5 || $rc -eq 0 ]]; then
    # GitHub/GitLab typically return 1 after greeting; any connection-level failure would be different
    info "SSH check for '$provider' alias '$alias_name' executed (rc=$rc)."
  else
    warn "SSH check for '$provider' alias '$alias_name' returned rc=$rc."
  fi
}

ensure_setup() {
  local provider="$1"
  if [[ "$provider" == "github" ]]; then
    ensure_ssh_alias "$GITHUB_SSH_HOST_ALIAS" "$GITHUB_HOSTNAME" "$GITHUB_SSH_KEY"
    ensure_remote github
  elif [[ "$provider" == "gitlab" ]]; then
    ensure_ssh_alias "$GITLAB_SSH_HOST_ALIAS" "$GITLAB_HOSTNAME" "$GITLAB_SSH_KEY"
    ensure_remote gitlab
  elif [[ "$provider" == "both" ]]; then
    ensure_ssh_alias "$GITHUB_SSH_HOST_ALIAS" "$GITHUB_HOSTNAME" "$GITHUB_SSH_KEY"
    ensure_remote github
    ensure_ssh_alias "$GITLAB_SSH_HOST_ALIAS" "$GITLAB_HOSTNAME" "$GITLAB_SSH_KEY"
    ensure_remote gitlab
  else
    die "Unknown provider for setup: '$provider'"
  fi
}

current_branch() {
  git symbolic-ref --quiet --short HEAD || git rev-parse --short HEAD
}

ensure_upstream_if_missing() {
  local remote="$1"
  local branch="$2"
  if ! git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
    info "No upstream set. Using -u $remote $branch"
    echo "-u"
  fi
}

cmd_push() {
  local provider="$1"; shift || true
  local branch="${1:-$(current_branch)}"
  ensure_setup "$provider"
  local upstream_flag
  upstream_flag="$(ensure_upstream_if_missing "$provider" "$branch" || true)"
  git push ${upstream_flag:-} "$provider" "$branch"
  info "Pushed branch '$branch' to '$provider'"
}

cmd_pull() {
  local provider="$1"; shift || true
  local branch="${1:-$(current_branch)}"
  ensure_setup "$provider"
  git pull "$provider" "$branch"
  info "Pulled branch '$branch' from '$provider'"
}

cmd_checkout_with_provider() {
  local provider="$1"; shift || true
  set_identity "$provider"
  git checkout "$@"
}

cmd_setup() {
  local target="${1:-both}"
  ensure_setup "$target"
  test_ssh github || true
  test_ssh gitlab || true
  info "Setup finished for: $target"
}

print_usage() {
  cat <<USAGE
Usage:
  ./git.sh setup [github|gitlab|both]
  ./git.sh push github <branch>
  ./git.sh push gitlab <branch>
  ./git.sh pull github <branch>
  ./git.sh pull gitlab <branch>
  ./git.sh github checkout [-b] <branch-name>
  ./git.sh gitlab checkout [-b] <branch-name>
  ./git.sh identity <github|gitlab>

Notes:
  - Configure values in .git-remotes.env first if needed.
  - The checkout form with provider sets commit identity for this repo.
USAGE
}

main() {
  require_tools
  load_config

  if [[ $# -lt 1 ]]; then
    print_usage; exit 1
  fi

  local a1="${1:-}"; shift || true

  case "$a1" in
    setup)
      cmd_setup "${1:-both}"
      ;;
    push)
      local provider="$(normalize_provider "${1:-}")"; shift || true
      [[ -n "$provider" ]] || die "Provider required: github|gitlab"
      cmd_push "$provider" "${1:-}"
      ;;
    pull)
      local provider2="$(normalize_provider "${1:-}")"; shift || true
      [[ -n "$provider2" ]] || die "Provider required: github|gitlab"
      cmd_pull "$provider2" "${1:-}"
      ;;
    identity)
      local provider3="$(normalize_provider "${1:-}")"; shift || true
      [[ -n "$provider3" ]] || die "Provider required: github|gitlab"
      set_identity "$provider3"
      ;;
    github|gitlab|gh|gl)
      local provider4="$(normalize_provider "$a1")"
      local subcmd="${1:-}"; shift || true
      case "$subcmd" in
        checkout)
          [[ $# -ge 1 ]] || die "checkout needs args, e.g. -b new-branch or branch-name"
          cmd_checkout_with_provider "$provider4" "$@"
          ;;
        *)
          die "Unknown subcommand '$subcmd' for provider-first form"
          ;;
      esac
      ;;
    *)
      print_usage; exit 1
      ;;
  esac
}

main "$@"


