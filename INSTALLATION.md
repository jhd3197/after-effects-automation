# Installation Guide

Complete installation instructions for After Effects Automation.

## Requirements

- **Python 3.7+**
- **Adobe After Effects** (2024, 2025, or 2025 Beta recommended)
- **Windows, macOS, or Linux**

## Installation Methods

### Method 1: Via Pip (Recommended)

```bash
pip install after-effects-automation
```

### Method 2: From Source

```bash
git clone https://github.com/jhd3197/after-effects-automation.git
cd after-effects-automation
pip install -e .
```

## After Effects Setup

### 1. Install the Startup Script

This allows Python to communicate with After Effects while it's running:

```bash
python install_ae_runner.py
```

**What this does:**
- Installs `ae_command_runner.jsx` to After Effects' startup folder
- Enables real-time script execution without manually opening AE
- Required for the batch automation system to work

**Location installed:**
- Windows: `%APPDATA%\Adobe\After Effects\<version>\Scripts\Startup\`
- macOS: `~/Library/Preferences/Adobe/After Effects/<version>/Scripts/Startup/`

### 2. Enable Scripting in After Effects

1. Open After Effects
2. Go to **Edit > Preferences > Scripting & Expressions**
3. Check **Allow Scripts to Write Files and Access Network**
4. Restart After Effects

## Environment Configuration

### Create .env File

```bash
cp .env.example .env
```

### Configure Settings

Edit `.env` with your paths:

```env
# Cache folder for temporary files
CACHE_FOLDER=C:/temp/ae_cache

# After Effects installation folder
AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files

# Project folder name (created automatically in AE)
AFTER_EFFECT_PROJECT_FOLDER=au-automate

# Optional: Override aerender path
# AERENDER_PATH=C:/custom/path/to/aerender.exe
```

### Important Paths

| Setting | Description | Example |
|---------|-------------|---------|
| `CACHE_FOLDER` | Temp files, scripts, logs | `C:/temp/ae_cache` |
| `AFTER_EFFECT_FOLDER` | AE installation directory | `C:/Program Files/Adobe/Adobe After Effects 2025/Support Files` |
| `AERENDER_PATH` | Path to aerender.exe (optional) | Auto-detected from `AFTER_EFFECT_FOLDER` |

## Verify Installation

### Test Basic Functionality

```bash
# If installed via pip
ae-automation --version

# Test with an example
cd examples/basic_composition
python run.py
```

### Check Startup Script

1. Open After Effects
2. Check **Window > Info** panel
3. Look for "AE Command Runner initialized" message

If you don't see this message, the startup script isn't installed correctly.

## Troubleshooting

### "Module not found" Error

```bash
# Reinstall package
pip uninstall after-effects-automation
pip install after-effects-automation

# Or for development
pip install -e .
```

### After Effects Won't Start

**Check paths in .env:**
```bash
# Test if path exists
ls "C:/Program Files/Adobe/Adobe After Effects 2025/Support Files"
```

**Common issues:**
- Wrong version number in path (2024 vs 2025)
- AE installed in custom location
- Spaces in path not quoted correctly

### Scripts Don't Execute

1. **Verify scripting is enabled** (see step 2 above)
2. **Reinstall startup script:**
   ```bash
   python install_ae_runner.py
   ```
3. **Restart After Effects**

### Permission Denied Errors

**Windows:**
- Run terminal as Administrator
- Check antivirus isn't blocking Python

**macOS/Linux:**
- Check file permissions on cache folder
- May need `sudo` for some operations

## Uninstallation

### Remove Package

```bash
pip uninstall after-effects-automation
```

### Remove Startup Script

**Windows:**
```cmd
del "%APPDATA%\Adobe\After Effects\<version>\Scripts\Startup\ae_command_runner.jsx"
```

**macOS:**
```bash
rm ~/Library/Preferences/Adobe/After Effects/<version>/Scripts/Startup/ae_command_runner.jsx
```

### Clean Cache

```bash
# Delete cache folder specified in .env
rm -rf C:/temp/ae_cache
```

## Next Steps

- [Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
- [Examples](examples/README.md) - Practical examples
- [CLI Guide](CLI_GUIDE.md) - Command-line usage
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

## Platform-Specific Notes

### Windows

- Use forward slashes `/` or double backslashes `\\` in paths
- Run PowerShell/CMD as Administrator for installation
- Check Windows Defender isn't blocking Python scripts

### macOS

- Grant Terminal "Full Disk Access" in Security Settings
- After Effects might need approval in Security & Privacy

### Linux

- Wine required to run After Effects (experimental)
- Path structure may differ
- Community support limited

## Support

- **Issues**: [GitHub Issues](https://github.com/jhd3197/after-effects-automation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jhd3197/after-effects-automation/discussions)
