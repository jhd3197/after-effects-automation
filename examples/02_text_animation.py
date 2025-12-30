"""
Example 2: Text Animation
==========================
This example shows how to update text layers in After Effects compositions.

This tests:
- Text property updates
- Layer property manipulation
- Multiple custom actions
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 2: Text Animation")
    print("="*60)

    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "TextAnimation",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 15,
            "output_file": "text_animation.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": False,
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
                        "value": "Welcome to After Effects<br>Automation"
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "TitleTemplate",
                        "layer_name": "Subtitle",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Powered by Python"
                    }
                ]
            },
            {
                "name": "content_scene",
                "duration": 10,
                "startTime": 5,
                "template_comp": "ContentTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "ContentTemplate",
                        "layer_name": "ContentText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "• Automate video production<br>• Batch process compositions<br>• Programmatic control<br>• Save time and effort"
                    }
                ]
            }
        ]
    }

    # Save configuration
    config_file = "text_animation_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nText layers configured:")
    for scene in config['timeline']:
        print(f"\n  Scene: {scene['name']}")
        for action in scene['custom_actions']:
            if action['change_type'] == 'update_layer_property':
                print(f"    - Layer: {action['layer_name']}")
                print(f"      Text: {action['value'][:50]}...")

    print("\n" + "="*60)
    print("Note: Update layer names to match your template")
    print("="*60)

if __name__ == "__main__":
    main()
