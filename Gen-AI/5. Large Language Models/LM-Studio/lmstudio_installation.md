# LM Studio AppImage Installation Guide for Linux


## Prerequisites

LM Studio AppImage requires **libfuse2** to run. Most modern Linux distributions use FUSE 3 by default, but AppImages still need FUSE 2.

### Install libfuse2

**For Ubuntu/Debian-based systems:**
```bash
sudo apt-get update
sudo apt-get install -y libfuse2
```

## Installation Steps

### 1. Download LM Studio

Download the LM Studio AppImage from the official website. The file will typically be named something like `LM-Studio-0.3.30-2-x64.AppImage`.

### 2. Create Installation Directory (Optional)

It's recommended to keep your AppImages organized in a dedicated directory:

```bash
mkdir -p ~/Applications
```

### 3. Move the AppImage

Move the downloaded AppImage to your installation directory:

```bash
mv ~/Downloads/LM-Studio-*.AppImage ~/Applications/
```

### 4. Make the AppImage Executable

```bash
chmod +x ~/Applications/LM-Studio-*.AppImage
```

### 5. Run LM Studio

You can now run LM Studio directly:

```bash
~/Applications/LM-Studio-*.AppImage
```

## Setting Up Desktop Integration

To make LM Studio appear in your application menu with a custom icon:

### 1. Prepare a Custom Icon (Optional)

If you have a custom PNG icon for LM Studio:

```bash
mkdir -p ~/.local/share/icons
cp /path/to/your/lmstudio-icon.png ~/.local/share/icons/lm-studio.png
```

### 2. Create Desktop Entry

Create a desktop entry file:

```bash
mkdir -p ~/.local/share/applications
```

Create the file `~/.local/share/applications/lm-studio.desktop` with the following content:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=LM Studio
Comment=Local AI Model Studio
Exec=/home/YOUR_USERNAME/Applications/LM-Studio-0.3.30-2-x64.AppImage %U
Icon=/home/YOUR_USERNAME/.local/share/icons/lm-studio.png
Terminal=false
Categories=Development;Utility;Science;
StartupNotify=true
StartupWMClass=lm-studio
```

**Important:** Replace `YOUR_USERNAME` with your actual username, or use the full path to where you placed the AppImage.

### 3. Make Desktop Entry Executable

```bash
chmod +x ~/.local/share/applications/lm-studio.desktop
```

### 4. Update Application Database

```bash
update-desktop-database ~/.local/share/applications
gtk-update-icon-cache ~/.local/share/icons/ 2>/dev/null || true
```

### 5. Refresh Your Application Menu

Close and reopen your application launcher, or log out and log back in. LM Studio should now appear in your applications menu with your custom icon.

## Creating a Command-Line Shortcut (Optional)

To run LM Studio from anywhere in the terminal:

### 1. Create Symlink

```bash
mkdir -p ~/.local/bin
ln -sf ~/Applications/LM-Studio-*.AppImage ~/.local/bin/lm-studio
```

### 2. Add to PATH (if not already)

Add this line to your `~/.bashrc` or `~/.profile`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 3. Reload Shell Configuration

```bash
source ~/.bashrc
# or
source ~/.profile
```

### 4. Run from Anywhere

Now you can run LM Studio from any terminal:

```bash
lm-studio
```

## Troubleshooting

### Error: "dlopen(): error loading libfuse.so.2"

**Problem:** The AppImage cannot find libfuse2.

**Solution:** Install libfuse2 as described in the Prerequisites section.

### Desktop Entry Not Showing Up

**Solutions:**
1. Make sure the `.desktop` file is executable
2. Update the desktop database: `update-desktop-database ~/.local/share/applications`
3. Log out and log back in
4. Check that the paths in the `.desktop` file are correct

### AppImage Won't Execute

**Solutions:**
1. Verify the file is executable: `ls -l ~/Applications/LM-Studio-*.AppImage`
2. If not executable, run: `chmod +x ~/Applications/LM-Studio-*.AppImage`
3. Check file integrity by downloading again if necessary

### Icon Not Displaying

**Solutions:**
1. Verify the icon file exists: `ls -l ~/.local/share/icons/lm-studio.png`
2. Make sure the Icon path in the `.desktop` file is correct
3. Update icon cache: `gtk-update-icon-cache ~/.local/share/icons/`
4. Try using an absolute path instead of relative path in the Icon field

## Alternative: Running Without FUSE

If you cannot install libfuse2, you can extract and run the AppImage:

```bash
cd ~/Applications
./LM-Studio-*.AppImage --appimage-extract
cd squashfs-root
./lm-studio
```

This extracts the AppImage contents to a `squashfs-root` directory and runs the application directly.


