"""
Example 1: Basic Composition Creation
======================================
This example demonstrates how to create a simple After Effects composition
with basic settings.

This tests:
- Client initialization
- Basic composition creation
- Timeline setup
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 1: Basic Composition Creation")
    print("="*60)

    # Initialize the client
    client = Client()
    print("✓ Client initialized")

    # Create a simple configuration
    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "BasicComposition",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 10,  # 10 seconds
            "output_file": "basic_output.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": False,  # Set to True to render
            "debug": True,  # Set to False for production
            "resources": []
        },
        "timeline": [
            {
                "name": "intro",
                "duration": 5,
                "startTime": 0,
                "template_comp": "IntroTemplate",
                "reverse": False,
                "custom_actions": []
            },
            {
                "name": "outro",
                "duration": 5,
                "startTime": 5,
                "template_comp": "OutroTemplate",
                "reverse": False,
                "custom_actions": []
            }
        ]
    }

    # Save configuration to file
    config_file = "basic_composition_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nConfiguration details:")
    print(f"  - Composition: {config['project']['comp_name']}")
    print(f"  - Resolution: {config['project']['comp_width']}x{config['project']['comp_height']}")
    print(f"  - FPS: {config['project']['comp_fps']}")
    print(f"  - Duration: {config['project']['comp_end_time']} seconds")
    print(f"  - Scenes: {len(config['timeline'])}")

    print("\n" + "="*60)
    print("Next steps:")
    print("1. Update 'project_file' path to your AE project template")
    print("2. Ensure template compositions exist in your project")
    print("3. Run: python run.py basic_composition_config.json")
    print("="*60)

    # Note: Uncomment to run automation (requires AE to be installed and configured)
    # client.startBot(config_file)

if __name__ == "__main__":
    main()
