# Troubleshooting Guide

Common issues and solutions for After Effects Automation.

## Quick Fixes

### After Effects Won't Start

**Symptom:** Automation fails to launch After Effects

**Solutions:**

1. **Check .env path:**
   ```bash
   # Open .env and verify:
   AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2025/Support Files
   ```

2. **Test manually:**
   ```bash
   # Try opening AE directly
   start "" "C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\AfterFX.exe"
   ```

3. **Check version:**
   - Ensure path matches your installed AE version (2024, 2025, etc.)

### Scripts Not Executing

**Symptom:** AE opens but scripts don't run

**Solutions:**

1. **Enable scripting:**
   - Edit > Preferences > Scripting & Expressions
   - Check "Allow Scripts to Write Files and Access Network"
   - Restart After Effects

2. **Reinstall startup script:**
   ```bash
   python install_ae_runner.py
   ```

3. **Verify startup script installed:**
   - Windows: `%APPDATA%\Adobe\After Effects\<version>\Scripts\Startup\ae_command_runner.jsx`
   - Check AE's Window > Info panel for "AE Command Runner initialized"

### Composition Not Found Error

**Symptom:** `aerender ERROR: No comp was found with the given name`

**Solutions:**

1. **Check composition name (case-sensitive):**
   ```bash
   # Wrong
   python render.py --comp "finalcomposition"

   # Right
   python render.py --comp "FinalComposition"
   ```

2. **Verify file type:**
   - `basic_template.aep` → Use `IntroTemplate` or `OutroTemplate`
   - `ae_automation.aep` → Use `FinalComposition`

3. **Open .aep in AE to check available compositions**

### Empty/Black Video Output

**Symptom:** Video renders but shows only black frames

**Causes & Fixes:**

1. **Batch system bug (FIXED):**
   - Update to latest version: `pip install --upgrade after-effects-automation`

2. **Missing scenes in timeline:**
   - Check that automation ran completely
   - Look for error messages in output

3. **Composition actually empty:**
   - Open .aep in After Effects
   - Check if FinalComposition contains layers

### Python Module Not Found

**Symptom:** `ModuleNotFoundError: No module named 'ae_automation'`

**Solutions:**

```bash
# Reinstall package
pip uninstall after-effects-automation
pip install after-effects-automation

# Or for development
cd after-effects-automation
pip install -e .
```

### Permission Denied Errors

**Windows:**
```bash
# Run as Administrator
Right-click PowerShell > Run as Administrator
```

**macOS:**
```bash
# Grant Full Disk Access to Terminal
System Preferences > Security & Privacy > Privacy > Full Disk Access
```

### Render Fails Immediately

**Symptom:** aerender exits with error code

**Solutions:**

1. **Check aerender path:**
   ```bash
   # Test aerender manually
   "C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\aerender.exe" -version
   ```

2. **Verify output directory exists and is writable:**
   ```bash
   mkdir output
   ```

3. **Check AE license:**
   - Ensure After Effects is properly licensed
   - Try opening AE manually first

## Error Messages

### "Process with PID X has been terminated"

**Normal behavior** - This is expected. The automation kills the AE process after setup to ensure clean rendering with aerender.

### "Waiting for AfterFX.exe to start..."

**Hangs here:**
- Check Task Manager - is AE actually starting?
- Try manually: `start "" "path\to\AfterFX.exe"`
- Antivirus might be blocking

### "Template not found"

**For examples:**
```bash
# Run template.py first
cd examples/basic_composition
python template.py

# Then run automation
python run.py
```

### "UnicodeEncodeError: 'charmap' codec"

**Windows console encoding issue:**
```bash
# Use UTF-8 encoding
set PYTHONIOENCODING=utf-8
python run.py
```

Or the fix is already applied in latest version.

## Performance Issues

### Slow Rendering

**Normal render times:**
- Simple comp (5s @ 1080p): 2-10 seconds
- Complex effects (10s @ 1080p): 10-30 seconds
- Production (60s @ 4K): 2-5 minutes

**Speed up rendering:**
1. Close other applications
2. Use SSD for cache and output
3. Reduce composition quality during testing
4. Disable effects temporarily

### High Memory Usage

**Normal:** AE + Python can use 2-4GB RAM

**If excessive:**
- Close After Effects between automation runs
- Clear AE cache: Edit > Purge > All Memory & Disk Cache
- Reduce composition resolution for testing

## Platform-Specific Issues

### Windows

**Antivirus Blocking:**
- Add Python and AE folders to exclusions
- Temporarily disable real-time protection for testing

**Path Issues:**
- Use forward slashes: `C:/Program Files/Adobe/...`
- Or escape backslashes: `C:\\Program Files\\Adobe\\...`

### macOS

**Gatekeeper:**
- System Preferences > Security & Privacy
- Allow apps from identified developers

**Permissions:**
- Terminal needs Full Disk Access
- AE needs Accessibility permissions

### Linux (Experimental)

**Wine Required:**
- After Effects runs via Wine (limited support)
- Community-maintained, may have issues

## Getting Help

### Before Posting an Issue

1. **Check this guide** - Most issues covered here
2. **Update to latest version:**
   ```bash
   pip install --upgrade after-effects-automation
   ```
3. **Test with basic example:**
   ```bash
   cd examples/basic_composition
   python run.py
   ```

### When Reporting Issues

Include:
- Python version: `python --version`
- Package version: `pip show after-effects-automation`
- AE version: e.g., "After Effects 2025 (v25.0)"
- OS: Windows 11, macOS 14, etc.
- Full error message and traceback
- Steps to reproduce

### Resources

- **GitHub Issues**: Report bugs and feature requests
- **Examples**: `examples/` folder for working code
- **Documentation**: All `.md` files in repo
- **Source Code**: Read the code for advanced usage

## Debug Mode

Enable verbose logging:

```python
# In your script
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs in:
- Console output
- AE's Info panel (Window > Info)
- Cache folder (if file logging enabled)

## Still Stuck?

1. **Read the examples** - Working code in `examples/`
2. **Check discussions** - Others may have same issue
3. **Ask on GitHub** - Create detailed issue
4. **Community Discord** - Real-time help (if available)

## Known Issues

### Batch System (FIXED in v0.0.4)

**Issue:** Videos rendering as black/empty
**Status:** Fixed
**Solution:** Update to latest version

### Unicode on Windows (FIXED)

**Issue:** Emoji/Unicode errors in console
**Status:** Fixed
**Solution:** Update examples or set `PYTHONIOENCODING=utf-8`

### Multiple AE Instances

**Issue:** Multiple AE windows open simultaneously
**Status:** By design - automation uses fresh instance
**Workaround:** Close other AE instances before running

## Contributing Fixes

Found a fix not listed here? Please contribute:

1. Fork the repo
2. Add fix to this file
3. Submit pull request
4. Help other users!
