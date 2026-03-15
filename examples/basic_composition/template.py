#!/usr/bin/env python3
"""
Basic Composition - Template Creator
=====================================
Creates an After Effects template with basic compositions for the automation.

This template includes:
- IntroTemplate: Simple intro with title text
- OutroTemplate: Simple outro with closing text
"""

import os
import sys

from ae_automation import Client

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    import codecs

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


def create_template(output_path=None):
    """Create the basic composition template"""

    print("\n" + "=" * 70)
    print("Creating Basic Composition Template")
    print("=" * 70 + "\n")

    # Initialize client
    client = Client()

    # Define template configuration
    template_config = {
        "name": "Basic Composition Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 10,
        "compositions": [
            {
                "name": "IntroTemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.15],  # Dark blue-gray
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "MainTitle",
                        "text": "Welcome to My Video",
                        "x": 960,
                        "y": 540,
                        "fontSize": 96,
                    },
                    {
                        "type": "text",
                        "name": "Subtitle",
                        "text": "Let's get started",
                        "x": 960,
                        "y": 700,
                        "fontSize": 48,
                    },
                ],
            },
            {
                "name": "OutroTemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.15, 0.1, 0.1],  # Dark red-gray
                        "width": 1920,
                        "height": 1080,
                    },
                    {
                        "type": "text",
                        "name": "ClosingText",
                        "text": "Thanks for Watching!",
                        "x": 960,
                        "y": 540,
                        "fontSize": 84,
                    },
                ],
            },
        ],
    }

    # Output path
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "basic_template.aep")

    # Build the template
    client.buildTemplate(template_config, output_path)

    print("\n" + "=" * 70)
    print("✓ Template Created Successfully!")
    print("=" * 70 + "\n")
    print(f"Template file: {os.path.abspath(output_path)}")
    print()
    print("Template includes:")
    print("  - IntroTemplate: Intro with title and subtitle")
    print("  - OutroTemplate: Outro with closing text")
    print()
    print("Next steps:")
    print("  1. Open basic_template.aep in After Effects to customize")
    print("  2. Run the automation: python run.py")
    print()

    return output_path


if __name__ == "__main__":
    create_template()
