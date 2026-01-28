#!/usr/bin/env python3
import argparse
import json
import os
import sys

from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin


def main():
    """
    Main entry point for the After Effects Video Editor web interface.
    """
    parser = argparse.ArgumentParser(
        description="After Effects Video Editor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ae-editor config.json
  ae-editor example.json --host 0.0.0.0 --port 8080
  ae-editor --config myproject.json
        """,
    )

    parser.add_argument("config_file", nargs="?", default=None, help="Path to the JSON configuration file to edit")

    parser.add_argument(
        "--config", default=None, help="Path to the JSON configuration file to edit (alternative to positional arg)"
    )

    parser.add_argument("--host", default="127.0.0.1", help="Host to run the web server on (default: 127.0.0.1)")

    parser.add_argument("--port", type=int, default=5000, help="Port to run the web server on (default: 5000)")

    args = parser.parse_args()

    # Determine which config file to use (positional arg takes precedence)
    config_file = args.config_file or args.config or "config.json"

    # Create default config if it doesn't exist
    if not os.path.exists(config_file):
        default_config = {
            "project": {"project_file": "", "composition": "", "output_file": "", "comp_name": ""},
            "settings": {"render_settings": "Best Settings", "output_module": "Lossless"},
            "timeline": [],
        }
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default config file: {config_file}")

    editor = VideoEditorAppMixin()

    try:
        print(f"\nStarting Video Editor at http://{args.host}:{args.port}")
        print(f"Using configuration file: {config_file}")
        editor.runVideoEditor(config_file, host=args.host, port=args.port)
    except Exception as e:
        print(f"Error starting video editor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
