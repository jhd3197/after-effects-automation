#!/usr/bin/env python3
"""
After Effects Automation CLI
Unified command-line interface for all automation tasks
"""

import os
import sys
import argparse


def cmd_run(args):
    """Run automation with a configuration file"""
    from ae_automation import Client
    import json

    if not os.path.exists(args.config):
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)

    print(f"Running automation with config: {args.config}")

    client = Client()
    client.startBot(args.config)


def cmd_editor(args):
    """Open the web-based configuration editor"""
    from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin
    import json

    config_file = args.config

    # Create default config if it doesn't exist
    if not os.path.exists(config_file):
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
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default config file: {config_file}")

    editor = VideoEditorAppMixin()

    try:
        print(f"\nStarting Video Editor at http://{args.host}:{args.port}")
        print(f"Using configuration file: {config_file}")
        print("Press Ctrl+C to stop the server\n")
        editor.runVideoEditor(config_file, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"Error starting video editor: {e}")
        sys.exit(1)





def cmd_test(args):
    """Run compatibility tests"""
    import subprocess

    test_args = ['python', 'test.py']

    if args.verbose:
        test_args.append('--verbose')

    if args.version:
        test_args.extend(['--version', args.version])

    try:
        result = subprocess.run(test_args, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


def cmd_diagnose(args):
    """Run diagnostic checks"""
    from ae_automation import Client

    client = Client()

    try:
        client.run_full_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

    if not args.no_wait:
        input("\nPress Enter to close...")

    sys.exit(0)


def main():
    """Main CLI entry point"""

    # Detect if called via legacy command
    prog_name = os.path.basename(sys.argv[0])
    is_legacy = prog_name.startswith('ae-automate')

    # If legacy command and has arguments, treat first arg as config file
    if is_legacy and len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Legacy mode: ae-automate config.json
        # Convert to: ae-automation run config.json
        sys.argv.insert(1, 'run')

    parser = argparse.ArgumentParser(
        prog='ae-automation',
        description='After Effects Automation - Automate video production workflows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run automation
  ae-automation run config.json
  ae-automation run example.json

  # Open editor
  ae-automation editor config.json
  ae-automation editor config.json --port 8080
  ae-automation editor config.json --host 0.0.0.0 --port 8080

  # Generate templates
  ae-automation generate --all
  ae-automation generate --template tutorial
  ae-automation generate --template social-media --output my_template.aep

  # Create template and export as video
  ae-automation export --template tutorial
  ae-automation export --template social-media --output-dir renders/
  ae-automation export --template tutorial --comp IntroTemplate --force

  # Run tests
  ae-automation test
  ae-automation test --verbose
  ae-automation test --version 2024

  # Run diagnostics
  ae-automation diagnose
  ae-automation diagnose --no-wait

For more information, visit: https://github.com/jhd3197/after-effects-automation
        """
    )

    # Create subparsers
    subparsers = parser.add_subparsers(
        title='commands',
        description='Available commands',
        dest='command',
        help='Command to execute'
    )

    # ============================================================
    # RUN command
    # ============================================================
    parser_run = subparsers.add_parser(
        'run',
        help='Run automation with a configuration file',
        description='Execute After Effects automation using a JSON configuration file'
    )
    parser_run.add_argument(
        'config',
        help='Path to the JSON configuration file'
    )
    parser_run.set_defaults(func=cmd_run)

    # ============================================================
    # EDITOR command
    # ============================================================
    parser_editor = subparsers.add_parser(
        'editor',
        help='Open web-based configuration editor',
        description='Launch a web interface to edit configuration files'
    )
    parser_editor.add_argument(
        'config',
        nargs='?',
        default='config.json',
        help='Path to the JSON configuration file (default: config.json)'
    )
    parser_editor.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to run the web server on (default: 127.0.0.1)'
    )
    parser_editor.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run the web server on (default: 5000)'
    )
    parser_editor.set_defaults(func=cmd_editor)

    # ============================================================
    # TEST command
    # ============================================================
    parser_test = subparsers.add_parser(
        'test',
        help='Run compatibility tests',
        description='Test package compatibility with your After Effects installation'
    )
    parser_test.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed test output'
    )
    parser_test.add_argument(
        '--version',
        help='Specify After Effects version for testing'
    )
    parser_test.set_defaults(func=cmd_test)

    # ============================================================
    # DIAGNOSE command
    # ============================================================
    parser_diagnose = subparsers.add_parser(
        'diagnose',
        help='Run diagnostic checks',
        description='Diagnose After Effects scripting and automation issues'
    )
    parser_diagnose.add_argument(
        '--no-wait',
        action='store_true',
        help='Do not wait for user input at the end'
    )
    parser_diagnose.set_defaults(func=cmd_diagnose)

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command specified
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    # Execute the command
    args.func(args)


if __name__ == '__main__':
    main()
