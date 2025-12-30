#!/usr/bin/env python3
"""
Install the After Effects Command Runner startup script
This script must be installed for ae-automation to work with running AE instances
"""

import os
import shutil
from ae_automation import settings

def install_startup_script():
    """Install the ae_command_runner.jsx to After Effects Startup folder"""

    print("=" * 70)
    print("After Effects Command Runner Installation")
    print("=" * 70)
    print()

    # Source file
    source_file = os.path.join(settings.JS_DIR, 'ae_command_runner.jsx')

    if not os.path.exists(source_file):
        print(f"ERROR: Source file not found: {source_file}")
        return False

    # Destination folder
    startup_folder = os.path.join(settings.AFTER_EFFECT_FOLDER, 'Scripts', 'Startup')

    if not os.path.exists(startup_folder):
        print(f"ERROR: After Effects Startup folder not found: {startup_folder}")
        print()
        print("Please update your .env file with the correct AFTER_EFFECT_FOLDER path")
        return False

    # Destination file
    dest_file = os.path.join(startup_folder, 'ae_command_runner.jsx')

    try:
        # Check if already installed
        if os.path.exists(dest_file):
            print(f"Command runner already installed at:")
            print(f"  {dest_file}")
            print()
            response = input("Reinstall? (y/n): ").strip().lower()
            if response != 'y':
                print("Installation cancelled")
                return True

        # Copy the file
        print(f"Installing command runner...")
        print(f"  From: {source_file}")
        print(f"  To:   {dest_file}")
        print()

        shutil.copy2(source_file, dest_file)

        print("✓ Installation successful!")
        print()
        print("=" * 70)
        print("IMPORTANT: Next Steps")
        print("=" * 70)
        print()
        print("1. RESTART After Effects (if it's currently running)")
        print("   The startup script only loads when After Effects starts")
        print()
        print("2. Check the Info panel in After Effects (Window > Info)")
        print("   You should see: 'AE Command Runner: Started successfully'")
        print()
        print("3. Test the automation:")
        print("   python test_file_communication.py")
        print()
        print("=" * 70)

        return True

    except PermissionError:
        print("ERROR: Permission denied!")
        print()
        print("The After Effects folder requires administrator privileges.")
        print("Please run this script as administrator:")
        print()
        print("  Right-click Command Prompt > Run as administrator")
        print("  Then run: python install_ae_runner.py")
        return False

    except Exception as e:
        print(f"ERROR: Installation failed: {e}")
        return False


if __name__ == '__main__':
    success = install_startup_script()
    exit(0 if success else 1)
