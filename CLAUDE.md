# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

After Effects Automation is a Python package (`after-effects-automation` on PyPI) that programmatically controls Adobe After Effects from Python. It translates Python/JSON configuration into ExtendScript (JavaScript) commands executed inside AE via a file-based command queue, then renders final videos using `aerender`.

**Workflow:** Python config (JSON) → JS bridge → ExtendScript in AE → Composition built → aerender → MP4 output

## Commands

```bash
# Install from source
pip install -e .

# Install AE startup script (required for file-based command queue)
python install_ae_runner.py

# Run unit tests
python -m unittest discover tests -v

# Run a specific test file or class
python -m unittest tests.test_client -v
python -m unittest tests.test_client.TestClientInitialization -v

# Run AE compatibility tests
python test.py

# CLI usage
ae-automation run config.json
ae-automation editor config.json
ae-automation test
ae-automation diagnose
```

## Architecture

### Mixin-based Client

The `Client` class in `ae_automation/__init__.py` composes six mixins:

| Mixin | File | Responsibility |
|-------|------|----------------|
| `afterEffectMixin` | `mixins/afterEffect.py` | Core AE automation: launching AE, executing JSX scripts, building compositions, rendering |
| `botMixin` | `mixins/bot.py` | Loads JSON config files and orchestrates the automation pipeline via `startBot()` |
| `ProcessManagerMixin` | `mixins/processManager.py` | Detects AE process, waits for window readiness, checks responsiveness |
| `TemplateGeneratorMixin` | `mixins/templateGenerator.py` | Programmatic .aep project file creation |
| `VideoEditorAppMixin` | `mixins/VideoEditorApp.py` | Flask-based web editor with REST API for visual config editing |
| `ToolsMixin` | `mixins/tools.py` | Utility functions (hex→RGBA, slugify, process checks) |

### JavaScript/ExtendScript Bridge

`ae_automation/mixins/js/` contains the ExtendScript layer:
- **`framework.js`** — Core JS utilities prepended to every script execution
- **`json2.js`** — JSON polyfill for older AE versions
- **`*.jsx`** — Individual AE operation scripts (addComp, add_text_layer, update_properties, duplicate_comp, save_project, file_map, etc.)

JSX scripts use `{key}` placeholders that Python replaces with actual values before execution.

### File-Based Command Queue

Python writes scripts to `%APPDATA%/ae_automation/queue/`. The AE startup script (`ae_command_runner.jsx`, installed via `install_ae_runner.py`) monitors this directory and executes scripts as they appear. This enables asynchronous, non-blocking communication between Python and AE.

### Configuration

Environment settings in `.env` (see `.env.example`):
- `AFTER_EFFECT_FOLDER` — AE installation path (must match your version)
- `CACHE_FOLDER` — Temp file location (defaults to `%APPDATA%/ae_automation/cache`)
- `AFTER_EFFECT_PROJECT_FOLDER` — AE project folder name
- `AERENDER_PATH` — Optional override for aerender.exe location

Settings are loaded in `ae_automation/settings.py` and validated on import.

### Automation Config Structure

JSON configs have two main sections:
- **`project`** — Output settings (project_file, comp dimensions, fps, output_dir, renderComp)
- **`timeline`** — Array of scenes, each with `custom_actions` that map to JSX operations (update_layer_property, add_resource, add_comp, swap_items_by_index, etc.)

## Key Conventions

- **Path separators:** Use forward slashes in paths destined for JavaScript. Python-side path conversion happens in `settings.py` and `__init__.py`.
- **Text sanitization:** HTML `<br>` tags are converted to AE carriage returns (`\r`) and straight quotes are preserved to avoid UTF-8 issues. This must happen in Python before passing to JS.
- **Method naming:** Mixed camelCase and snake_case throughout the codebase.
- **Entry points:** `cli.py` is the unified CLI (`ae-automation` command). `ae-automate` is a legacy alias that still works.
