# CLI Guide

The CLI is one of three interfaces provided by After Effects Automation, alongside the Python API and the built-in Web Editor. Use it to run automation pipelines, launch the visual config editor, test compatibility, and diagnose issues — all from the terminal.

| Interface | Best For | Entry Point |
|-----------|----------|-------------|
| **Python API** | Programmatic control, custom workflows | `from ae_automation import Client` |
| **CLI** | Running configs, testing, diagnostics | `ae-automation run config.json` |
| **Web Editor** | Visual config editing in the browser | `ae-automation editor config.json` |

## Installation

```bash
# Install the package
pip install after-effects-automation

# The CLI commands are automatically registered
```

## Verify Installation

```bash
# Check that commands are available
ae-automation --help

# Should show available commands
```

## Available Commands

### 1. `run` - Run Automation

Execute After Effects automation from a JSON configuration file.

```bash
ae-automation run <config_file>
```

**Examples:**

```bash
# Run automation from a config file
ae-automation run config.json

# Run from a custom path
ae-automation run path/to/my_config.json
```

**What it does:**
- Loads your JSON configuration
- Auto-creates template if needed
- Opens After Effects
- Builds compositions
- Applies custom actions
- Renders video (if enabled)

**Typical use:**
You create a `run.py` file that builds a config and calls `client.startBot(config)`. The CLI command is an alternative way to run existing config files directly.

---

### 2. `editor` - Web-Based Config Editor

Launch a web interface to visually edit configuration files.

```bash
ae-automation editor [config_file] [--host HOST] [--port PORT]
```

**Arguments:**
- `config_file` - Path to JSON config (default: config.json)
- `--host` - Server host (default: 127.0.0.1)
- `--port` - Server port (default: 5000)

**Examples:**

```bash
# Edit default config.json
ae-automation editor

# Edit specific config
ae-automation editor my_project.json

# Run on custom port
ae-automation editor config.json --port 8080

# Make accessible from network
ae-automation editor config.json --host 0.0.0.0 --port 8080
```

**What it does:**
- Starts local web server
- Opens editor in your browser
- Provides visual interface for editing
- Auto-saves changes to JSON file

**Use when:**
- You want to edit configs visually
- You're new to the JSON structure
- You need to preview timeline changes

---

### 3. `test` - Compatibility Tests

Test package compatibility with your After Effects installation.

```bash
ae-automation test [--verbose] [--version VERSION]
```

**Options:**
- `--verbose`, `-v` - Show detailed output
- `--version VERSION` - Test specific AE version

**Examples:**

```bash
# Run basic tests
ae-automation test

# Show detailed output
ae-automation test --verbose

# Test specific AE version
ae-automation test --version 2025

# Verbose test for specific version
ae-automation test -v --version 2024
```

**What it does:**
- Tests package imports
- Checks environment config
- Validates JSX scripts
- Tests After Effects detection
- Verifies dependencies

**Use when:**
- Setting up for the first time
- Troubleshooting issues
- After updating After Effects

---

### 4. `diagnose` - Run Diagnostics

Run comprehensive diagnostic checks for troubleshooting.

```bash
ae-automation diagnose [--no-wait]
```

**Options:**
- `--no-wait` - Don't wait for user input at end

**Examples:**

```bash
# Run full diagnostics
ae-automation diagnose

# Run without pause at end (for scripts)
ae-automation diagnose --no-wait
```

**What it does:**
- Checks After Effects installation
- Verifies scripting permissions
- Tests startup script installation
- Validates environment settings
- Generates diagnostic report

**Use when:**
- After Effects won't start
- Scripts aren't executing
- Setting up on a new machine
- Getting unexplained errors

---

## Common Workflows

### Quick Start

```bash
# 1. Navigate to an example
cd examples/basic_composition

# 2. Run the automation
python run.py

# Output: Automated video in output/FinalComposition.mp4
```

### Config-Based Workflow

```bash
# 1. Create or edit config
ae-automation editor my_project.json

# 2. Run automation
ae-automation run my_project.json

# 3. Video renders to specified output
```

### Development Workflow

