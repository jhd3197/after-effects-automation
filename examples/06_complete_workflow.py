"""
Example 6: Complete Production Workflow
=========================================
This is a comprehensive example showing a complete video production workflow
combining all features.

This tests:
- All major features combined
- Complex timeline
- Multiple resource types
- Templates
- Custom actions
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 6: Complete Production Workflow")
    print("="*60)

    # This represents a real-world video production scenario
    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "CompleteProduction",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": False,
            "comp_start_time": "00:00:00",
            "comp_end_time": 60,  # 1 minute video
            "output_file": "complete_production.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": True,  # Enable rendering
            "debug": False,  # Production mode
            "resources": [
                {
                    "type": "audio",
                    "name": "intro_music",
                    "path": "assets/audio/intro.mp3",
                    "duration": 10
                },
                {
                    "type": "audio",
                    "name": "background_music",
                    "path": "assets/audio/background.mp3",
                    "duration": 50
                },
                {
                    "type": "audio",
                    "name": "voiceover",
                    "path": "assets/audio/voiceover.mp3",
                    "duration": 45
                },
                {
                    "type": "image",
                    "name": "company_logo",
                    "path": "assets/images/logo.png"
                },
                {
                    "type": "image",
                    "name": "hero_image",
                    "path": "assets/images/hero.jpg"
                },
                {
                    "type": "image",
                    "name": "feature1",
                    "path": "assets/images/feature1.jpg"
                },
                {
                    "type": "image",
                    "name": "feature2",
                    "path": "assets/images/feature2.jpg"
                },
                {
                    "type": "image",
                    "name": "feature3",
                    "path": "assets/images/feature3.jpg"
                },
                {
                    "type": "video",
                    "name": "demo_video",
                    "path": "assets/video/demo.mp4",
                    "duration": 15
                }
            ]
        },
        "templates": {
            "brandedTitle": [
                {
                    "change_type": "update_layer_property",
                    "comp_name": "TitleTemplate",
                    "layer_name": "MainTitle",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{title}"
                },
                {
                    "change_type": "swap_items_by_index",
                    "layer_name": "company_logo",
                    "comp_name": "TitleTemplate",
                    "layer_index": "5",
                    "fit_to_screen": False,
                    "fit_to_screen_width": True,
                    "fit_to_screen_height": False
                }
            ],
            "featureHighlight": [
                {
                    "change_type": "update_layer_property",
                    "comp_name": "FeatureTemplate",
                    "layer_name": "FeatureTitle",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{feature_name}"
                },
                {
                    "change_type": "update_layer_property",
                    "comp_name": "FeatureTemplate",
                    "layer_name": "FeatureDescription",
                    "property_name": "Text.Source Text",
                    "property_type": "string",
                    "value": "{description}"
                },
                {
                    "change_type": "swap_items_by_index",
                    "layer_name": "{image}",
                    "comp_name": "FeatureTemplate",
                    "layer_index": "3",
                    "fit_to_screen": True,
                    "fit_to_screen_width": False,
                    "fit_to_screen_height": False
                }
            ]
        },
        "timeline": [
            {
                "name": "opening",
                "duration": 5,
                "startTime": 0,
                "template_comp": "BrandIntro",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "add_resource",
                        "resource_name": "intro_music",
                        "comp_name": "BrandIntro",
                        "startTime": "0",
                        "duration": "0"
                    },
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "company_logo",
                        "comp_name": "BrandIntro",
                        "layer_index": "2",
                        "fit_to_screen": False,
                        "fit_to_screen_width": True,
                        "fit_to_screen_height": False
                    }
                ]
            },
            {
                "name": "main_title",
                "duration": 5,
                "startTime": 5,
                "template_comp": "TitleTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "brandedTitle",
                        "template_values": {
                            "title": "Introducing Our Latest Innovation"
                        }
                    },
                    {
                        "change_type": "add_resource",
                        "resource_name": "background_music",
                        "comp_name": "TitleTemplate",
                        "startTime": "0",
                        "duration": "0"
                    }
                ]
            },
            {
                "name": "hero_section",
                "duration": 8,
                "startTime": 10,
                "template_comp": "HeroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "hero_image",
                        "comp_name": "HeroTemplate",
                        "layer_index": "2",
                        "fit_to_screen": True,
                        "fit_to_screen_width": False,
                        "fit_to_screen_height": False
                    },
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "HeroTemplate",
                        "layer_name": "HeroText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Transforming the way you work<br>with cutting-edge technology"
                    },
                    {
                        "change_type": "add_resource",
                        "resource_name": "voiceover",
                        "comp_name": "HeroTemplate",
                        "startTime": "0",
                        "duration": "0"
                    }
                ]
            },
            {
                "name": "feature1_section",
                "duration": 10,
                "startTime": 18,
                "template_comp": "FeatureTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "featureHighlight",
                        "template_values": {
                            "feature_name": "Advanced Analytics",
                            "description": "Real-time insights and data visualization<br>Make informed decisions faster",
                            "image": "feature1"
                        }
                    }
                ]
            },
            {
                "name": "feature2_section",
                "duration": 10,
                "startTime": 28,
                "template_comp": "FeatureTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "featureHighlight",
                        "template_values": {
                            "feature_name": "Cloud Integration",
                            "description": "Seamless sync across all devices<br>Work from anywhere, anytime",
                            "image": "feature2"
                        }
                    }
                ]
            },
            {
                "name": "feature3_section",
                "duration": 10,
                "startTime": 38,
                "template_comp": "FeatureTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "template",
                        "template_name": "featureHighlight",
                        "template_values": {
                            "feature_name": "Smart Automation",
                            "description": "AI-powered workflows<br>Save time and boost productivity",
                            "image": "feature3"
                        }
                    }
                ]
            },
            {
                "name": "call_to_action",
                "duration": 7,
                "startTime": 48,
                "template_comp": "CTATemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "CTATemplate",
                        "layer_name": "CTAText",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Start Your Free Trial Today<br>www.yourcompany.com"
                    },
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "company_logo",
                        "comp_name": "CTATemplate",
                        "layer_index": "4",
                        "fit_to_screen": False,
                        "fit_to_screen_width": True,
                        "fit_to_screen_height": False
                    }
                ]
            },
            {
                "name": "closing",
                "duration": 5,
                "startTime": 55,
                "template_comp": "BrandOutro",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "swap_items_by_index",
                        "layer_name": "company_logo",
                        "comp_name": "BrandOutro",
                        "layer_index": "2",
                        "fit_to_screen": False,
                        "fit_to_screen_width": True,
                        "fit_to_screen_height": False
                    }
                ]
            }
        ]
    }

    # Save configuration
    config_file = "complete_workflow_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nProduction Summary:")
    print(f"  Duration: {config['project']['comp_end_time']} seconds")
    print(f"  Scenes: {len(config['timeline'])}")
    print(f"  Resources: {len(config['project']['resources'])}")
    print(f"  Templates: {len(config.get('templates', {}))}")

    print("\n  Scene breakdown:")
    for scene in config['timeline']:
        print(f"    {scene['startTime']:2}s - {scene['name']}")

    print("\n" + "="*60)
    print("This example demonstrates:")
    print("  ✓ Complete video production workflow")
    print("  ✓ Multiple resource types (audio, image, video)")
    print("  ✓ Reusable templates")
    print("  ✓ Custom actions")
    print("  ✓ Precise timing control")
    print("  ✓ Professional structure")
    print("\nTo use this example:")
    print("  1. Update all file paths to match your assets")
    print("  2. Ensure template compositions exist in AE project")
    print("  3. Set debug=False and renderComp=True for production")
    print("  4. Run: python run.py complete_workflow_config.json")
    print("="*60)

if __name__ == "__main__":
    main()
