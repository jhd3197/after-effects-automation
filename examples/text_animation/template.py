#!/usr/bin/env python3
"""
Text Animation - Template Creator
==================================
Creates an After Effects template demonstrating various text manipulation features.

This template includes:
- TitleTemplate: Multiple text layers with different styles
- SubtitleTemplate: Multi-line text demonstration
- CreditTemplate: Scrolling credits layout
"""

import os

from ae_automation import Client


def create_template():
    """Create the text animation template"""

    print("\n" + "=" * 70)
    print("Creating Text Animation Template")
    print("=" * 70 + "\n")

    # Initialize client
    client = Client()

    # Define template configuration
    template_config = {
        "name": "Text Animation Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 15,
        "compositions": [
            {
                "name": "TitleTemplate",
                "duration": 5,
                "layers": [
                    {"type": "solid", "name": "Background", "color": [0.05, 0.05, 0.1], "width": 1920, "height": 1080},
                    {
                        "type": "text",
                        "name": "MainTitle",
                        "text": "Main Title Here",
                        "x": 960,
                        "y": 400,
                        "fontSize": 120,
                    },
                    {
                        "type": "text",
                        "name": "SubtitleText",
                        "text": "Subtitle text goes here",
                        "x": 960,
                        "y": 580,
                        "fontSize": 60,
                    },
                    {
                        "type": "text",
                        "name": "SmallText",
                        "text": "Additional info",
                        "x": 960,
                        "y": 720,
                        "fontSize": 36,
                    },
                ],
            },
            {
                "name": "DescriptionTemplate",
                "duration": 5,
                "layers": [
                    {"type": "solid", "name": "Background", "color": [0.95, 0.95, 0.97], "width": 1920, "height": 1080},
                    {"type": "text", "name": "Heading", "text": "Section Title", "x": 960, "y": 300, "fontSize": 84},
                    {
                        "type": "text",
                        "name": "Description",
                        "text": "Line 1\nLine 2\nLine 3",
                        "x": 960,
                        "y": 540,
                        "fontSize": 48,
                    },
                ],
            },
            {
                "name": "CreditsTemplate",
                "duration": 5,
                "layers": [
                    {"type": "solid", "name": "Background", "color": [0, 0, 0], "width": 1920, "height": 1080},
                    {"type": "text", "name": "Role1", "text": "Director", "x": 960, "y": 300, "fontSize": 48},
                    {"type": "text", "name": "Name1", "text": "John Doe", "x": 960, "y": 380, "fontSize": 64},
                    {"type": "text", "name": "Role2", "text": "Producer", "x": 960, "y": 550, "fontSize": 48},
                    {"type": "text", "name": "Name2", "text": "Jane Smith", "x": 960, "y": 630, "fontSize": 64},
                ],
            },
        ],
    }

    # Output path
    output_path = os.path.join(os.path.dirname(__file__), "text_animation_template.aep")

    # Build the template
    client.buildTemplate(template_config, output_path)

    print("\n" + "=" * 70)
    print("✓ Template Created Successfully!")
    print("=" * 70 + "\n")
    print(f"Template file: {os.path.abspath(output_path)}")
    print()
    print("Template includes:")
    print("  - TitleTemplate: Multiple text layers with different sizes")
    print("  - DescriptionTemplate: Multi-line text demonstration")
    print("  - CreditsTemplate: Credits layout with roles and names")
    print()
    print("Next steps:")
    print("  1. Open text_animation_template.aep in After Effects to customize")
    print("  2. Run the automation: python run.py")
    print()

    return output_path


if __name__ == "__main__":
    create_template()
