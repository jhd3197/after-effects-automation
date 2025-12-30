"""
Example 5: Advanced Template System
=====================================
This example demonstrates the template system for reusable action sets.

This tests:
- Template definition
- Template variables
- Template reuse across scenes
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 5: Advanced Template System")
    print("="*60)

    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "TemplateDemo",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": True,
            "comp_start_time": "00:00:00",
            "comp_end_time": 30,
            "output_file": "template_demo.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": False,
            "debug": True,
            "resources": [
                {
                    "type": "image",
                    "name": "product1",
                    "path": "path/to/product1.png"
                },
                {
                    "type": "image",
                    "name": "product2",
                    "path": "path/to/product2.png"
                },
                {
                    "type": "image",
                    "name": "product3",
                    "path": "path/to/product3.png"
                }
            ]
        },
        "templates": {
            "productCard": [
                {
                    "change_type": "update_layer_property",
                    "comp_name": "ProductTemplate",
                    "layer_name": "ProductTitle",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{title}"
                },
                {
                    "change_type": "update_layer_property",
                    "comp_name": "ProductTemplate",
                    "layer_name": "ProductDescription",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{description}"
                },
                {
                    "change_type": "update_layer_property",
                    "comp_name": "ProductTemplate",
                    "layer_name": "ProductPrice",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{price}"
                },
                {
                    "change_type": "swap_items_by_index",
                    "layer_name": "{image}",
                    "comp_name": "ProductTemplate",
                    "layer_index": "4",
                    "fit_to_screen": True,
                    "fit_to_screen_width": False,
                    "fit_to_screen_height": False
                }
            ],
            "titleCard": [
                {
                    "change_type": "update_layer_property",
                    "comp_name": "TitleTemplate",
                    "layer_name": "MainTitle",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{title}"
                },
                {
                    "change_type": "update_layer_property",
                    "comp_name": "TitleTemplate",
                    "layer_name": "Subtitle",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{subtitle}"
                }
            ]
        },
        "timeline": [
            {
                "name": "intro_title",
                "duration": 3,
                "startTime": 0,
                "template_comp": "TitleTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "titleCard",
                        "template_values": {
                            "title": "Product Showcase 2025",
                            "subtitle": "Innovation at its finest"
                        }
                    }
                ]
            },
            {
                "name": "product1_showcase",
                "duration": 8,
                "startTime": 3,
                "template_comp": "ProductTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "productCard",
                        "template_values": {
                            "title": "Premium Widget Pro",
                            "description": "The ultimate solution for professionals<br>High performance and reliability",
                            "price": "$199.99",
                            "image": "product1"
                        }
                    }
                ]
            },
            {
                "name": "product2_showcase",
                "duration": 8,
                "startTime": 11,
                "template_comp": "ProductTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "productCard",
                        "template_values": {
                            "title": "Smart Gadget Plus",
                            "description": "Cutting-edge technology<br>Intuitive and powerful",
                            "price": "$149.99",
                            "image": "product2"
                        }
                    }
                ]
            },
            {
                "name": "product3_showcase",
                "duration": 8,
                "startTime": 19,
                "template_comp": "ProductTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "productCard",
                        "template_values": {
                            "title": "Essential Kit Basic",
                            "description": "Everything you need to get started<br>Quality at an affordable price",
                            "price": "$79.99",
                            "image": "product3"
                        }
                    }
                ]
            },
            {
                "name": "outro_title",
                "duration": 3,
                "startTime": 27,
                "template_comp": "TitleTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "titleCard",
                        "template_values": {
                            "title": "Thank You",
                            "subtitle": "Visit our store today!"
                        }
                    }
                ]
            }
        ]
    }

    # Save configuration
    config_file = "advanced_templates_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nTemplate definitions:")
    for template_name, actions in config['templates'].items():
        print(f"  - {template_name}: {len(actions)} actions")

    print("\nTemplate usage in timeline:")
    for scene in config['timeline']:
        for action in scene['custom_actions']:
            if action['change_type'] == 'template':
                print(f"\n  {scene['name']}:")
                print(f"    Template: {action['template_name']}")
                print(f"    Values: {list(action['template_values'].keys())}")

    print("\n" + "="*60)
    print("Benefits of templates:")
    print("  - Reusable action sets")
    print("  - Consistent styling")
    print("  - Easy to maintain")
    print("  - Reduce configuration redundancy")
    print("="*60)

if __name__ == "__main__":
    main()
