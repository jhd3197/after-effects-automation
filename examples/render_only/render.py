#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render Only - Simple AE Project Renderer
=========================================
Renders an After Effects project file without running automation.

Usage:
    python render.py                        # Interactive mode
    python render.py path/to/project.aep    # Direct mode
    python render.py --comp "MyComp"        # Specify composition name

This is useful when you already have a .aep file ready and just want to render it.
"""

import os
import sys
import argparse
import time

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def find_basic_template():
    """Try to find the basic composition template"""
    # Look in the basic_composition example folder
    basic_comp_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "basic_composition",
        "output",
        "basic_template.aep"
    )

    if os.path.exists(basic_comp_path):
        return basic_comp_path

    return None


def create_basic_template():
    """Generate the basic composition template"""
    print("\n" + "="*70)
    print("Template not found. Creating basic composition template...")
    print("="*70 + "\n")

    # Import the template creator from basic_composition
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "basic_composition"))

    try:
        import template

        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "basic_composition",
            "output"
        )
        os.makedirs(output_dir, exist_ok=True)

        template_path = os.path.join(output_dir, "basic_template.aep")
        template.create_template(template_path)

        return template_path

    except Exception as e:
        print(f"Error creating template: {e}")
        return None


def get_project_file(provided_path=None):
    """Get the project file path from user or arguments"""

    if provided_path:
        # User provided a path via command line
        if os.path.exists(provided_path):
            return os.path.abspath(provided_path)
        else:
            print(f"Error: File not found: {provided_path}")
            return None

    # Interactive mode - ask user for file
    print("\n" + "="*70)
    print("After Effects Project Renderer")
    print("="*70 + "\n")

    print("Options:")
    print("  1. Enter path to your .aep file")
    print("  2. Use basic template (IntroTemplate or OutroTemplate)")
    print("  3. Use automation output (FinalComposition - requires running automation first)")
    print("  4. Exit")
    print()

    choice = input("Select option (1-4): ").strip()

    if choice == "1":
        file_path = input("\nEnter path to .aep file: ").strip()
        # Remove quotes if user copy-pasted from Windows Explorer
        file_path = file_path.strip('"').strip("'")

        if os.path.exists(file_path):
            abs_path = os.path.abspath(file_path)

            # Provide hints about available compositions
            file_name = os.path.basename(abs_path).lower()
            if "ae_automation" in file_name:
                print(f"\nSelected: {os.path.basename(abs_path)}")
                print("This file should contain: FinalComposition (assembled scenes)")
            elif "basic_template" in file_name:
                print(f"\nSelected: {os.path.basename(abs_path)}")
                print("This file should contain: IntroTemplate, OutroTemplate")

            return abs_path
        else:
            print(f"\nError: File not found: {file_path}")
            return None

    elif choice == "2":
        # Try to find or create basic template
        template_path = find_basic_template()

        if template_path:
            print(f"\nFound template: {template_path}")
            print("\nAvailable compositions: IntroTemplate, OutroTemplate")
            return template_path
        else:
            # Generate it
            template_path = create_basic_template()
            if template_path:
                print(f"\nTemplate created: {template_path}")
                print("\nAvailable compositions: IntroTemplate, OutroTemplate")
                return template_path
            else:
                print("\nFailed to create template")
                return None

    elif choice == "3":
        # Use automation output file
        automation_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "basic_composition",
            "output",
            "ae_automation.aep"
        )

        if os.path.exists(automation_path):
            print(f"\nFound automation file: {automation_path}")
            print("\nNote: This includes FinalComposition with all scenes")
            return automation_path
        else:
            print("\nAutomation file not found!")
            print("Please run the basic_composition automation first:")
            print("  cd examples/basic_composition")
            print("  python run.py")
            return None

    else:
        print("\nExiting...")
        return None


def render_project(project_path, comp_name=None, output_dir=None, interactive=False):
    """Render an After Effects project

    Args:
        project_path: Path to .aep file
        comp_name: Composition name (None = use default)
        output_dir: Output directory (None = current_dir/output)
        interactive: If True, prompt for comp name; if False, use default
    """
    from ae_automation import settings
    import subprocess

    print("\n" + "="*70)
    print("Starting Render")
    print("="*70 + "\n")

    # Determine output directory
    # Default to current working directory's output folder
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "output")

    os.makedirs(output_dir, exist_ok=True)

    # If no comp name provided, ask user or use default
    if comp_name is None:
        print(f"Project: {os.path.basename(project_path)}")

        # Determine smart default based on file name
        file_name = os.path.basename(project_path).lower()
        if "basic_template" in file_name:
            default_comp = "IntroTemplate"
            print("Hint: basic_template.aep contains IntroTemplate and OutroTemplate")
        elif "ae_automation" in file_name:
            default_comp = "FinalComposition"
            print("Hint: ae_automation.aep should contain FinalComposition")
        else:
            default_comp = "FinalComposition"

        # Only prompt if in interactive mode
        if interactive:
            try:
                prompt = f"Enter composition name (or press Enter for '{default_comp}'): "
                comp_name = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                comp_name = ""
        else:
            comp_name = ""

        if not comp_name:
            comp_name = default_comp
            print(f"Using default composition: {comp_name}")

    print(f"\nConfiguration:")
    print(f"  Project:     {project_path}")
    print(f"  Composition: {comp_name}")
    print(f"  Output Dir:  {output_dir}")
    print()

    # Build output path
    output_file = os.path.join(output_dir, f"{comp_name}.mp4")

    # Build aerender command
    render_command = f'"{settings.AERENDER_PATH}" -project "{project_path}" -comp "{comp_name}" -output "{output_file}" -mem_usage 20 40'

    print("Rendering...")
    print("-" * 70)

    start_time = time.time()

    # Execute aerender
    process = subprocess.Popen(
        render_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Stream output and collect it for error analysis
    output_lines = []
    for line in process.stdout:
        print(line.rstrip())
        output_lines.append(line)

    # Wait for completion
    process.wait()

    # Get stderr
    stderr = process.stderr.read()

    end_time = time.time()
    render_time = end_time - start_time

    # Combine stdout and stderr for error checking
    all_output = '\n'.join(output_lines) + '\n' + stderr

    # Check for composition not found error
    if "No comp was found" in all_output or "No comp was found" in stderr:
        print("-" * 70)
        print("\n" + "="*70)
        print("ERROR: Composition Not Found")
        print("="*70 + "\n")
        print(f"Could not find composition: '{comp_name}'")
        print()
        print("Possible solutions:")
        print()

        file_name = os.path.basename(project_path).lower()
        if "basic_template" in file_name:
            print("  For basic_template.aep, try one of these compositions:")
            print("    python render.py --comp \"IntroTemplate\"")
            print("    python render.py --comp \"OutroTemplate\"")
        elif "ae_automation" in file_name:
            print("  For ae_automation.aep, the composition should be:")
            print("    python render.py --comp \"FinalComposition\"")
        else:
            print("  1. Open the .aep file in After Effects")
            print("  2. Check the composition names (case-sensitive)")
            print("  3. Run render.py again with the correct name")

        print()
        print("  Or run in interactive mode to select a different file:")
        print("    python render.py")

        return None

    if process.returncode == 0:
        print("-" * 70)
        print("\n" + "="*70)
        print("Render Complete!")
        print("="*70 + "\n")
        print(f"Output:      {output_file}")
        print(f"Render Time: {render_time:.2f}s")
        print()

        # Check if file exists and show size
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"File Size:   {file_size:.2f} MB")

        return output_file
    else:
        print("\n" + "="*70)
        print("Render Failed!")
        print("="*70 + "\n")

        # Print error output
        if stderr:
            print("Error Output:")
            print(stderr)

        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Render an After Effects project file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python render.py                           # Interactive mode
  python render.py myproject.aep             # Render with default settings
  python render.py myproject.aep --comp "Intro"  # Render specific comp
  python render.py --comp "MyComp"           # Use basic template, render MyComp
        """
    )

    parser.add_argument(
        'project_file',
        nargs='?',
        help='Path to .aep project file (optional, will prompt if not provided)'
    )

    parser.add_argument(
        '--comp',
        '-c',
        default=None,
        help='Composition name to render (default: FinalComposition or prompt)'
    )

    parser.add_argument(
        '--output',
        '-o',
        default=None,
        help='Output directory (default: project directory/output)'
    )

    args = parser.parse_args()

    try:
        # Determine if we're in interactive mode
        # Interactive if: no project file provided AND no comp name provided
        is_interactive = args.project_file is None

        # Get project file
        project_path = get_project_file(args.project_file)

        if not project_path:
            sys.exit(1)

        # Render it
        output_file = render_project(
            project_path,
            comp_name=args.comp,
            output_dir=args.output,
            interactive=is_interactive
        )

        if output_file:
            print("\nSuccess!")
            sys.exit(0)
        else:
            print("\nRender failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nRender cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
