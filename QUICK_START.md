# Quick Start Guide

Get After Effects Automation running and produce your first rendered video — from install to MP4 output — in a single walkthrough.

## Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.7+** installed
- ✅ **Adobe After Effects** (2024, 2025, or 2026)
- ✅ **Administrator/sudo access** (for initial setup)

## Step 1: Install the Package

```bash
pip install after-effects-automation
```

## Step 2: Install AE Integration

This enables Python to communicate with After Effects:

```bash
python install_ae_runner.py
```

**What this does:**
- Installs a startup script (`ae_command_runner.jsx`) in After Effects' startup folder
- This script monitors a file-based command queue, allowing Python to send ExtendScript commands to AE asynchronously
- Enables real-time automation without manual intervention

## Step 3: Enable Scripting in After Effects

1. Open **After Effects**
2. Go to **Edit > Preferences > Scripting & Expressions**
3. Check **"Allow Scripts to Write Files and Access Network"**
4. **Restart After Effects**

## Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your text editor
# Set AFTER_EFFECT_FOLDER to your AE installation path
```

**Example paths:**

**Windows:**
```env
AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files
```

**macOS:**
```env
AFTER_EFFECT_FOLDER=/Applications/Adobe After Effects 2025/Adobe After Effects 2025.app/Contents
```

## Step 5: Run Your First Example

```bash
cd examples/basic_composition
python run.py
```

**That's it!**

## What Happens Next

Here is the end-to-end pipeline that runs when you execute a single command. Every step is handled automatically:

When you run `python run.py`, the automation will:

1. ✅ **Auto-create template** (if it doesn't exist)
2. ✅ **Launch After Effects**
3. ✅ **Build compositions** with intro and outro scenes
4. ✅ **Render video** to `output/FinalComposition.mp4`
5. ✅ **Complete in ~2 minutes**

You should see output like this:

```
🎬 Starting After Effects Automation...
📁 Template not found - creating automatically...
✅ Template created: basic_template.aep
🚀 Launching After Effects...
⚙️  Building compositions...
🎨 Adding scenes to timeline...
🎥 Rendering video...
✅ Done! Output: output/FinalComposition.mp4
```

## Verify Installation

### Check the startup script installed correctly:

1. Open After Effects
2. Go to **Window > Info**
3. Look for **"AE Command Runner initialized"**

If you see this message, you're ready to go!

## Next Steps

### Try More Examples

```bash
# Text animation example
cd examples/text_animation
python run.py

# Quick rendering of existing .aep files
cd examples/render_only
python render.py
```

### Learn the Basics

- **[Examples Guide](examples/README.md)** - See what you can build
- **[Main README](README.md)** - Full feature overview
- **[CLI Guide](CLI_GUIDE.md)** - Command-line tools
- **Web Editor** - Run `ae-automation editor config.json` to edit configurations visually in your browser

## Common Issues

### After Effects won't start?

**Check your .env path:**
```bash
# Make sure this path exists on your system
ls "C:/Program Files/Adobe/Adobe After Effects 2025/Support Files"
```

### Scripts not executing?

1. Verify scripting is enabled (Step 3 above)
2. Reinstall the startup script:
   ```bash
   python install_ae_runner.py
   ```
3. Restart After Effects

### Module not found error?

```bash
# Reinstall the package
pip uninstall after-effects-automation
pip install after-effects-automation
```

### Empty/black video output?

Update to the latest version (batch system bug was fixed in v0.0.4):
```bash
pip install --upgrade after-effects-automation
```

**📖 More Solutions:** See [Troubleshooting Guide](TROUBLESHOOTING.md)

## Getting Help

- **📖 Documentation** - All guides in repo root
- **💡 Working Examples** - `examples/` folder
- **🐛 Report Issues** - [GitHub Issues](https://github.com/jhd3197/after-effects-automation/issues)

---

**Ready to automate!** 🚀

Start with `examples/basic_composition` and modify it to fit your needs.
