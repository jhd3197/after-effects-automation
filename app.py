#!/usr/bin/env python3
import os
import sys
import argparse
import json
from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin

def main():
    """
    Main entry point for the After Effects Video Editor web interface.
    """
    parser = argparse.ArgumentParser(
        description='After Effects Video Editor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to the JSON configuration file to edit (default: config.json)'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to run the web server on (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run the web server on (default: 5000)'
    )
    
    args = parser.parse_args()
    
    # Create default config if it doesn't exist
    if not os.path.exists(args.config):
        default_config = {
            "project": {
                "project_file": "",
                "composition": "",
                "output_file": "",
                "comp_name": ""
            },
            "settings": {
                "render_settings": "Best Settings",
                "output_module": "Lossless"
            },
            "timeline": []
        }
        with open(args.config, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default config file: {args.config}")
    
    editor = VideoEditorAppMixin()
    
    try:
        print(f"\nStarting Video Editor at http://{args.host}:{args.port}")
        print(f"Using configuration file: {args.config}")
        editor.runVideoEditor(args.config, host=args.host, port=args.port)
    except Exception as e:
        print(f"Error starting video editor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
