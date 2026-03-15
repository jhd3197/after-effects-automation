#!/usr/bin/env python3
"""
After Effects Automation CLI
Unified command-line interface for all automation tasks
"""

from __future__ import annotations

import argparse
import os
import sys


def cmd_run(args: argparse.Namespace) -> None:
    """Run automation with a configuration file"""

    from ae_automation import Client

    if not os.path.exists(args.config):
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)

    print(f"Running automation with config: {args.config}")

    client = Client()
    client.startBot(args.config)


def cmd_editor(args: argparse.Namespace) -> None:
    """Open the web-based configuration editor"""
    import json

    from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin

    config_file = args.config

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
        print("Press Ctrl+C to stop the server\n")
        editor.runVideoEditor(config_file, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"Error starting video editor: {e}")
        sys.exit(1)


def cmd_test(args: argparse.Namespace) -> None:
    """Run compatibility tests"""
    import subprocess

    test_args = ["python", "test.py"]

    if args.verbose:
        test_args.append("--verbose")

    if args.version:
        test_args.extend(["--version", args.version])

    try:
        result = subprocess.run(test_args, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate a template .aep project from a built-in template"""
    from ae_automation import Client
    from ae_automation.templates import BUILTIN_TEMPLATES, list_templates

    # List available templates
    if args.list:
        print("Available templates:")
        for name, description in list_templates():
            print(f"  {name:20s} {description}")
        return

    # Determine which templates to generate
    if args.all:
        templates_to_build = list(BUILTIN_TEMPLATES.keys())
    elif args.template:
        if args.template not in BUILTIN_TEMPLATES:
            print(f"Error: Unknown template '{args.template}'")
            print(f"Available templates: {', '.join(BUILTIN_TEMPLATES.keys())}")
            sys.exit(1)
        templates_to_build = [args.template]
    else:
        print("Error: Specify --template <name>, --all, or --list")
        sys.exit(1)

    client = Client()

    for template_name in templates_to_build:
        config = BUILTIN_TEMPLATES[template_name]

        if args.output and len(templates_to_build) == 1:
            output_path = args.output
        else:
            output_path = os.path.abspath(f"{template_name}.aep")

        print(f"Generating template: {template_name} -> {output_path}")
        client.buildTemplate(config, output_path)

    print(f"\nGenerated {len(templates_to_build)} template(s).")


def cmd_export(args: argparse.Namespace) -> None:
    """Generate a template and render it to video"""
    from ae_automation import Client
    from ae_automation.templates import BUILTIN_TEMPLATES

    if args.template not in BUILTIN_TEMPLATES:
        print(f"Error: Unknown template '{args.template}'")
        print(f"Available templates: {', '.join(BUILTIN_TEMPLATES.keys())}")
        sys.exit(1)

    config = BUILTIN_TEMPLATES[args.template]
    output_dir = os.path.abspath(args.output_dir)

    # Determine output .aep path
    aep_path = os.path.join(output_dir, f"{args.template}.aep")

    if os.path.exists(aep_path) and not args.force:
        print(f"Error: {aep_path} already exists. Use --force to overwrite.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    client = Client()

    # Step 1: Generate the template
    print(f"Generating template: {args.template}")
    client.buildTemplate(config, aep_path)

    # Step 2: Determine which comp to render
    comp_name = args.comp
    if not comp_name:
        # Use the first composition defined in the template
        comps = config.get("compositions", [])
        if not comps:
            print("Error: Template has no compositions to render.")
            sys.exit(1)
        comp_name = comps[0]["name"]

    # Step 3: Render
    print(f"Rendering composition: {comp_name}")
    output_file = client.renderFile(aep_path, comp_name, output_dir)
    print(f"\nExport complete: {output_file}")


def cmd_chat(args: argparse.Namespace) -> None:
    """Start the chat panel backend server"""
    from ae_automation import Client

    client = Client()

    try:
        client.runChatPanel(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\nChat server stopped by user")
    except Exception as e:
        print(f"Error starting chat server: {e}")
        sys.exit(1)


def cmd_plugins(args: argparse.Namespace) -> None:
    """Manage plugins"""
    from ae_automation.plugins import PluginRegistry

    registry = PluginRegistry()
    sub = args.plugins_action

    if sub == "list":
        plugins = registry.list_plugins()
        if not plugins:
            print("No plugins installed.")
            return
        print(f"{'Name':<25} {'Type':<10} {'Version':<10} Description")
        print("-" * 80)
        for p in plugins:
            print(f"{p['name']:<25} {p['type']:<10} {p['version']:<10} {p['description']}")

    elif sub == "install":
        source = args.source
        try:
            result = registry.install_plugin(source)
            print(f"Installed plugin: {result['name']} v{result['version']}")
        except ValueError as exc:
            print(f"Error: {exc}")
            sys.exit(1)

    elif sub == "uninstall":
        name = args.name
        if registry.uninstall_plugin(name):
            print(f"Uninstalled plugin: {name}")
        else:
            print(f"Plugin not found: {name}")
            sys.exit(1)

    elif sub == "search":
        tags = args.tag if args.tag else None
        results = registry.search_plugins(
            query=args.query or "",
            plugin_type=args.type or "",
            tags=tags,
        )
        if not results:
            print("No matching plugins found.")
            return
        print(f"{'Name':<25} {'Type':<10} {'Tags'}")
        print("-" * 70)
        for p in results:
            tag_str = ", ".join(p.get("tags", []))
            print(f"{p['name']:<25} {p['type']:<10} {tag_str}")

    elif sub == "info":
        name = args.name
        plugin = registry.get_plugin(name)
        if plugin is None:
            print(f"Plugin not found: {name}")
            sys.exit(1)
        print(f"Name:        {plugin['name']}")
        print(f"Version:     {plugin['version']}")
        print(f"Author:      {plugin['author']}")
        print(f"Type:        {plugin['type']}")
        print(f"Description: {plugin['description']}")
        print(f"Tags:        {', '.join(plugin.get('tags', []))}")
        print(f"AE Min:      {plugin.get('ae_min_version', 'any')}")
        print(f"Location:    {plugin.get('_dir', 'unknown')}")
        compat = registry.check_plugin_compat(name)
        status = "Yes" if compat.get("compatible") else "No"
        if compat.get("warning"):
            status += f" ({compat['warning']})"
        elif compat.get("error"):
            status += f" ({compat['error']})"
        print(f"Compatible:  {status}")

    elif sub == "run":
        name = args.name
        plugin = registry.get_plugin(name)
        if plugin is None:
            print(f"Plugin not found: {name}")
            sys.exit(1)
        if plugin.get("type") not in ("template", "bundle"):
            print(f"Plugin '{name}' is type '{plugin['type']}' and cannot be run directly.")
            sys.exit(1)

        from ae_automation import Client

        client = Client()
        print(f"Running plugin: {name}")
        client.run_plugin(name)

    else:
        print("Unknown plugins action. Use: list, install, uninstall, search, info, run")
        sys.exit(1)


def cmd_batch(args: argparse.Namespace) -> None:
    """Run multiple automation configs sequentially"""
    import glob as glob_mod
    import time as time_mod

    from ae_automation import Client

    config_paths: list[str] = []

    if args.dir:
        pattern = os.path.join(args.dir, "*.json")
        config_paths = sorted(glob_mod.glob(pattern))
        if not config_paths:
            print(f"Error: No .json files found in {args.dir}")
            sys.exit(1)

    if args.configs:
        for p in args.configs:
            if not os.path.isfile(p):
                print(f"Error: Config file not found: {p}")
                sys.exit(1)
            config_paths.append(os.path.abspath(p))

    if not config_paths:
        print("Error: No config files specified. Use positional args or --dir.")
        sys.exit(1)

    print(f"Batch processing {len(config_paths)} config(s):")
    for p in config_paths:
        print(f"  - {p}")
    print()

    client = Client()
    client.queue_configs(config_paths)
    client.start_batch()

    # Wait for completion by polling status
    while True:
        status = client.get_batch_status()
        if not status["running"]:
            break
        print(
            f"  [{status['current']}/{status['total']}] Processing...",
            end="\r",
        )
        time_mod.sleep(2)

    print()
    # Report results
    results = status["results"]
    successes = sum(1 for r in results if r["status"] == "success")
    failures = sum(1 for r in results if r["status"] == "error")
    print(f"\nBatch complete: {successes} succeeded, {failures} failed")

    for r in results:
        icon = "OK" if r["status"] == "success" else "FAIL"
        msg = f"  [{icon}] {r['config']}"
        if r["error"]:
            msg += f" -- {r['error']}"
        print(msg)

    if failures > 0:
        sys.exit(1)


def cmd_diagnose(args: argparse.Namespace) -> None:
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


def main() -> None:
    """Main CLI entry point"""

    # Detect if called via legacy command
    prog_name = os.path.basename(sys.argv[0])
    is_legacy = prog_name.startswith("ae-automate")

    # If legacy command and has arguments, treat first arg as config file
    if is_legacy and len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        # Legacy mode: ae-automate config.json
        # Convert to: ae-automation run config.json
        sys.argv.insert(1, "run")

    parser = argparse.ArgumentParser(
        prog="ae-automation",
        description="After Effects Automation - Automate video production workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Global options:
  --verbose               Enable debug logging (or set AE_LOG_LEVEL=DEBUG)

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

  # Start AI chat panel backend
  ae-automation chat
  ae-automation chat --port 8080

  # Run tests
  ae-automation test
  ae-automation test --verbose
  ae-automation test --version 2024

  # Run diagnostics
  ae-automation diagnose
  ae-automation diagnose --no-wait

For more information, visit: https://github.com/jhd3197/after-effects-automation
        """,
    )

    # Global verbose flag
    parser.add_argument("--verbose", action="store_true", default=False, help="Enable debug logging output")

    # Create subparsers
    subparsers = parser.add_subparsers(
        title="commands", description="Available commands", dest="command", help="Command to execute"
    )

    # ============================================================
    # RUN command
    # ============================================================
    parser_run = subparsers.add_parser(
        "run",
        help="Run automation with a configuration file",
        description="Execute After Effects automation using a JSON configuration file",
    )
    parser_run.add_argument("config", help="Path to the JSON configuration file")
    parser_run.set_defaults(func=cmd_run)

    # ============================================================
    # EDITOR command
    # ============================================================
    parser_editor = subparsers.add_parser(
        "editor",
        help="Open web-based configuration editor",
        description="Launch a web interface to edit configuration files",
    )
    parser_editor.add_argument(
        "config", nargs="?", default="config.json", help="Path to the JSON configuration file (default: config.json)"
    )
    parser_editor.add_argument("--host", default="127.0.0.1", help="Host to run the web server on (default: 127.0.0.1)")
    parser_editor.add_argument("--port", type=int, default=5000, help="Port to run the web server on (default: 5000)")
    parser_editor.set_defaults(func=cmd_editor)

    # ============================================================
    # GENERATE command
    # ============================================================
    parser_generate = subparsers.add_parser(
        "generate",
        help="Generate a template .aep project",
        description="Create After Effects project files from built-in templates",
    )
    parser_generate.add_argument("--template", "-t", help="Name of the built-in template to generate")
    parser_generate.add_argument("--all", action="store_true", help="Generate all built-in templates")
    parser_generate.add_argument(
        "--output", "-o", help="Custom output path for the .aep file (only with single --template)"
    )
    parser_generate.add_argument("--list", "-l", action="store_true", help="List available built-in templates")
    parser_generate.set_defaults(func=cmd_generate)

    # ============================================================
    # EXPORT command
    # ============================================================
    parser_export = subparsers.add_parser(
        "export",
        help="Generate a template and render to video",
        description="Create an After Effects project from a template and render it to video",
    )
    parser_export.add_argument("--template", "-t", required=True, help="Name of the built-in template to export")
    parser_export.add_argument(
        "--output-dir", "-o", default=".", help="Directory for rendered output (default: current directory)"
    )
    parser_export.add_argument(
        "--comp", "-c", help="Composition name to render (default: first composition in template)"
    )
    parser_export.add_argument("--force", "-f", action="store_true", help="Overwrite existing files")
    parser_export.set_defaults(func=cmd_export)

    # ============================================================
    # CHAT command
    # ============================================================
    parser_chat = subparsers.add_parser(
        "chat",
        help="Start the AI chat panel backend",
        description="Launch the backend server for the AE Automation Chat panel",
    )
    parser_chat.add_argument("--host", default="127.0.0.1", help="Host to run the server on (default: 127.0.0.1)")
    parser_chat.add_argument("--port", type=int, default=5001, help="Port to run the server on (default: 5001)")
    parser_chat.set_defaults(func=cmd_chat)

    # ============================================================
    # BATCH command
    # ============================================================
    parser_batch = subparsers.add_parser(
        "batch",
        help="Run multiple configs sequentially",
        description="Queue and process multiple JSON configuration files in batch",
    )
    parser_batch.add_argument("configs", nargs="*", help="Paths to JSON configuration files")
    parser_batch.add_argument(
        "--dir", "-d", help="Directory containing .json config files to process"
    )
    parser_batch.set_defaults(func=cmd_batch)

    # ============================================================
    # TEST command
    # ============================================================
    parser_test = subparsers.add_parser(
        "test",
        help="Run compatibility tests",
        description="Test package compatibility with your After Effects installation",
    )
    parser_test.add_argument("--verbose", "-v", action="store_true", help="Show detailed test output")
    parser_test.add_argument("--version", help="Specify After Effects version for testing")
    parser_test.set_defaults(func=cmd_test)

    # ============================================================
    # PLUGINS command
    # ============================================================
    parser_plugins = subparsers.add_parser(
        "plugins",
        help="Manage community plugins",
        description="Install, list, search, and run community plugins",
    )
    plugins_sub = parser_plugins.add_subparsers(dest="plugins_action")

    # plugins list
    plugins_sub.add_parser("list", help="List installed plugins")

    # plugins install <source>
    p_install = plugins_sub.add_parser("install", help="Install a plugin from a directory or zip")
    p_install.add_argument("source", help="Path to a plugin directory or .zip file")

    # plugins uninstall <name>
    p_uninstall = plugins_sub.add_parser("uninstall", help="Uninstall a plugin by name")
    p_uninstall.add_argument("name", help="Plugin name to uninstall")

    # plugins search
    p_search = plugins_sub.add_parser("search", help="Search installed plugins")
    p_search.add_argument("query", nargs="?", default="", help="Search query")
    p_search.add_argument("--tag", action="append", help="Filter by tag (can repeat)")
    p_search.add_argument("--type", help="Filter by plugin type (template, action, bundle)")

    # plugins info <name>
    p_info = plugins_sub.add_parser("info", help="Show plugin details")
    p_info.add_argument("name", help="Plugin name")

    # plugins run <name>
    p_run = plugins_sub.add_parser("run", help="Run a template plugin")
    p_run.add_argument("name", help="Plugin name to run")

    parser_plugins.set_defaults(func=cmd_plugins)

    # ============================================================
    # DIAGNOSE command
    # ============================================================
    parser_diagnose = subparsers.add_parser(
        "diagnose", help="Run diagnostic checks", description="Diagnose After Effects scripting and automation issues"
    )
    parser_diagnose.add_argument("--no-wait", action="store_true", help="Do not wait for user input at the end")
    parser_diagnose.set_defaults(func=cmd_diagnose)

    # Parse arguments
    args = parser.parse_args()

    # Configure logging level from --verbose flag
    if args.verbose:
        import logging

        from ae_automation.logging_config import setup_logging

        setup_logging(level=logging.DEBUG)

    # Show help if no command specified
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    # Execute the command
    args.func(args)


if __name__ == "__main__":
    main()
