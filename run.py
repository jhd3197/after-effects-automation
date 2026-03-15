#!/usr/bin/env python3
import argparse
import os
import sys

import ae_automation
from ae_automation.settings import validate_settings


def main():
    """
    Main entry point for the After Effects automation tool.
    """
    parser = argparse.ArgumentParser(
        description="After Effects Automation Tool", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("config_file", help="Path to the JSON configuration file")

    args = parser.parse_args()

    # Validate settings before proceeding
    try:
        validate_settings()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    # Check if config file exists
    if not os.path.exists(args.config_file):
        print(f"Error: Config file not found: {args.config_file}")
        sys.exit(1)

    # Initialize automation client
    client = ae_automation.Client()

    try:
        print("\nStarting After Effects automation...")
        client.startBot(args.config_file)
        print("Automation completed successfully!")
    except Exception as e:
        print(f"Error during automation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