```bash
# 1. Test your setup first
ae-automation test --verbose

# 2. Run diagnostics if issues
ae-automation diagnose

# 3. Edit your config
ae-automation editor config.json

# 4. Run automation
ae-automation run config.json
```

### Batch Processing

Because each `ae-automation run` invocation is a self-contained pipeline (launch AE, build, render, done), you can chain multiple runs to produce videos in sequence without manual intervention:


**Windows (batch_render.bat):**
```batch
ae-automation run video1_config.json
ae-automation run video2_config.json
ae-automation run video3_config.json
```

**Linux/macOS (batch_render.sh):**
```bash
#!/bin/bash
ae-automation run video1_config.json
ae-automation run video2_config.json
ae-automation run video3_config.json
```

---

## Working with Examples

The package includes working examples you can run directly:

### Basic Composition
```bash
cd examples/basic_composition
python run.py
```

Creates a 10-second video with intro and outro scenes.

### Text Animation
```bash
cd examples/text_animation
python run.py
```

Creates a video with multiple styled text layers.

### Render Only
```bash
cd examples/render_only
python render.py
```

Renders existing .aep files without automation.

**📖 More:** See [examples/README.md](examples/README.md)

---

## Environment Configuration

Configure via `.env` file in your project root:

```env
# After Effects installation path
AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files

# Cache folder for temporary files
CACHE_FOLDER=C:/temp/ae_cache

# Project folder name (created in AE)
AFTER_EFFECT_PROJECT_FOLDER=au-automate
```

**Platform-specific paths:**

**Windows:**
```env
AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files
```

**macOS:**
```env
AFTER_EFFECT_FOLDER=/Applications/Adobe After Effects 2025/Adobe After Effects 2025.app/Contents
```

---

## Troubleshooting

### Command not found

**Error:**
```
'ae-automation' is not recognized as an internal or external command
```

**Solution:**
```bash
# Reinstall package
pip uninstall after-effects-automation
pip install after-effects-automation

# Verify installation
pip show after-effects-automation
```

### Module import errors

**Error:**
```
ModuleNotFoundError: No module named 'ae_automation'
```

**Solution:**
```bash
# Reinstall with dependencies
pip install --upgrade after-effects-automation

# Or for development
cd after-effects-automation
pip install -e .
```

### After Effects not found

**Error:**
```
Error: After Effects not detected
```

**Solution:**
```bash
# 1. Check .env file
cat .env

# 2. Verify path exists
ls "C:/Program Files/Adobe/Adobe After Effects 2025/Support Files"

# 3. Run diagnostics
ae-automation diagnose
```

### Port already in use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Use different port
ae-automation editor config.json --port 8080
```

### Config file errors

**Error:**
```
Error: Configuration file not found
```

**Solution:**
```bash
# Create config with editor
ae-automation editor my_config.json

# Or check file path
ls my_config.json
```

---

## Getting Help

```bash
# Main help
ae-automation --help

# Command-specific help
ae-automation run --help
ae-automation editor --help
ae-automation test --help
ae-automation diagnose --help
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Run automation | `ae-automation run config.json` |
| Open editor | `ae-automation editor config.json` |
| Run tests | `ae-automation test` |
| Verbose tests | `ae-automation test -v` |
| Diagnostics | `ae-automation diagnose` |
| Help | `ae-automation --help` |

---

## Using the Python API Instead

You can also drive the same automation pipeline from Python directly, which gives you full programmatic control over config generation and execution:

```python
from ae_automation import Client

# Initialize client
client = Client()

# Run automation
client.startBot("config.json")
```

This is what the `run.py` files in examples use.

---

## Legacy Commands

For backward compatibility:

```bash
# Old way (still works)
ae-automate config.json

# New way (preferred)
ae-automation run config.json
```

---

## Next Steps

- **[Quick Start](QUICK_START.md)** - Get started in 5 minutes
- **[Examples](examples/README.md)** - Working examples
- **[Troubleshooting](TROUBLESHOOTING.md)** - Problem solving
- **[Main README](README.md)** - Package overview

---

## Support

- **Issues:** [GitHub Issues](https://github.com/jhd3197/after-effects-automation/issues)
- **Documentation:** All `.md` files in repo
- **Examples:** Working code in `examples/` folder
