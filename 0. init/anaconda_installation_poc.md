### Anaconda installation on Ubuntu

- Anaconda docs: [Installing Anaconda Distribution — macOS/Linux](https://www.anaconda.com/docs/getting-started/anaconda/install#macos-linux-installation:how-do-i-verify-my-installers-integrity)
- DigitalOcean tutorial: [How to Install the Anaconda Python Distribution on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-22-04)
- Archive used for download and SHA-256 verification: [Anaconda archive](https://repo.anaconda.com/archive/)

---

### Steps performed (Ubuntu 22.04/24.04)

1) Download the Linux x86_64 installer from Anaconda official page

2) Verify the installer SHA-256 checksum

```bash
sha256sum ~/Downloads/Anaconda3-2025.06-0-Linux-x86_64.sh
# Manually compare with the SHA256 listed on https://repo.anaconda.com/archive/
```

3) Run the installer

```bash
bash ~/Downloads/Anaconda3-2025.06-0-Linux-x86_64.sh
```

4) Initialize shell and validate

```bash
source ~/.bashrc
conda --version
which conda
```       
