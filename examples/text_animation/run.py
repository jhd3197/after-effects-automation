#!/usr/bin/env python3
"""
Text Animation - Automation Runner
===================================
Demonstrates various text manipulation techniques.

This shows:
- Updating multiple text layers
- Multi-line text with line breaks
- Dynamic text content from variables
- Text property updates
"""

import os
import sys
from ae_automation import Client


def run_automation():
    """Run the text animation automation"""

    print("\n" + "="*70)
    print("Running Text Animation Automation")
    print("="*70 + "\n")

    # Check if template exists
    template_path = os.path.join(os.path.dirname(__file__), "text_animation_template.aep")

    if not os.path.exists(template_path):
        print("❌ Template not found!")
        print(f"   Expected: {template_path}")
        print()
        print("Please create the template first:")
        print("  python template.py")
        print()
        sys.exit(1)

    print(f"✓ Template found: {template_path}")
    print()

    # Initialize client
    client = Client()

    # Define custom content
    video_title = "My Awesome Tutorial"
    video_subtitle = "Learn After Effects Automation"
    description_lines = [
        "• Easy to use Python API",
        "• Template-based workflow",
        "• Automated video production"
    ]

    # Define the automation configuration
    config = {
        "project": {
            "project_file": ".\\text_animation_template.aep",
            "comp_name": "TextAnimationDemo",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 15,
            "output_file": "text_animation_output.mp4",
            "output_dir": ".\\output",
            "renderComp": False,  # Set to True to render
            "debug": True,
            "resources": []
        },
        "timeline": [
            {
                "name": "title_scene",
                "duration": 5,
                "startTime": 0,
                "template_comp": "TitleTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "TitleTemplate",
                        "layer_name": "MainTitle",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": video_title
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "TitleTemplate",
                        "layer_name": "SubtitleText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": video_subtitle
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "TitleTemplate",
                        "layer_name": "SmallText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Episode 1"
                    }
                ]
            },
            {
                "name": "description_scene",
                "duration": 5,
                "startTime": 5,
                "template_comp": "DescriptionTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "DescriptionTemplate",
                        "layer_name": "Heading",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "What You'll Learn"
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "DescriptionTemplate",
                        "layer_name": "Description",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "<br>".join(description_lines)  # Multi-line text with HTML breaks
                    }
                ]
            },
            {
                "name": "credits_scene",
                "duration": 5,
                "startTime": 10,
                "template_comp": "CreditsTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "CreditsTemplate",
                        "layer_name": "Role1",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Created By"
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "CreditsTemplate",
                        "layer_name": "Name1",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Your Name Here"
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "CreditsTemplate",
                        "layer_name": "Role2",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Powered By"
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "CreditsTemplate",
                        "layer_name": "Name2",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "AE Automation"
                    }
                ]
            }
        ]
    }

    print("Configuration:")
    print(f"  - Title: {video_title}")
    print(f"  - Subtitle: {video_subtitle}")
    print(f"  - Duration: {config['project']['comp_end_time']} seconds")
    print(f"  - Scenes: {len(config['timeline'])}")
    print()

    # Create output directory
    os.makedirs(config['project']['output_dir'], exist_ok=True)

    print("="*70)
    print("Starting Automation...")
    print("="*70 + "\n")

    # Run the automation
    try:
        # Save config to file (startBot expects a file path, not a dict)
        import json
        config_path = os.path.join(os.path.dirname(__file__), "automation_config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Config saved to: {config_path}")
        print()

        # Start the automation (pass file path, not dict)
        client.startBot(config_path)

        print("\n" + "="*70)
        print("✓ Automation Complete!")
        print("="*70 + "\n")

        if config['project']['renderComp']:
            print(f"Output video: {os.path.join(config['project']['output_dir'], config['project']['output_file'])}")

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
