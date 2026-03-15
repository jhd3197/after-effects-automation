"""Cross-platform helpers for AE automation.

All Windows-specific operations go through these helpers so the rest of
the codebase doesn't need platform checks.
"""

from __future__ import annotations

import os
import subprocess

from ae_automation.settings import IS_MACOS, IS_WINDOWS

try:
    import psutil
except ImportError:
    psutil = None

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import pydirectinput
except ImportError:
    pydirectinput = None

try:
    from pywinauto.keyboard import send_keys
except ImportError:
    send_keys = None


def get_ae_process_name() -> str:
    """Return 'AfterFX.exe' on Windows, 'After Effects' on macOS."""
    if IS_WINDOWS:
        return "AfterFX.exe"
    return "After Effects"


def open_file(path: str) -> None:
    """Open a file with the OS default handler.

    Uses os.startfile on Windows, 'open' command on macOS,
    'xdg-open' on Linux.
    """
    if IS_WINDOWS:
        os.startfile(path)
    elif IS_MACOS:
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def kill_ae_process() -> None:
    """Kill all After Effects processes.

    Uses taskkill on Windows, killall on macOS/Linux.
    """
    if IS_WINDOWS:
        os.system('taskkill /F /FI "WINDOWTITLE eq Adobe After Effects*"')
    elif IS_MACOS:
        os.system("killall 'After Effects' 2>/dev/null")
    else:
        os.system("killall AfterFX 2>/dev/null")


def process_is_running(name: str) -> bool:
    """Cross-platform process check using psutil.

    Falls back to TASKLIST on Windows if psutil is not available.
    """
    if psutil is not None:
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    # Fallback: Windows TASKLIST (original behavior)
    if IS_WINDOWS:
        try:
            call = "TASKLIST", "/FI", f"imagename eq {name}"
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split("\r\n")[-1]
            return last_line.lower().startswith(name.lower())
        except Exception:
            return False

    # Fallback: Unix pgrep
    try:
        result = subprocess.run(
            ["pgrep", "-i", name],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_ae_executable(ae_folder: str) -> str:
    """Return full path to After Effects executable.

    On Windows: ae_folder/AfterFX.exe
    On macOS:   ae_folder/After Effects (or the .app binary inside)
    """
    if IS_WINDOWS:
        return os.path.join(ae_folder, "AfterFX.exe")
    elif IS_MACOS:
        # macOS AE lives inside an .app bundle
        app_binary = os.path.join(
            ae_folder, "Adobe After Effects.app", "Contents", "MacOS", "After Effects"
        )
        if os.path.isfile(app_binary):
            return app_binary
        # Fallback: direct binary in folder
        return os.path.join(ae_folder, "After Effects")
    return os.path.join(ae_folder, "AfterFX")


def hotkey(*keys: str) -> None:
    """Send keyboard shortcut, translating ctrl to cmd on macOS.

    Uses pyautogui if available.

    Args:
        *keys: Key names (e.g. "ctrl", "alt", "s"). On macOS, "ctrl"
               is automatically translated to "command".
    """
    translated = []
    for key in keys:
        if IS_MACOS and key.lower() == "ctrl":
            translated.append("command")
        else:
            translated.append(key)

    if pyautogui is not None:
        pyautogui.hotkey(*translated)
    else:
        raise RuntimeError(
            "pyautogui is not installed. Install it with: pip install pyautogui"
        )


def press_key(key: str) -> None:
    """Send a single key press. Handles cross-platform key names.

    On Windows with pywinauto available, uses send_keys for special keys.
    Otherwise falls back to pyautogui.

    Args:
        key: Key name — 'delete', 'enter', 'space', etc.
    """
    key_lower = key.lower()

    # Map normalized names to pywinauto send_keys format
    _pywinauto_map = {
        "delete": "{DEL}",
        "del": "{DEL}",
        "enter": "{ENTER}",
        "return": "{ENTER}",
        "space": " ",
        "tab": "{TAB}",
        "escape": "{ESC}",
        "esc": "{ESC}",
        "backspace": "{BACKSPACE}",
    }

    # Map normalized names to pyautogui format
    _pyautogui_map = {
        "delete": "delete",
        "del": "delete",
        "enter": "enter",
        "return": "enter",
        "space": "space",
        "tab": "tab",
        "escape": "escape",
        "esc": "escape",
        "backspace": "backspace",
    }

    # On Windows, prefer pywinauto send_keys for DEL/ENTER (original behavior)
    if IS_WINDOWS and send_keys is not None and key_lower in _pywinauto_map:
        send_keys(_pywinauto_map[key_lower])
        return

    # Fallback / macOS / Linux: use pyautogui
    if pyautogui is not None:
        resolved = _pyautogui_map.get(key_lower, key_lower)
        pyautogui.press(resolved)
        return

    raise RuntimeError(
        "No keyboard automation library available. "
        "Install pyautogui: pip install pyautogui"
    )


def save_project_hotkey() -> None:
    """Save the current AE project via keyboard shortcut.

    Ctrl+S on Windows, Cmd+S on macOS.
    """
    hotkey("ctrl", "s")
