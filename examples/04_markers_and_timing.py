"""
Example 4: Markers and Timing
===============================
This example shows how to add markers and control precise timing
in compositions.

This tests:
- Adding markers
- Precise timing control
- Multiple scenes with specific start times
"""

from ae_automation import Client
import json
import os

def main():
    print("="*60)
    print("Example 4: Markers and Timing")
    print("="*60)

    config = {
        "project": {
            "project_file": "path/to/your/template.aep",
            "comp_name": "MarkerDemo",
            "comp_fps": 29.97,
            "comp_width": 1920,
            "comp_height": 1080,
            "auto_time": False,  # Manual timing control
            "comp_start_time": "00:00:00",
            "comp_end_time": 30,
            "output_file": "marker_demo.mp4",
            "output_dir": os.path.join(os.getcwd(), "output"),
            "renderComp": False,
            "debug": True,
            "resources": []
        },
        "timeline": [
            {
                "name": "intro",
                "duration": 5,
                "startTime": 0,
                "template_comp": "IntroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "add_marker",
                        "comp_name": "IntroTemplate",
                        "layer_name": "timeline",
                        "marker_name": "intro_start",
                        "marker_time": 0
                    },
                    {
                        "change_type": "add_marker",
                        "comp_name": "IntroTemplate",
                        "layer_name": "timeline",
                        "marker_name": "logo_appear",
                        "marker_time": 2.5
                    }
                ]
            },
            {
                "name": "main_content",
                "duration": 15,
                "startTime": 5,
                "template_comp": "ContentTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "add_marker",
                        "comp_name": "ContentTemplate",
                        "layer_name": "timeline",
                        "marker_name": "section_1",
                        "marker_time": 0
                    },
                    {
                        "change_type": "add_marker",
                        "comp_name": "ContentTemplate",
                        "layer_name": "timeline",
                        "marker_name": "section_2",
                        "marker_time": 5
                    },
                    {
                        "change_type": "add_marker",
                        "comp_name": "ContentTemplate",
                        "layer_name": "timeline",
                        "marker_name": "section_3",
                        "marker_time": 10
                    }
                ]
            },
            {
                "name": "transition",
                "duration": 2,
                "startTime": 20,
                "template_comp": "TransitionTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "add_marker",
                        "comp_name": "TransitionTemplate",
                        "layer_name": "timeline",
                        "marker_name": "transition_peak",
                        "marker_time": 1
                    }
                ]
            },
            {
                "name": "outro",
                "duration": 8,
                "startTime": 22,
                "template_comp": "OutroTemplate",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "add_marker",
                        "comp_name": "OutroTemplate",
                        "layer_name": "timeline",
                        "marker_name": "final_frame",
                        "marker_time": 7.5
                    }
                ]
            }
        ]
    }

    # Save configuration
    config_file = "markers_timing_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print("\nTimeline structure:")

    total_markers = 0
    for scene in config['timeline']:
        markers = [a for a in scene['custom_actions'] if a['change_type'] == 'add_marker']
        total_markers += len(markers)
        print(f"\n  {scene['name']}:")
        print(f"    Start: {scene['startTime']}s, Duration: {scene['duration']}s")
        print(f"    Markers: {len(markers)}")
        for marker in markers:
            print(f"      - '{marker['marker_name']}' at {marker['marker_time']}s")

    print(f"\n  Total markers: {total_markers}")

    print("\n" + "="*60)
    print("Markers are useful for:")
    print("  - Sync points for audio")
    print("  - Animation triggers")
    print("  - Scene transitions")
    print("  - Keyframe references")
    print("="*60)

if __name__ == "__main__":
    main()
