# Process Management Guide

Understanding how After Effects Automation manages the After Effects process lifecycle.

## Overview

Intelligent process management is one of the key things that separates a unified automation platform from a collection of standalone scripts. Rather than assuming After Effects is already running and correctly configured, the platform handles the full process lifecycle automatically.

The automation system includes sophisticated process management to handle:
- **Process Detection** - Find and monitor After Effects
- **Window Waiting** - Wait for UI to be ready
- **Responsiveness Checks** - Ensure AE can accept commands
- **Crash Handling** - Recover from crashes and dialogs
- **Script Execution** - Safe script running with completion tracking

## Architecture

### ProcessManagerMixin

The core process management is implemented in `ae_automation/mixins/processManager.py` and composed into the unified `Client` class alongside the other mixins (afterEffect, bot, templateGenerator, etc.):

```python
from ae_automation import Client

client = Client()
client.ensure_after_effects_running()  # Handles everything automatically
```

## Key Features

### 1. Process Detection

**Wait for Process to Start**

```python
process = client.wait_for_process("AfterFX.exe", timeout=30)
```

- Monitors system processes using `psutil`
- Returns process object with PID when found
- Configurable timeout (default: 30 seconds)
- Handles access denied and missing process errors

**Use Case:** Ensure After Effects has launched before attempting window detection.

---

### 2. Window Detection

**Wait for Main Window**

```python
ready = client.wait_for_window("Adobe After Effects", timeout=60)
```

- Uses `pywinauto` for primary detection
- Falls back to `pygetwindow` if needed
- Waits for UI initialization (3 second grace period)
- Detects Home screen, project windows, etc.

**Use Case:** Confirm UI is visible before sending automation commands.

---

### 3. Responsiveness Testing

**Check if AE Can Execute Scripts**

```python
responsive = client.is_after_effects_responsive(max_retries=5)
```

**How it works:**
1. Writes a minimal test script: `app.project ? 'ready' : 'no project';`
2. Executes via `AfterFX.exe -s` command
3. Waits for completion (10 second timeout)
4. Retries up to 5 times with 3 second delays
5. Returns `True` if responsive

**Use Case:** Verify AE can accept automation commands before running complex scripts.

---

### 4. Crash Dialog Handling

**Auto-Dismiss Crash/Safe Mode Dialogs**

```python
client.handle_crash_dialog()
```

**What it does:**
- Sends `SPACE` key to dismiss common dialogs
- Handles "Crash Repair Options"
- Handles "Start in Safe Mode" prompts
- Called automatically during startup

**Use Case:** Prevent automation from stalling on crash recovery dialogs.

---

### 5. Comprehensive Startup

**All-in-One Ready Check**

```python
ready = client.wait_for_after_effects_ready(timeout=120)
```

**Complete startup sequence:**

```
1. Wait for Process (30s timeout)
   ↓
2. Handle Crash Dialog (initial check)
   ↓
3. Wait for Window (remaining time)
   ↓
4. Wait for Plugins (5s initialization)
   ↓
5. Check Responsiveness (3 retries)
   ↓
6. Final Crash Dialog Check (if needed)
   ↓
✓ After Effects Ready!
```

**Use Case:** Most reliable way to ensure AE is fully loaded and ready.

---

### 6. Ensure Running

**Start AE if Needed, Wait if Already Running**

```python
client.ensure_after_effects_running(
    project_file="path/to/project.aep",
    timeout=120
)
```

**Logic:**
1. Check if `AfterFX.exe` is already running
2. If running: Skip to readiness check
3. If not running: Launch with optional project file
4. Wait for complete startup
5. Return `True` when ready

**Use Case:** Robust automation that works whether AE is running or not.

---

### 7. Safe Script Execution

**Execute Script with Auto-Wait**

```python
client.safe_script_execution(
    "create_comp.jsx",
    replacements={"{{name}}": "MyComp"},
    wait_time=3
)
```

**Benefits:**
- Automatic waiting after execution
- Template replacement support
- Configurable wait time
- Prevents race conditions

**Use Case:** Run scripts with confidence that they complete before next action.

---

## Diagnostic Tools

### Test Script Execution

```python
client.test_script_execution()
```

**Shows alert dialog in AE to confirm scripts work.**

Expected output:
```
Testing Script Execution
========================
Running test script...
(You should see an alert dialog in After Effects)

✓ Test script sent to After Effects

⚠ IMPORTANT: Did you see an alert dialog in After Effects?
  - If YES: Scripts are working! ✓
  - If NO: Scripts are NOT executing - check preferences
```

---

### Check Scripting Settings

```python
client.check_scripting_settings()
```

**Shows detailed alert with current settings.**

Displays in AE:
- Scripting enabled status
- Network access permissions
- Current preferences

---

### Test Composition Creation

```python
client.test_composition_creation()
```

**Creates debug composition with progress alerts.**

Creates: `DEBUG_TEST_COMP` (1920x1080, 10s, 29.97fps)

**Shows multiple alerts:**
1. "Starting composition creation..."
2. "Composition created successfully"
3. Progress status

---

### Full Diagnostic Suite

```python
client.run_full_diagnostic()
```

**Complete system test:**

1. ✅ Check if AE is running
2. ✅ Verify window detection works
3. ✅ Test script execution
4. ✅ Check scripting settings
5. ✅ Test composition creation
6. 📋 Display comprehensive recommendations

**Use Case:** Troubleshoot automation issues systematically.

---

## Common Patterns

### Pattern 1: Start Fresh

```python
# Ensure AE is running and ready
client.ensure_after_effects_running(timeout=120)

# Run your automation
client.runScript("my_automation.jsx")
```

