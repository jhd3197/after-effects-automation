"""
Example 3: Resource Management
================================
This example demonstrates importing and using resources (images, audio, video)
in After Effects compositions.

This tests:
- Resource importing (images, audio, video)
- Resource placement in timeline
- Swap items functionality
- Fit to screen options
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 3: Resource Management")
    print("="*60)

    # Note: Update these paths to actual media files
    assets_dir = "path/to/your/assets"

    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "ResourceDemo",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 20,
            "output_file": "resource_demo.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": False,
            "debug": True,
            "resources": [
                {
                    "type": "audio",
                    "name": "background_music",
                    "path": os.path.join(assets_dir, "music.mp3"),
                    "duration": 20
                },
                {
                    "type": "image",
                    "name": "logo",
                    "path": os.path.join(assets_dir, "logo.png")
                },
                {
                    "type": "image",
                    "name": "photo1",
                    "path": os.path.join(assets_dir, "photo1.jpg")
                },
                {
                    "type": "image",
                    "name": "photo2",
                    "path": os.path.join(assets_dir, "photo2.jpg")
                },
                {
                    "type": "video",
                    "name": "intro_video",
                    "path": os.path.join(assets_dir, "intro.mp4"),
                    "duration": 5
                }
            ]
        },
        "timeline": [
            {
                "name": "intro_with_logo",
                "duration": 5,
                "startTime": 0,
                "template_comp": "IntroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "logo",
                        "comp_name": "IntroTemplate",
                        "layer_index": "2",
                        "fit_to_screen": False,
                        "fit_to_screen_width": True,
                        "fit_to_screen_height": False
                    },
                    {
                        "change_type": "add_resource",
                        "resource_name": "background_music",
                        "comp_name": "IntroTemplate",
                        "startTime": "0",
                        "duration": "0"
                    }
                ]
            },
            {
                "name": "photo_slideshow",
                "duration": 10,
                "startTime": 5,
                "template_comp": "SlideTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "photo1",
                        "comp_name": "SlideTemplate",
                        "layer_index": "3",
                        "fit_to_screen": True,
                        "fit_to_screen_width": False,
                        "fit_to_screen_height": False
                    }
                ]
            },
            {
                "name": "second_photo",
                "duration": 5,
                "startTime": 15,
                "template_comp": "SlideTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "photo2",
                        "comp_name": "SlideTemplate",
                        "layer_index": "3",
                        "fit_to_screen": False,
                        "fit_to_screen_width": True,
                        "fit_to_screen_height": True
                    }
                ]
            }
        ]
    }

    # Save configuration
    config_file = "resource_management_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nResources configured:")
    for resource in config['project']['resources']:
        print(f"  - {resource['type']}: {resource['name']}")
        print(f"    Path: {resource['path']}")

    print("\n" + "="*60)
    print("Fit to screen options:")
    print("  - fit_to_screen: Fits both width and height")
    print("  - fit_to_screen_width: Fits to width only")
    print("  - fit_to_screen_height: Fits to height only")
    print("="*60)

if __name__ == "__main__":
    main()
