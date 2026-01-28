#!/usr/bin/env python3
"""
Video Editor Test
==================
Simple test script to launch the video editor.
"""

import os
import sys

# Add parent directory to path to import ae_automation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ae_automation import Client


def main():
    print("=" * 70)
    print("Video Editor Test")
    print("=" * 70)
    print()

    # Get or create a test project file
    test_project = os.path.join(os.path.dirname(__file__), "test_project.json")

    if not os.path.exists(test_project):
        print(f"Creating test project file: {test_project}")
        import json

        # Create a basic project structure
        test_data = {
            "project": {
                "project_file": "",  # User will fill this in
                "comp_name": "FinalComposition",
                "width": 1920,
                "height": 1080,
                "frameRate": 30,
                "duration": 60,
                "resources": [],
            },
            "timeline": [
                {
                    "name": "Intro Scene",
                    "duration": 30,
                    "startTime": 0,
                    "template_comp": "",
                    "reverse": False,
                    "custom_actions": [],
                },
                {
                    "name": "Main Scene",
                    "duration": 30,
                    "startTime": 30,
                    "template_comp": "",
                    "reverse": False,
                    "custom_actions": [],
                },
            ],
        }

        with open(test_project, "w") as f:
            json.dump(test_data, f, indent=4)

        print(f"Created: {test_project}")
    else:
        print(f"Using existing project file: {test_project}")

    print()
    print("Starting Video Editor...")
    print("The editor will open in your browser at http://localhost:5000")
    print()
    print("IMPORTANT: Before rendering, set your .aep file path in Project Settings!")
    print()
    print("-" * 70)

    # Create the client instance
    ae = Client()

    # Run the video editor
    ae.runVideoEditor(test_project, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nVideo Editor stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
