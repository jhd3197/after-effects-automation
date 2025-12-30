#!/usr/bin/env python3
"""
After Effects Template Generator
Generates .aep template files for the example configurations
"""

import os
import sys
import argparse
from ae_automation import Client


def generate_tutorial_template(output_path):
    """Generate template for tutorial videos"""
    print("\n" + "="*60)
    print("Generating Tutorial Video Template")
    print("="*60 + "\n")

    client = Client()

    template_config = {
        "name": "Tutorial Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 30,
        "compositions": [
            {
                "name": "IntroTemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.15],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "null",
                        "name": "PlaceholderLogo"
                    },
                    {
                        "type": "text",
                        "name": "TitleText",
                        "text": "Tutorial Title",
                        "x": 960,
                        "y": 540,
                        "fontSize": 96
                    }
                ]
            },
            {
                "name": "ContentTemplate",
                "duration": 20,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.95, 0.95, 0.95],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "ContentText",
                        "text": "Tutorial Steps",
                        "x": 960,
                        "y": 400,
                        "fontSize": 48
                    },
                    {
                        "type": "shape",
                        "name": "ContentBox",
                        "width": 1600,
                        "height": 800,
                        "color": [1, 1, 1]
                    }
                ]
            },
            {
                "name": "OutroTemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.15],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "OutroText",
                        "text": "Thanks for Watching!",
                        "x": 960,
                        "y": 540,
                        "fontSize": 72
                    }
                ]
            }
        ]
    }

    client.buildTemplate(template_config, output_path)
    return output_path


def generate_social_media_template(output_path):
    """Generate template for social media posts (vertical format)"""
    print("\n" + "="*60)
    print("Generating Social Media Template")
    print("="*60 + "\n")

    client = Client()

    template_config = {
        "name": "Social Media Template",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "duration": 15,
        "compositions": [
            {
                "name": "HookTemplate",
                "width": 1080,
                "height": 1920,
                "duration": 3,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.9, 0.1, 0.3],
                        "width": 1080,
                        "height": 1920
                    },
                    {
                        "type": "text",
                        "name": "HookText",
                        "text": "Wait for it...",
                        "x": 540,
                        "y": 960,
                        "fontSize": 96
                    }
                ]
            },
            {
                "name": "StoryTemplate",
                "width": 1080,
                "height": 1920,
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0, 0, 0],
                        "width": 1080,
                        "height": 1920
                    },
                    {
                        "type": "null",
                        "name": "ImagePlaceholder"
                    },
                    {
                        "type": "text",
                        "name": "MainText",
                        "text": "Your Message",
                        "x": 540,
                        "y": 1600,
                        "fontSize": 72
                    }
                ]
            },
            {
                "name": "CTATemplate",
                "width": 1080,
                "height": 1920,
                "duration": 3,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.1],
                        "width": 1080,
                        "height": 1920
                    },
                    {
                        "type": "null",
                        "name": "LogoPlaceholder"
                    },
                    {
                        "type": "text",
                        "name": "CTAText",
                        "text": "Shop Now",
                        "x": 540,
                        "y": 1200,
                        "fontSize": 84
                    }
                ]
            }
        ]
    }

    client.buildTemplate(template_config, output_path)
    return output_path


def generate_product_showcase_template(output_path):
    """Generate template for product showcase videos"""
    print("\n" + "="*60)
    print("Generating Product Showcase Template")
    print("="*60 + "\n")

    client = Client()

    template_config = {
        "name": "Product Showcase Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 45,
        "compositions": [
            {
                "name": "BrandIntro",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [1, 1, 1],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "null",
                        "name": "LogoPlaceholder"
                    },
                    {
                        "type": "null",
                        "name": "timeline"
                    }
                ]
            },
            {
                "name": "ProductTemplate",
                "duration": 12,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.95, 0.95, 0.97],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "shape",
                        "name": "ProductCard",
                        "width": 800,
                        "height": 900,
                        "color": [1, 1, 1]
                    },
                    {
                        "type": "null",
                        "name": "ProductImagePlaceholder"
                    },
                    {
                        "type": "text",
                        "name": "ProductName",
                        "text": "Product Name",
                        "x": 500,
                        "y": 200,
                        "fontSize": 64
                    },
                    {
                        "type": "text",
                        "name": "ProductFeatures",
                        "text": "Features",
                        "x": 500,
                        "y": 400,
                        "fontSize": 36
                    },
                    {
                        "type": "text",
                        "name": "ProductPrice",
                        "text": "$99",
                        "x": 500,
                        "y": 700,
                        "fontSize": 48
                    },
                    {
                        "type": "null",
                        "name": "timeline"
                    }
                ]
            },
            {
                "name": "CTATemplate",
                "duration": 4,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.2, 0.6, 0.9],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "CTAText",
                        "text": "Visit Our Website",
                        "x": 960,
                        "y": 540,
                        "fontSize": 72
                    },
                    {
                        "type": "null",
                        "name": "LogoPlaceholder"
                    }
                ]
            }
        ]
    }

    client.buildTemplate(template_config, output_path)
    return output_path


