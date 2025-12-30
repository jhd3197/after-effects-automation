#!/usr/bin/env python3
"""
Quick script to generate all example templates with paths matching the example configs
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_templates import (
    generate_tutorial_template,
    generate_social_media_template,
    generate_product_showcase_template,
    generate_slideshow_template,
    generate_event_promo_template
)


def main():
    """Generate templates for examples"""
    print("\n" + "="*60)
    print("Generating Example Templates")
    print("="*60 + "\n")

    # Create output directory
    output_dir = "AE_Templates"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}\n")

    templates = [
        ("tutorial_template.aep", generate_tutorial_template, "01_tutorial_video.json"),
        ("social_media_template.aep", generate_social_media_template, "02_social_media_post.json"),
        ("product_template.aep", generate_product_showcase_template, "03_product_showcase.json"),
        ("slideshow_template.aep", generate_slideshow_template, "04_photo_slideshow.json"),
        ("event_template.aep", generate_event_promo_template, "05_event_promo.json"),
    ]

    print("The following templates will be generated:\n")
    for filename, _, config_name in templates:
        print(f"  • {filename:<30} (for {config_name})")

    print("\n" + "="*60 + "\n")

    generated = []
    for filename, generator_func, config_name in templates:
        output_path = os.path.join(output_dir, filename)
        try:
            print(f"Generating {filename}...")
            generator_func(output_path)
            generated.append((filename, config_name))
        except Exception as e:
            print(f"✗ Error generating {filename}: {e}\n")

    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60 + "\n")

    if generated:
        print("✓ Successfully generated templates:\n")
        for filename, config_name in generated:
            print(f"  {filename:<30} → examples/configs/{config_name}")

        print(f"\n📁 Location: {os.path.abspath(output_dir)}")
        print(f"📊 Total: {len(generated)} template(s)\n")

        print("="*60)
        print("NEXT STEPS")
        print("="*60 + "\n")
        print("1. Update the JSON config files in examples/configs/")
        print("   to point to these template files:\n")
        print('   "project_file": "AE_Templates/tutorial_template.aep"')
        print("\n2. Open a template in After Effects to customize:\n")
        for filename, _ in generated[:2]:
            print(f"   AE_Templates/{filename}")
        print("\n3. Run an example with the editor:\n")
        print("   ae-editor examples/configs/01_tutorial_video.json")
        print("\n4. Or run automation directly:\n")
        print("   ae-automate examples/configs/01_tutorial_video.json")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
