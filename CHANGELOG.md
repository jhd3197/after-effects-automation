# Changelog

All notable changes to After Effects Automation will be documented in this file.

## [Unreleased] - 2025-01-XX

### Added - Intelligent Process Management ✅
- **ProcessManagerMixin** - New intelligent wait system for After Effects
  - `wait_for_process()` - Detects when AE process starts
  - `wait_for_window()` - Waits for main window to appear
  - `is_after_effects_responsive()` - Verifies AE can execute scripts
  - `wait_for_after_effects_ready()` - Complete readiness check (main method)
  - `ensure_after_effects_running()` - Starts AE if needed and waits

- **Benefits:**
  - ✅ No more fixed wait times that are too short or too long
  - ✅ Adapts to your system's speed
  - ✅ Verifies AE is actually ready before proceeding
  - ✅ Clear feedback at each stage
  - ✅ Configurable timeouts for different systems

### Added - Unified CLI System ✅
- **Single Command Interface** - `ae-automation` with subcommands
  - `ae-automation run <config>` - Run automation
  - `ae-automation editor <config>` - Open web editor
  - `ae-automation generate` - Generate templates
  - `ae-automation test` - Run compatibility tests

- **Improved Argument Handling:**
  - Positional arguments work correctly
  - `ae-automation editor config.json` now works
  - Comprehensive help for each subcommand
  - Better error messages

- **Backward Compatibility:**
  - `ae-automate` still works as an alias

### Added - Template Generation System ✅
- **Programmatic .aep Creation** - Generate After Effects projects from Python
  - 5 built-in templates (tutorial, social-media, product, slideshow, event)
  - JSON-based template configuration
  - Support for text, solid, null, and shape layers
  - Automatic composition creation

- **New JSX Scripts:**
  - `create_new_project.jsx` - Create new AE project
  - `save_project.jsx` - Save project to disk
  - `add_text_layer.jsx` - Add text layers
  - `add_solid_layer.jsx` - Add solid color layers
  - `add_null_layer.jsx` - Add null objects (placeholders)
  - `add_shape_layer.jsx` - Add shape layers

- **Template Generator API:**
  - `client.buildTemplate(config, output_path)` - Build from config
  - `client.createNewProject()` - Create blank project
  - `client.saveProject(path)` - Save project file
  - `client.addTextLayer()`, `addSolidLayer()`, etc. - Layer creation

### Added - Comprehensive Testing ✅
- **test.py** - Version compatibility test suite
  - Auto-detects After Effects version
  - Tests all major components
  - Generates detailed JSON reports
  - Colored terminal output

- **Unit Tests** (tests/ directory):
  - `test_client.py` - Client initialization tests
  - `test_utils.py` - Utility function tests
  - `test_config.py` - Configuration parsing tests
  - `test_jsx_integration.py` - JSX integration tests

### Added - Documentation ✅
- **CLI_GUIDE.md** - Complete CLI reference with 70+ examples
- **QUICK_START.md** - 5-minute getting started guide
- **TROUBLESHOOTING.md** - Template creation guide
- **PROCESS_MANAGEMENT.md** - Process management documentation
- **CHANGELOG.md** - This file

### Added - Installation Scripts ✅
- `install.bat` - Windows one-click installer
- `install.sh` - Linux/Mac installer
- Verifies installation and shows next steps

### Changed
- **Replaced Fixed Waits** - All `time.sleep(60)` replaced with intelligent waits
  - `startAfterEffect()` now uses `wait_for_after_effects_ready()`
  - `buildTemplate()` uses `ensure_after_effects_running()`
  - Template generation waits properly for AE

- **Updated Dependencies:**
  - Added `psutil>=5.8.0` for process management

### Fixed
- **Template Generation** - Scripts no longer execute before AE is fully loaded
- **Editor Command** - Now accepts positional arguments correctly
- **Process Detection** - Reliably detects when AE is ready

## [0.0.3] - 2024-XX-XX

### Changed
- Version bump to 0.0.3
- README enhancements with tips and project links

## [0.0.2] - 2024-XX-XX

### Added
- Initial public release
- Basic automation functionality
- Web-based editor
- JSON configuration system

## Future Improvements

### Planned Features
- [ ] Real-time progress tracking
- [ ] Batch processing queue
- [ ] Template marketplace/sharing
- [ ] GUI application (beyond web editor)
- [ ] Video preview generation
- [ ] Cloud rendering integration
- [ ] Version control for templates
- [ ] Automated testing against AE versions

### Under Consideration
- Support for macOS
- Support for Linux (via Wine)
- Plugin system for custom actions
- Expression library
- Preset management
- Team collaboration features

## Breaking Changes

None in this release. All changes are backward compatible.

## Migration Guide

### From 0.0.2 to Current

No breaking changes. However, you should:

1. **Reinstall the package:**
   ```bash
   pip install -e .
   ```

2. **Use new CLI commands:**
   ```bash
   # Old way (still works)
   python run.py config.json

   # New way (recommended)
   ae-automation run config.json
   ```

3. **Update your code to use wait mechanisms:**
   ```python
   # Old (still works but not recommended)
   time.sleep(60)

   # New (recommended)
   client.wait_for_after_effects_ready()
   ```

## Contributors

- Juan Denis (@jhd3197) - Creator and maintainer

## License

MIT License - see LICENSE file for details
