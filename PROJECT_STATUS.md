# Project Status & Roadmap

Full audit of the After Effects Automation codebase as of January 2026.
This document covers what exists, what's missing, what's broken, and what to build next.

---

## Table of Contents

- [Architecture Snapshot](#architecture-snapshot)
- [What Works Today](#what-works-today)
- [The Testing Problem](#the-testing-problem)
- [Code Quality Issues](#code-quality-issues)
- [Missing and Incomplete Features](#missing-and-incomplete-features)
- [CI/CD Gaps](#cicd-gaps)
- [Dependency Audit](#dependency-audit)
- [Configuration Drift](#configuration-drift)
- [TODOs Left in Source Code](#todos-left-in-source-code)
- [Roadmap](#roadmap)

---

## Architecture Snapshot

```
Python Config (JSON)
        |
        v
  ae_automation.Client        <-- Composed from 6 mixins
        |
        v
  File-Based Command Queue    <-- Scripts written to %APPDATA%/ae_automation/queue/
        |
        v
  ae_command_runner.jsx        <-- AE startup script watches queue directory
        |
        v
  After Effects (ExtendScript) <-- Executes JSX scripts inside AE
        |
        v
  aerender.exe                 <-- Renders final MP4
```

### Mixin Composition

The `Client` class in `ae_automation/__init__.py` inherits from all six mixins:

| Mixin | File | Lines | What It Does |
|-------|------|-------|--------------|
| `afterEffectMixin` | `mixins/afterEffect.py` | ~660 | Core automation: launching AE, JSX execution, composition building, rendering |
| `botMixin` | `mixins/bot.py` | ~42 | Loads JSON configs, orchestrates the pipeline via `startBot()` |
| `ProcessManagerMixin` | `mixins/processManager.py` | ~502 | Process detection, window readiness, crash dialog handling, diagnostics |
| `TemplateGeneratorMixin` | `mixins/templateGenerator.py` | ~272 | Programmatic .aep creation from config dictionaries |
| `VideoEditorAppMixin` | `mixins/VideoEditorApp.py` | -- | Flask web editor with REST API for visual config editing |
| `ToolsMixin` | `mixins/tools.py` | ~46 | Utility functions: hex to RGBA, slugify, process checks, file reading |

### ExtendScript Bridge

38 JSX/JS files in `ae_automation/mixins/js/`:

**Core infrastructure:**
- `framework.js` -- Utility functions prepended to every script execution
- `json2.js` -- JSON polyfill for older AE versions
- `ae_command_runner.jsx` -- Startup script that monitors the queue directory
- `ae_server.jsx` -- Server-style communication (alternative to queue)

**Composition operations:**
- `addComp.jsx`, `create_folder.jsx`, `file_map.jsx`
- `duplicate_comp.jsx`, `duplicate_comp_1.jsx`, `duplicate_comp_2.jsx`
- `add_comp_to_templates.jsx`

**Layer operations:**
- `add_text_layer.jsx`, `add_solid_layer.jsx`, `add_null_layer.jsx`, `add_shape_layer.jsx`
- `selectItem.jsx`, `selectItemByName.jsx`, `selectItemLayer.jsx`
- `selectLayerByIndex.jsx`, `selectLayerByLayer.jsx`

**Property/resource operations:**
- `update_properties.jsx`, `update_properties_frame.jsx`
- `add_resource.jsx`, `update_resource.jsx`
- `add_marker.jsx`, `getMarker.jsx`
- `renameItem.jsx`, `openItemName.jsx`, `checkIfItemExists.jsx`

**Project operations:**
- `create_new_project.jsx`, `save_project.jsx`, `debug_save_project.jsx`
- `importFile.jsx`, `renderComp.jsx`, `workAreaComp.jsx`, `run_command.jsx`

**Diagnostics:**
- `debug_create_comp.jsx`, `check_scripting_enabled.jsx`

### Three Interfaces

1. **Python API** -- `from ae_automation import Client; client.startBot("config.json")`
2. **CLI** -- `ae-automation run config.json` (with subcommands: `run`, `editor`, `test`, `diagnose`)
3. **Web Editor** -- Flask app at `ae-automation editor config.json`

---

## What Works Today

These are the features that are implemented and functional:

- Client instantiation with JS framework loading
- JSON config parsing with `project` and `timeline` sections
- AE process launching and intelligent readiness detection (`ProcessManagerMixin`)
- Crash dialog handling during AE startup
- File-based command queue (Python writes JSX to queue, AE runner executes)
- Composition creation, duplication, editing
- Layer operations (text, solid, null, shape)
- Property updates on layers
- Resource importing and management
- Template generation from config dictionaries (`buildTemplate`)
- Rendering via `aerender.exe`
- CLI with `run`, `editor`, `test`, and `diagnose` subcommands
- Web editor (Flask + React) for visual config editing
- Utility functions (slug, hexToRGBA, file reading, process checking)
- Full diagnostic suite (`run_full_diagnostic`)
- Compatibility test suite (`test.py`) with colored output and JSON reports
- Unit test suite (4 test files covering client init, config parsing, JSX validation, utilities)
- CI/CD for PyPI publishing and GitHub Pages demo deployment
- Documentation (8 markdown guides)
- 3 working examples (basic composition, text animation, render only)

---

## The Testing Problem

This is the biggest architectural challenge for the project. After Effects is a commercial desktop application that costs $23/month. You cannot install it in a GitHub Actions runner. You cannot run it headlessly on a Linux VM. Every core method in this project -- `startAfterEffect()`, `createComp()`, `editComp()`, `renderFile()`, `startBot()` -- ultimately talks to a running AE process through the file-based command queue or direct ExtendScript execution.

Even locally, a single automation run can take over a minute because AE needs to launch, load plugins, build compositions, and render.

### What This Means for Testing

The project currently has **two tiers** of tests, but only one of them can run anywhere:

**Tier 1: Unit tests** (`tests/` directory) -- Run anywhere, no AE needed
- `test_client.py` -- Client instantiation, method existence, cache folder creation
- `test_config.py` -- JSON config structure validation, time format parsing
- `test_jsx_integration.py` -- JSX file existence, readability, syntax markers, framework loading
- `test_utils.py` -- slug(), hexToRGBA(), file_get_contents(), process_exists()

**Tier 2: Compatibility tests** (`test.py`) -- Requires Windows + AE installed
- Import verification, environment setup, client init, JS framework, utilities, JSON parsing, AE detection, JSX scripts, dependency checks

Neither tier tests the actual automation pipeline. There are **zero tests** for:
- `startAfterEffect()` / `startBot()` (launching AE and running a config)
- `createComp()` / `editComp()` (building compositions)
- `renderFile()` (rendering output)
- `buildTemplate()` (template generation end-to-end)
- `VideoEditorApp` Flask routes (web editor API)
- Error recovery paths (what happens when AE crashes mid-automation)

### Testing Strategy: What Can Actually Be Done

Here's a realistic breakdown of what's testable at each level:

#### 1. Pure Unit Tests (CI-safe, no AE, no Windows)

These can run in GitHub Actions on `ubuntu-latest` right now. They test logic in isolation, with no OS or AE dependencies.

**What to test:**
- Config validation and parsing logic
- Text sanitization (`sanitize_text_for_ae`) -- the HTML `<br>` to `\r` conversion, quote handling
- Path conversion logic (backslash to forward slash for JS)
- Time format parsing (`time_to_seconds`)
- Hex to RGBA conversion
- Slug generation
- JSX template string replacement (the `{key}` placeholder system)
- JSON config structure validation (required fields, types, defaults)
- Template config validation (does the config dict have valid structure before we try to send it to AE)

**What's needed:**
- Mock `settings.py` so it doesn't call `validate_settings()` on import (which checks for `AFTER_EFFECT_FOLDER` on disk and fails on Linux)
- Or: guard `validate_settings()` behind an environment flag so tests can skip path validation
- Or: restructure settings so validation is lazy rather than on-import

The `settings.py` import problem is the main blocker. Right now, `from ae_automation import Client` triggers `from ae_automation import settings` which calls `validate_settings()` on module load, which checks that `C:/Program Files/Adobe/Adobe After Effects 2025/Support Files` exists. On Linux CI, this raises `ValueError` immediately. The fix is straightforward -- make validation opt-in or deferrable.

#### 2. Mock-Based Integration Tests (CI-safe, no AE)

These test the orchestration logic without actually talking to AE. The idea is to mock `runScript()` (the method that writes JSX to the queue) and verify that the right scripts get called with the right parameters.

**What you can validate with mocks:**
- `startBot("config.json")` reads the config, resolves paths, and calls `startAfterEffect(data)` with the right data structure
- `buildTemplate(config, output_path)` calls `createNewProject()`, then `createFolder()`, then `createComp()` for each composition, then the right layer methods for each layer, then `saveProject()`
- `createComp()` calls `runScript("addComp.jsx", ...)` with the right replacements
- `addTextLayer()` calls `runScript("add_text_layer.jsx", ...)` with the right replacements
- Error paths: what happens if `runScript` raises, if config is missing fields, if paths don't exist

**What this doesn't test:**
- Whether the JSX script actually works inside AE
- Whether the parameter replacements produce valid ExtendScript
- Whether the file-based queue timing works in practice
- Whether `aerender` produces correct output

This is the highest-value testing tier to add next. It validates the Python orchestration layer without needing AE.

#### 3. JSX Validation Tests (CI-safe, no AE)

The 38 JSX files can be validated statically:
- All `{placeholder}` tokens in JSX files have corresponding Python-side replacements
- No JSX file has syntax errors (basic bracket/paren matching, or run through a JS parser)
- Every JSX file referenced by Python methods actually exists on disk
- Framework.js and json2.js produce valid JS when concatenated

This is already partially done in `test_jsx_integration.py` but could go deeper.

#### 4. Local Integration Tests (Windows + AE required)

These run on a developer machine with AE installed. They're slow (1-5 minutes per test) and can't run in CI.

**What to test:**
- Create a minimal composition and verify it exists in the AE project
- Add a text layer and verify the layer was created
- Render a 1-second test composition and verify the output file exists and has non-zero size
- Run `buildTemplate()` with a minimal config and verify the .aep file is created
- Full pipeline: load config -> build comp -> render -> verify output

**How to run them:**
- Separate test file or mark with `@unittest.skipUnless(os.environ.get("AE_INSTALLED"), "Requires After Effects")`
- Run manually: `AE_INSTALLED=1 python -m unittest tests.test_ae_integration -v`
- Never run in CI

#### 5. Smoke Tests (Windows + AE, manual)

The existing `test.py` compatibility suite already serves this purpose. It's meant to be run manually after installation to verify the setup works.

### Summary: Testing Tiers

| Tier | Runs In CI | Needs AE | Needs Windows | Coverage |
|------|-----------|----------|---------------|----------|
| Unit tests | Yes | No | No | Config parsing, utilities, text sanitization, path logic |
| Mock integration | Yes | No | No | Orchestration flow, method call sequences, error paths |
| JSX validation | Yes | No | No | Script existence, placeholder matching, basic syntax |
| Local integration | No | Yes | Yes | Actual AE operations, rendering, file output |
| Smoke tests | No | Yes | Yes | Full pipeline verification (existing `test.py`) |

### The One Blocker

Before any CI tests work, `settings.py` needs to stop failing on import when AE isn't installed. The current code:

```python
# ae_automation/settings.py (line 42-43)
# Validate settings on import
validate_settings()
```

This runs every time anything imports `ae_automation`, including in tests. On Linux (or any machine without AE), it immediately throws `ValueError: After Effects folder not found`. Options:

1. **Environment variable guard:** `if os.getenv("AE_VALIDATE_SETTINGS", "1") == "1": validate_settings()`
2. **Lazy validation:** Only validate when a method actually needs AE (first call to `runScript`, etc.)
3. **Try/except with warning:** Catch the error, print a warning, let the import succeed

Option 2 is cleanest. Settings can still be loaded as defaults, but the path existence check only fires when you actually try to use AE.

---

## Code Quality Issues

### Critical: Dead Imports and Code

**`afterEffect.py:2`** -- Completely unused import from Python's internal parser:
```python
from lib2to3.pgen2.pgen import DFAState  # Never referenced anywhere
```

**`afterEffect.py:6`** -- Unused pandas import:
```python
import pandas as pd  # Never used in this file
```

**`afterEffect.py:7`** -- Unused pydantic import:
```python
from pydantic import FilePath  # Never referenced
```

**`bot.py:1`** -- Unused pandas import:
```python
import pandas as pd  # Never used
```

**`bot.py:17`** -- Redundant os import inside method body (already available at module level via other mixins):
```python
import os  # Re-imported inside startBot()
```

**`tools.py:22-26`** -- Dead test function:
```python
def testFunction(self):
    """testFunction"""
    print("testFunction")
```

**`afterEffect.py:30`** -- Unused class variable:
```python
afterEffectItems=[]  # Declared but never populated or read
```

### High: Bare Except Clauses

`processManager.py:80` catches everything silently:
```python
except:
    pass  # Could be hiding real errors
```

This is inside `wait_for_window()` as a fallback when `pygetwindow` fails. It should at least catch `Exception` and ideally log it.

### High: Minimal Error Handling in Core Module

`afterEffect.py` is 660 lines with only ~6 try/except blocks. The core automation logic -- launching AE, writing scripts, waiting for results -- largely assumes nothing will go wrong. Key gaps:

- `os.startfile(filePath)` at line 78 has no error handling
- Script file writing to the queue directory has no error handling
- No retry logic when AE doesn't respond
- No cleanup of queue files on failure

### Medium: Boolean Comparison Style

```python
# afterEffect.py:78
if data["project"]["debug"] == False:
```

Should be:
```python
if not data["project"]["debug"]:
```

### Medium: Inconsistent Naming

The codebase mixes camelCase and snake_case without a clear convention:

- camelCase: `startAfterEffect`, `createComp`, `editComp`, `hexToRGBA`, `startBot`, `runScript`
- snake_case: `file_get_contents`, `process_exists`, `wait_for_process`, `sanitize_text_for_ae`

The newer code (`processManager.py`, `templateGenerator.py`) uses snake_case. The older core (`afterEffect.py`, `tools.py`) uses camelCase. There's no strong reason to enforce one style retroactively since it would break the public API, but new code should consistently use snake_case.

### Medium: Docstring Quality

- `afterEffectMixin` has the docstring `"""ToolsMixin"""` (copy-paste error)
- `botMixin` docstring is just `"""Bot Mixin"""`
- Many methods have no docstrings at all in `afterEffect.py`
- `templateGenerator.py` has good docstrings (the newer code is better)

### Low: No Type Hints

Zero type annotations across the entire codebase. Every method signature is untyped:

```python
def startAfterEffect(self, data):  # data is a dict, but you'd never know
def createComp(self, compName, compWidth=1920, compHeight=1080, ...):  # all untyped
def hexToRGBA(self, hex):  # hex is a string like "#FF0000"
```

This makes IDE autocomplete unreliable and prevents static analysis tools from catching bugs.

---

## Missing and Incomplete Features

### CLI Commands Advertised But Not Implemented

`cli.py` shows these in its help text (lines 139-147) but they have no subparser definitions and no handler functions:

```
ae-automation generate --all
ae-automation generate --template tutorial
ae-automation generate --template social-media --output my_template.aep

ae-automation export --template tutorial
ae-automation export --template social-media --output-dir renders/
ae-automation export --template tutorial --comp IntroTemplate --force
```

Running `ae-automation generate` will print the top-level help (as if no command was given) since there's no `generate` subparser. A user reading the help text would expect these to work.

The `TemplateGeneratorMixin.buildTemplate()` method exists and could back the `generate` command. The `export` command would combine template generation with rendering.

### Unresolved Feature TODOs

From `afterEffect.py:24-29`:

```python
#TODO - Add search for items inside folder
#FIXME - Create a function to duplicate comp and loop through layers to duplicate all the comps inside the comp
#TODO - Create a duplicate function for items inside folder
#TODO - Create function to edit values from comp or create a template.json and add the values there
#TODO - Add transitions layer
```

These represent real gaps in composition management:
- **Folder item search** -- Currently no way to enumerate items inside an AE project folder from Python
- **Deep comp duplication** -- `duplicate_comp.jsx` exists but doesn't recursively duplicate nested comps
- **Template-based value editing** -- Would allow a template.json to define editable values, making configs reusable
- **Transitions** -- No built-in support for transitions between scenes

### Planned Features from CHANGELOG.md

These are listed but not started:

- Real-time progress tracking
- Batch processing queue
- Template marketplace/sharing
- GUI application (beyond web editor)
- Video preview generation
- Cloud rendering integration
- Version control for templates
- Automated testing against AE versions

Under consideration:

- macOS support
- Linux support (via Wine)
- Plugin system for custom actions
- Expression library
- Preset management
- Team collaboration features

---

## CI/CD Gaps

### Current Workflows

**`publish.yml`** -- Triggers on push to `main`:
1. Bumps version tag
2. Updates VERSION file and setup.py
3. Builds frontend (Node.js 18)
4. Creates GitHub Release
5. Builds Python package
6. Publishes to PyPI

**`deploy-demo.yml`** -- Triggers on push to `main`:
1. Builds React frontend in demo mode
2. Deploys to GitHub Pages

### What's Missing

**No test execution in CI.** The publish workflow builds and ships without running a single test. A bad commit goes straight to PyPI.

**No linting or formatting.** No flake8, black, ruff, or any code quality tool runs in CI. The dead imports and bare excepts described above would be caught automatically.

**No Python version matrix.** The workflow uses `python-version: '3.x'` which just picks the latest. The package claims to support 3.7+, but this is never verified. Python 3.7 reached end-of-life in June 2023 -- the minimum should probably be 3.9 or 3.10 at this point.

**No dependency security scanning.** No Dependabot, no `pip-audit`, no `safety` checks.

**CI runs on Linux but the package is Windows-only.** The `publish.yml` runs on `ubuntu-latest` for building and publishing. This works for building the sdist/wheel, but means the unit tests (if added to CI) would need the `settings.py` import fix mentioned in the testing section.

**No branch protection.** Merges to `main` immediately trigger a PyPI publish. There's no PR review gate, no required status checks, no staging workflow.

### Recommended CI Additions

A `test.yml` workflow that runs on every push and PR:

```yaml
# What it should do:
# 1. Run unit tests on ubuntu-latest with Python 3.10, 3.11, 3.12
# 2. Run linting (ruff or flake8)
# 3. Run type checking (mypy) -- optional, requires adding type hints first
# 4. Verify package builds cleanly
```

This requires fixing the `settings.py` import-time validation first.

---

## Dependency Audit

### Current Dependencies (from setup.py)

| Package | Version | Actually Used? | Purpose |
|---------|---------|---------------|---------|
| `python-dotenv>=0.19.0` | Yes | Yes | Loads `.env` files |
| `pyautogui>=0.9.53` | Yes | Yes | GUI automation (keyboard, mouse) |
| `pydirectinput>=1.0.4` | Yes | Yes | Direct keyboard input on Windows |
| `pywinauto>=0.6.8` | Yes | Yes | Windows UI automation, window detection |
| `pandas>=1.3.0` | Yes | **No** | Imported in `bot.py` and `afterEffect.py` but never used |
| `pydantic>=1.8.2` | Yes | **No** | Imported (`FilePath`) in `afterEffect.py` but never referenced |
| `jsmin>=3.0.0` | Yes | Yes | Minifies JS framework before execution |
| `mutagen>=1.45.1` | Yes | Yes | Reads MP3 metadata (audio duration) |
| `moviepy>=1.0.3` | Yes | Yes | Video file processing (duration, properties) |
| `flask>=2.0.0` | Yes | Yes | Web editor backend |
| `flask-cors>=3.0.0` | Yes | Yes | CORS for web editor API |
| `werkzeug>=2.0.0` | Yes | Yes | WSGI utilities (Flask dependency) |
| `psutil>=5.8.0` | Yes | Yes | Process management |

### Not in setup.py but imported

| Package | Where | Purpose |
|---------|-------|---------|
| `python-slugify` | `tools.py` | `from slugify import slugify` -- slug generation |
| `Pillow` | `tools.py` | `from PIL import ImageColor` -- hex to RGB conversion |
| `pygetwindow` | `processManager.py` | Window enumeration fallback (imported inside try/except) |

These are runtime dependencies that will cause `ImportError` if not installed. They should be in `install_requires`.

### Recommendation

- **Remove** `pandas` and `pydantic` from `install_requires` (and remove their unused imports)
- **Add** `python-slugify` and `Pillow` to `install_requires`
- **Evaluate** whether `pygetwindow` should be a required or optional dependency

Removing `pandas` alone would significantly reduce install size and time -- pandas pulls in numpy and several other heavy packages. For a video automation tool, pandas has no business being a dependency.

---

## Configuration Drift

### .env.example vs settings.py Defaults

| Setting | `.env.example` | `settings.py` default |
|---------|---------------|----------------------|
| `CACHE_FOLDER` | `cache` (relative) | `%APPDATA%/ae_automation/cache` (absolute) |
| `AFTER_EFFECT_FOLDER` | `C:/Program Files/Adobe/Adobe After Effects 2024/Support Files` | `C:/Program Files/Adobe/Adobe After Effects 2025/Support Files` |
| `AFTER_EFFECT_PROJECT_FOLDER` | `au-automate` | `au-automate` (matches) |

The AE version mismatch (2024 in example, 2025 in code) will confuse users who copy `.env.example` to `.env` and expect it to match the defaults.

The `CACHE_FOLDER` difference is intentional -- the example shows the old relative path behavior, while the code now defaults to an absolute path under `%APPDATA%`. But the example should be updated to reflect the current default.

### settings.py Import-Time Side Effects

`settings.py` does three things on import:
1. Loads `.env` file
2. Creates `CACHE_FOLDER` and `QUEUE_FOLDER` directories on disk
3. Validates that `AFTER_EFFECT_FOLDER`, `AERENDER_PATH`, and `JS_DIR` exist on disk

Steps 2 and 3 are side effects that happen whenever anything imports the `ae_automation` package. This is why tests fail on non-Windows systems and in CI environments.

---

## TODOs Left in Source Code

All located in `ae_automation/mixins/afterEffect.py:24-29`:

| # | Type | Description | Effort |
|---|------|-------------|--------|
| 1 | TODO | Add search for items inside folder | Medium -- New JSX script + Python wrapper |
| 2 | FIXME | Duplicate comp with nested comp recursion | Hard -- Requires recursive layer traversal in ExtendScript |
| 3 | TODO | Duplicate function for items inside folder | Medium -- Related to #1 |
| 4 | TODO | Edit values from comp via template.json | Medium -- Template value injection system |
| 5 | TODO | Add transitions layer | Medium -- New JSX scripts for transition effects |

---

## Roadmap

Organized by priority. Each section is independent -- you can tackle them in any order, but the suggested sequence minimizes wasted effort.

### Phase 1: Make Tests Run in CI

**Goal:** `python -m unittest discover tests -v` passes on Ubuntu in GitHub Actions.

1. Fix `settings.py` to not fail on import when AE paths don't exist
   - Make `validate_settings()` lazy or guarded by environment variable
   - Settings values can still have defaults; just don't check disk paths on import
2. Add mock-based integration tests
   - Test `startBot()` flow with mocked `runScript()`
   - Test `buildTemplate()` call sequence with mocked layer methods
   - Test `sanitize_text_for_ae()` with edge cases (nested `<br>`, unicode, empty strings)
3. Add a `test.yml` GitHub Actions workflow
   - Run unit tests on Python 3.10, 3.11, 3.12
   - Run on ubuntu-latest (no AE needed)
   - Required status check before merge to main

### Phase 2: Code Cleanup

**Goal:** Remove dead code, fix imports, add the missing declared dependencies.

1. Remove unused imports
   - `DFAState` from `afterEffect.py`
   - `pandas` from `afterEffect.py` and `bot.py`
   - `pydantic` from `afterEffect.py`
2. Remove dead code
   - `testFunction()` from `tools.py`
   - `afterEffectItems=[]` from `afterEffect.py`
3. Fix `afterEffectMixin` docstring (says "ToolsMixin")
4. Fix bare `except:` in `processManager.py:80` -- change to `except Exception:`
5. Fix boolean comparison: `== False` to `not`
6. Update `setup.py`:
   - Remove `pandas` and `pydantic` from `install_requires`
   - Add `python-slugify` and `Pillow` to `install_requires`
   - Consider adding `pygetwindow` as optional
   - Bump `python_requires` to `>=3.9` (3.7 and 3.8 are EOL)
7. Update `.env.example` to match `settings.py` defaults (AE 2025 path, absolute cache path)

### Phase 3: Implement Missing CLI Commands

**Goal:** `ae-automation generate` and `ae-automation export` work as documented.

1. Add `generate` subparser to `cli.py`
   - `ae-automation generate --template <name>` -- Generate a built-in template
   - `ae-automation generate --all` -- Generate all built-in templates
   - `ae-automation generate --template <name> --output <path>` -- Custom output path
   - Backed by `TemplateGeneratorMixin.buildTemplate()`
   - Needs a registry of built-in template configs (tutorial, social-media, product, slideshow, event -- already mentioned in CHANGELOG)
2. Add `export` subparser to `cli.py`
   - `ae-automation export --template <name>` -- Generate template + render
   - `ae-automation export --template <name> --output-dir <dir>` -- Custom render output
   - `ae-automation export --template <name> --comp <comp>` -- Specify which comp to render
   - Combines `buildTemplate()` with `renderFile()`
3. Or: remove the examples from the help text if these commands aren't planned for the near term

### Phase 4: Error Handling and Logging

**Goal:** Failures produce useful diagnostics instead of raw tracebacks.

1. Add custom exception classes:
   - `AENotFoundError` -- AE installation not found
   - `AENotResponsiveError` -- AE launched but not responding
   - `ScriptExecutionError` -- JSX script failed
   - `RenderError` -- aerender failed
   - `ConfigValidationError` -- Invalid JSON config
2. Add try/except blocks to core `afterEffect.py` methods
   - Script file writing (queue directory could be missing/read-only)
   - `os.startfile()` call (file might not exist)
   - Process launching (AE binary might not be at expected path)
3. Replace `print()` with `logging` module
   - `logging.info()` for progress messages
   - `logging.warning()` for non-fatal issues
   - `logging.error()` for failures
   - `logging.debug()` for verbose details
   - Let users configure log level via env var or CLI flag

### Phase 5: Type Hints

**Goal:** IDE autocomplete works, mypy can validate the codebase.

Start with the public API surface:

```python
# Example of what the signatures should look like
def startBot(self, file_name: str) -> None: ...
def createComp(self, compName: str, compWidth: int = 1920, compHeight: int = 1080,
               duration: float = 120, frameRate: float = 29.97,
               folderName: str = "") -> None: ...
def hexToRGBA(self, hex_color: str) -> str: ...
def buildTemplate(self, template_config: dict, output_path: str) -> None: ...
def wait_for_after_effects_ready(self, timeout: int = 120) -> bool: ...
```

Priority order:
1. `__init__.py` (Client class)
2. `settings.py`
3. `tools.py` (small file, quick win)
4. `templateGenerator.py` (already has good docstrings)
5. `processManager.py`
6. `bot.py`
7. `afterEffect.py` (biggest file, do last)

### Phase 6: Resolve Source Code TODOs

**Goal:** Implement the five features flagged in `afterEffect.py`.

1. **Folder item search** -- New `search_folder_items.jsx` that returns items inside a named folder as JSON. Python wrapper parses the result.
2. **Deep comp duplication** -- Extend `duplicate_comp_2.jsx` to walk layers, find nested CompItems, and duplicate them recursively. This is the hardest item -- ExtendScript doesn't have great recursion support.
3. **Template value system** -- A `template_values.json` file that defines editable fields (text content, colors, durations). `startBot()` reads these values and applies them to the comp before rendering.
4. **Transitions** -- New JSX scripts for common transitions (fade, wipe, slide). Python API: `client.addTransition(from_scene, to_scene, type="fade", duration=1.0)`.

### Phase 7: CI/CD Hardening

**Goal:** Ship with confidence.

1. Add linting to CI (ruff is fast and comprehensive)
2. Add `pip-audit` or `safety` for dependency scanning
3. Add branch protection on `main` -- require PR review + passing checks
4. Test on Python 3.10, 3.11, 3.12 matrix
5. Consider adding a `staging` publish step (publish to TestPyPI first, then promote)
6. Add automatic changelog generation from PR titles/labels

### Phase 8: Bigger Features (from CHANGELOG.md planned list)

These are larger efforts that would each be their own project phase:

- **Real-time progress tracking** -- Extend the file-based queue to include progress markers. AE scripts write status files, Python polls and reports.
- **Batch processing queue** -- Process multiple configs sequentially without restarting AE.
- **Video preview generation** -- Render low-res previews quickly using draft render settings.
- **macOS support** -- Replace Windows-specific APIs (pywinauto, pydirectinput, TASKLIST) with cross-platform alternatives or macOS-specific implementations. AE's ExtendScript bridge works the same way on Mac.
- **Plugin system** -- Allow users to register custom JSX scripts and Python handlers without modifying the package source.

---

## File Reference

Quick reference for finding things in the codebase:

| What | Where |
|------|-------|
| Package entry point | `ae_automation/__init__.py` |
| Client composition | `ae_automation/__init__.py:16-23` |
| Core AE automation | `ae_automation/mixins/afterEffect.py` |
| JSON config loading | `ae_automation/mixins/bot.py` |
| Process management | `ae_automation/mixins/processManager.py` |
| Template generation | `ae_automation/mixins/templateGenerator.py` |
| Web editor | `ae_automation/mixins/VideoEditorApp.py` |
| Utilities | `ae_automation/mixins/tools.py` |
| Settings/env | `ae_automation/settings.py` |
| CLI entry point | `cli.py` |
| ExtendScript bridge | `ae_automation/mixins/js/` (38 files) |
| Unit tests | `tests/` (4 files) |
| Compatibility tests | `test.py` |
| CI: publish | `.github/workflows/publish.yml` |
| CI: demo deploy | `.github/workflows/deploy-demo.yml` |
| Package config | `setup.py` |
| AE runner installer | `install_ae_runner.py` |
| Examples | `examples/` (3 directories) |
| Docs | `*.md` in repo root (8 files) |
