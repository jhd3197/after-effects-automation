#!/usr/bin/env python3
"""
Install the AE Automation Chat CEP extension into After Effects.

Creates a symlink (or copies files) from this repo's extension folder
to the CEP extensions directory, and enables debug mode for unsigned extensions.

Usage:
    python install_extension.py          # Install with symlink
    python install_extension.py --copy   # Install by copying files
    python install_extension.py --remove # Remove the extension
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys

EXTENSION_ID = "com.aeautomation.chat"
SOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ae_automation", "extension")

# CEP versions to enable debug mode for
CEP_VERSIONS = ["10", "11", "12"]


def _get_cep_dir() -> str:
    """Get the platform-appropriate CEP extensions directory."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        return os.path.join(appdata, "Adobe", "CEP", "extensions")
    elif sys.platform == "darwin":
        return os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Adobe",
            "CEP",
            "extensions",
        )
    # Linux (experimental)
    return os.path.join(os.path.expanduser("~"), ".adobe", "CEP", "extensions")


CEP_DIR = _get_cep_dir()
TARGET_DIR = os.path.join(CEP_DIR, EXTENSION_ID)


def enable_debug_mode() -> None:
    """Set PlayerDebugMode=1 for unsigned extensions.

    On Windows: sets registry keys.
    On macOS: writes plist defaults.
    """
    if sys.platform == "win32":
        import winreg

        for ver in CEP_VERSIONS:
            key_path = rf"Software\Adobe\CSXS.{ver}"
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
                winreg.SetValueEx(key, "PlayerDebugMode", 0, winreg.REG_SZ, "1")
                winreg.CloseKey(key)
                print(f"  Enabled debug mode for CEP {ver}")
            except Exception as e:
                print(f"  Warning: Could not set CEP {ver} debug mode: {e}")

    elif sys.platform == "darwin":
        import subprocess

        for ver in CEP_VERSIONS:
            domain = f"com.adobe.CSXS.{ver}"
            try:
                subprocess.run(
                    ["defaults", "write", domain, "PlayerDebugMode", "1"],
                    check=True,
                    capture_output=True,
                )
                print(f"  Enabled debug mode for CEP {ver}")
            except Exception as e:
                print(f"  Warning: Could not set CEP {ver} debug mode: {e}")
    else:
        print("  Debug mode setup not supported on this platform.")
        print("  Manually set PlayerDebugMode=1 for your CEP version.")


def install_symlink() -> None:
    """Install extension via directory symlink."""
    os.makedirs(CEP_DIR, exist_ok=True)

    if os.path.exists(TARGET_DIR):
        if os.path.islink(TARGET_DIR) or os.path.isdir(TARGET_DIR):
            print(f"  Removing existing: {TARGET_DIR}")
            if os.path.islink(TARGET_DIR):
                os.remove(TARGET_DIR)
            else:
                shutil.rmtree(TARGET_DIR)

    try:
        os.symlink(SOURCE_DIR, TARGET_DIR, target_is_directory=True)
        print(f"  Symlinked: {TARGET_DIR} -> {SOURCE_DIR}")
    except OSError:
        print("  Symlink failed (may need admin). Falling back to copy...")
        install_copy()


def install_copy() -> None:
    """Install extension by copying files."""
    os.makedirs(CEP_DIR, exist_ok=True)

    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    shutil.copytree(SOURCE_DIR, TARGET_DIR)
    print(f"  Copied to: {TARGET_DIR}")


def remove() -> None:
    """Remove the installed extension."""
    if os.path.exists(TARGET_DIR):
        if os.path.islink(TARGET_DIR):
            os.remove(TARGET_DIR)
        else:
            shutil.rmtree(TARGET_DIR)
        print(f"  Removed: {TARGET_DIR}")
    else:
        print("  Extension not found — nothing to remove.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install AE Automation Chat extension")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of symlinking")
    parser.add_argument("--remove", action="store_true", help="Remove the extension")
    args = parser.parse_args()

    print("\nAE Automation Chat Extension Installer")
    print("=" * 40)
    print(f"Platform: {sys.platform}")

    if args.remove:
        print("\nRemoving extension...")
        remove()
        print("\nDone. Restart After Effects to apply.")
        return

    print(f"\nSource:  {SOURCE_DIR}")
    print(f"Target:  {TARGET_DIR}")

    # Step 1: Enable debug mode
    print("\nEnabling debug mode for unsigned extensions...")
    enable_debug_mode()

    # Step 2: Install
    print("\nInstalling extension...")
    if args.copy:
        install_copy()
    else:
        install_symlink()

    # Step 3: Check CSInterface.js
    cs_file = os.path.join(SOURCE_DIR, "client", "lib", "CSInterface.js")
    with open(cs_file, encoding="utf-8") as f:
        content = f.read()
    if "Minimal stub" in content:
        print("\n  Note: Using built-in CSInterface.js stub.")
        print("  This works inside AE (the CEP runtime provides the real one).")
        print("  The stub is only used for browser-based testing outside AE.")

    print("\nInstallation complete!")
    print("\nNext steps:")
    print("  1. Restart After Effects")
    print("  2. Go to Window > Extensions > AE Automation Chat")
    print("  3. Start the backend: ae-automation chat")
    print("  4. Start chatting!")
    print("\nDebug the panel at http://localhost:8089/ while AE is running.")


if __name__ == "__main__":
    main()
