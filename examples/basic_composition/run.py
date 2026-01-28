#!/usr/bin/env python3
"""
Basic Composition - Automation Runner
======================================
Runs the automation workflow using the basic composition template.

This demonstrates:
- Client initialization
- Basic timeline creation
- Simple scene sequencing
- Text property updates
"""

import os
import sys
import time

import template

from ae_automation import Client

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    import codecs

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


def run_automation():
    """Run the basic composition automation"""

    start_total_time = time.time()
    template_time = 0

    print("\n" + "=" * 70)
    print("Running Basic Composition Automation")
    print("=" * 70 + "\n")

    # Check if template exists
    # Ensure output directory exists first
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Check if template exists inside output folder
    template_path = os.path.join(output_dir, "basic_template.aep")

    if not os.path.exists(template_path):
        print("⚠ Template not found. Creating it now...")
        start_template_time = time.time()
        try:
            # Pass path to create_template (create_template works with absolute paths)
            template.create_template(template_path)
            template_time = time.time() - start_template_time
            print(f"✓ Template created in {template_time:.2f} seconds")
        except Exception as e:
            print(f"❌ Failed to create template: {e}")
            sys.exit(1)
    else:
        print(f"✓ Template found: {template_path}")

    print()

    # Initialize client
    client = Client()

    # Define the automation configuration
    config = {
        "project": {
            "project_file": ".\\basic_template.aep",
            "comp_name": "FinalComposition",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 10,  # 10 seconds total
            "output_file": "basic_output.mp4",
            "output_dir": ".",  # Config is in output folder, so this is current dir
            "renderComp": True,  # Set to True to render the final video
            "debug": False,
            "resources": [],
        },
        "timeline": [
            {
                "name": "intro",
                "duration": 5,
                "startTime": 0,
                "template_comp": "IntroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "IntroTemplate",
                        "layer_name": "MainTitle",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "My Amazing Video",
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "IntroTemplate",
                        "layer_name": "Subtitle",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Created with AE Automation",
                    },
                ],
            },
            {
                "name": "outro",
                "duration": 5,
                "startTime": 5,
                "template_comp": "OutroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "OutroTemplate",
                        "layer_name": "ClosingText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "See You Next Time!",
                    }
                ],
            },
        ],
    }

    print("Configuration:")
    print(f"  - Composition: {config['project']['comp_name']}")
    print(f"  - Duration: {config['project']['comp_end_time']} seconds")
    print(f"  - Scenes: {len(config['timeline'])}")
    print(f"  - Render: {'Yes' if config['project']['renderComp'] else 'No'}")
    print()

    # Create output directory
    os.makedirs(config["project"]["output_dir"], exist_ok=True)

    print("=" * 70)
    print("Starting Automation...")
    print("=" * 70 + "\n")

    # Run the automation
    try:
        # Save config to file (startBot expects a file path, not a dict)
        import json

        config_path = os.path.join(output_dir, "automation_config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Config saved to: {config_path}")
        print()

        start_automation_time = time.time()

        # Start the automation (pass file path, not dict)
        client.startBot(config_path)

        end_automation_time = time.time()
        automation_time = end_automation_time - start_automation_time

        print("\n" + "=" * 70)
        print("✓ Automation Complete!")
        print("=" * 70 + "\n")

        if config["project"]["renderComp"]:
            print(f"Output video: {os.path.join(config['project']['output_dir'], config['project']['output_file'])}")

        print("\n" + "=" * 70)
        print("Performance Report")
        print("=" * 70)
        if template_time > 0:
            print(f"Template Creation: {template_time:.2f}s")
        print(f"Automation Run:    {automation_time:.2f}s")
        print(f"Total Time:        {(end_automation_time - start_total_time):.2f}s")
        print("=" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠ Automation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_automation()