### Pattern 2: Check Before Running

```python
# Check if responsive first
if client.is_after_effects_responsive():
    client.safe_script_execution("my_script.jsx")
else:
    print("AE is not responding, waiting...")
    client.wait_for_after_effects_ready()
```

### Pattern 3: Diagnostic First

```python
# Run diagnostics to verify setup
client.run_full_diagnostic()

# Then proceed with automation
client.ensure_after_effects_running()
```

---

## Timing Considerations

### Recommended Timeouts

| Operation | Default | Recommended Range |
|-----------|---------|-------------------|
| Process Detection | 30s | 20-45s |
| Window Waiting | 60s | 45-90s |
| Responsiveness | 10s/attempt | 5-15s |
| Full Startup | 120s | 90-180s |
| Script Execution | 3s | 1-10s |

### Factors Affecting Timing

**Slower startup:**
- First launch after install
- Many plugins installed
- Low system resources
- Opening large projects
- Crash recovery mode

**Faster startup:**
- AE already running
- Minimal plugins
- Modern hardware
- Small/no project file
- Recent launch

---

## Troubleshooting

### Process Not Detected

**Problem:** `wait_for_process` returns `None`

**Solutions:**
1. Verify AE is installed: Check `AFTER_EFFECT_FOLDER` in `.env`
2. Increase timeout: `wait_for_process(timeout=60)`
3. Check process name: Should be `AfterFX.exe` (Windows)
4. Run as Administrator: May need elevated permissions

### Window Not Found

**Problem:** `wait_for_window` returns `False`

**Solutions:**
1. Increase timeout: `wait_for_window(timeout=120)`
2. Check if Home screen is blocking
3. Verify no crash dialogs are present
4. Try alternate detection with `pygetwindow`

### Not Responsive

**Problem:** `is_after_effects_responsive` returns `False`

**Solutions:**
1. **Enable scripting** in Edit > Preferences > Scripting & Expressions
2. Check "Allow Scripts to Write Files and Access Network"
3. Restart After Effects
4. Increase retry count: `is_after_effects_responsive(max_retries=10)`
5. Check `CACHE_FOLDER` is writable

### Scripts Don't Execute

**Problem:** Scripts send but nothing happens

**Checklist:**
1. ✅ Scripting enabled in preferences?
2. ✅ Startup script installed? (Window > Info should show message)
3. ✅ After Effects restarted after enabling?
4. ✅ No error dialogs in AE?
5. ✅ Antivirus not blocking?

**Test:**
```python
client.test_script_execution()  # Should show alert in AE
```

---

## Best Practices

### 1. Always Use ensure_after_effects_running

✅ **Good:**
```python
client.ensure_after_effects_running()
client.runScript("automation.jsx")
```

❌ **Bad:**
```python
# Assumes AE is already running
client.runScript("automation.jsx")  # May fail!
```

### 2. Handle Timeouts Gracefully

✅ **Good:**
```python
if client.ensure_after_effects_running(timeout=120):
    # Proceed with automation
    client.runScript("script.jsx")
else:
    print("Failed to start After Effects")
    # Handle error appropriately
```

### 3. Use Safe Script Execution

✅ **Good:**
```python
client.safe_script_execution("script.jsx", wait_time=5)
```

❌ **Bad:**
```python
client.runScript("script.jsx")
# Immediately run next script - may cause issues!
client.runScript("next_script.jsx")
```

### 4. Run Diagnostics When Troubleshooting

✅ **Good:**
```python
# Something's wrong? Run diagnostics first
client.run_full_diagnostic()
```

---

## Advanced Usage

### Custom Process Management

```python
# Override default process manager behavior
class CustomProcessManager(ProcessManagerMixin):
    def custom_startup_sequence(self):
        """Custom startup with extra checks"""
        # Start AE
        self.ensure_after_effects_running()

        # Custom verification
        if not self.verify_plugins_loaded():
            raise Exception("Required plugins not loaded")

        # Continue automation
        return True
```

### Monitoring Long Operations

```python
import time

def monitor_render(client, max_time=3600):
    """Monitor a long render operation"""
    start = time.time()

    while time.time() - start < max_time:
        if client.is_after_effects_responsive():
            print("✓ AE still responsive")
        else:
            print("⚠ AE not responding - may be rendering")

        time.sleep(30)  # Check every 30 seconds
```

---

## Architecture Diagram

```
Automation Script
       ↓
┌──────────────────────┐
│ ensure_ae_running()  │
└──────────────────────┘
       ↓
┌──────────────────────┐
│ wait_for_process()   │ ← psutil monitoring
└──────────────────────┘
       ↓
┌──────────────────────┐
│ handle_crash_dialog()│ ← pyautogui SPACE
└──────────────────────┘
       ↓
┌──────────────────────┐
│ wait_for_window()    │ ← pywinauto/pygetwindow
└──────────────────────┘
       ↓
┌──────────────────────┐
│ Wait for plugins     │ ← 5 second delay
└──────────────────────┘
       ↓
┌──────────────────────┐
│ is_ae_responsive()   │ ← Test script execution
└──────────────────────┘
       ↓
┌──────────────────────┐
│ ✓ Ready for Scripts  │
└──────────────────────┘
```

---

## Related Documentation

- [Installation Guide](INSTALLATION.md) - Setup requirements
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [CLI Guide](CLI_GUIDE.md) - Command-line diagnostics
- [Quick Start](QUICK_START.md) - Get started quickly

---

## Support

**Issues with process management?**

1. Run diagnostics: `ae-automation diagnose`
2. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Report issues: [GitHub Issues](https://github.com/jhd3197/after-effects-automation/issues)