def generate_slideshow_template(output_path):
    """Generate template for photo slideshows"""
    print("\n" + "="*60)
    print("Generating Photo Slideshow Template")
    print("="*60 + "\n")

    client = Client()

    template_config = {
        "name": "Slideshow Template",
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "duration": 60,
        "compositions": [
            {
                "name": "TitleCard",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0, 0, 0],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "MainTitle",
                        "text": "Photo Slideshow",
                        "x": 960,
                        "y": 480,
                        "fontSize": 96
                    },
                    {
                        "type": "text",
                        "name": "Subtitle",
                        "text": "Memories",
                        "x": 960,
                        "y": 600,
                        "fontSize": 48
                    }
                ]
            },
            {
                "name": "SlideTemplate",
                "duration": 8,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.05, 0.05, 0.05],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "null",
                        "name": "PhotoPlaceholder"
                    },
                    {
                        "type": "shape",
                        "name": "CaptionBox",
                        "width": 1600,
                        "height": 150,
                        "color": [0, 0, 0]
                    },
                    {
                        "type": "text",
                        "name": "Caption",
                        "text": "Photo Caption",
                        "x": 960,
                        "y": 950,
                        "fontSize": 48
                    }
                ]
            },
            {
                "name": "EndCard",
                "duration": 7,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0, 0, 0],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "EndText",
                        "text": "Thank You",
                        "x": 960,
                        "y": 540,
                        "fontSize": 84
                    }
                ]
            }
        ]
    }

    client.buildTemplate(template_config, output_path)
    return output_path


def generate_event_promo_template(output_path):
    """Generate template for event promotion videos"""
    print("\n" + "="*60)
    print("Generating Event Promo Template")
    print("="*60 + "\n")

    client = Client()

    template_config = {
        "name": "Event Promo Template",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "duration": 25,
        "compositions": [
            {
                "name": "EventOpener",
                "duration": 3,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.2],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "EventName",
                        "text": "EVENT NAME",
                        "x": 960,
                        "y": 540,
                        "fontSize": 120
                    },
                    {
                        "type": "null",
                        "name": "LogoPlaceholder"
                    },
                    {
                        "type": "null",
                        "name": "timeline"
                    }
                ]
            },
            {
                "name": "InfoTemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.15, 0.15, 0.25],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "shape",
                        "name": "InfoCard",
                        "width": 1200,
                        "height": 600,
                        "color": [0.2, 0.2, 0.35]
                    },
                    {
                        "type": "text",
                        "name": "InfoTitle",
                        "text": "WHEN",
                        "x": 960,
                        "y": 400,
                        "fontSize": 72
                    },
                    {
                        "type": "text",
                        "name": "InfoDetails",
                        "text": "Event Details",
                        "x": 960,
                        "y": 550,
                        "fontSize": 42
                    },
                    {
                        "type": "null",
                        "name": "PhotoPlaceholder"
                    }
                ]
            },
            {
                "name": "CTATemplate",
                "duration": 5,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.8, 0.3, 0.1],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "text",
                        "name": "CTAHeadline",
                        "text": "REGISTER NOW",
                        "x": 960,
                        "y": 400,
                        "fontSize": 96
                    },
                    {
                        "type": "text",
                        "name": "CTADetails",
                        "text": "Event Info",
                        "x": 960,
                        "y": 600,
                        "fontSize": 48
                    },
                    {
                        "type": "null",
                        "name": "timeline"
                    }
                ]
            },
            {
                "name": "EventClosing",
                "duration": 3,
                "layers": [
                    {
                        "type": "solid",
                        "name": "Background",
                        "color": [0.1, 0.1, 0.2],
                        "width": 1920,
                        "height": 1080
                    },
                    {
                        "type": "null",
                        "name": "LogoPlaceholder"
                    },
                    {
                        "type": "text",
                        "name": "ClosingText",
                        "text": "See You There!",
                        "x": 960,
                        "y": 700,
                        "fontSize": 72
                    }
                ]
            }
        ]
    }

    client.buildTemplate(template_config, output_path)
    return output_path


def generate_all_templates(output_dir="AE_Templates"):
    """Generate all template files"""
    print("\n" + "="*60)
    print("GENERATING ALL AFTER EFFECTS TEMPLATES")
    print("="*60 + "\n")

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    templates = [
        ("tutorial_template.aep", generate_tutorial_template),
        ("social_media_template.aep", generate_social_media_template),
        ("product_template.aep", generate_product_showcase_template),
        ("slideshow_template.aep", generate_slideshow_template),
        ("event_template.aep", generate_event_promo_template)
    ]

    generated_files = []

    for filename, generator_func in templates:
        output_path = os.path.join(output_dir, filename)
        try:
            generator_func(output_path)
            generated_files.append(output_path)
        except Exception as e:
            print(f"\nError generating {filename}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*60)
    print("TEMPLATE GENERATION COMPLETE")
    print("="*60 + "\n")

    print("Generated templates:")
    for filepath in generated_files:
        print(f"  ✓ {filepath}")

    print(f"\nTotal: {len(generated_files)} template(s)")
    print(f"Location: {os.path.abspath(output_dir)}")

    return generated_files


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate After Effects template files (.aep)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_templates.py --all
  python generate_templates.py --template tutorial --output my_template.aep
  python generate_templates.py --template social-media --output-dir templates/
        """
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all templates'
    )

    parser.add_argument(
        '--template',
        choices=['tutorial', 'social-media', 'product', 'slideshow', 'event'],
        help='Generate a specific template'
    )

    parser.add_argument(
        '--output',
        help='Output file path (for single template)'
    )

    parser.add_argument(
        '--output-dir',
        default='AE_Templates',
        help='Output directory (for --all, default: AE_Templates)'
    )

    args = parser.parse_args()

    if args.all:
        generate_all_templates(args.output_dir)
    elif args.template:
        template_map = {
            'tutorial': ('tutorial_template.aep', generate_tutorial_template),
            'social-media': ('social_media_template.aep', generate_social_media_template),
            'product': ('product_template.aep', generate_product_showcase_template),
            'slideshow': ('slideshow_template.aep', generate_slideshow_template),
            'event': ('event_template.aep', generate_event_promo_template)
        }

        filename, generator_func = template_map[args.template]
        output_path = args.output or os.path.join(args.output_dir, filename)

        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        generator_func(output_path)
        print(f"\n✓ Template generated: {output_path}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
