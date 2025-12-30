from flask import Flask, send_from_directory, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import subprocess
from werkzeug.serving import run_simple
import webbrowser
from threading import Timer
from pathlib import Path

class VideoEditorAppMixin:
    def __init__(self):
        # Get absolute path to the videoEditor directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dist_dir = os.path.join(base_dir, 'videoEditor', 'dist')

        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for React development

        self.data = {}
        self.file_path = ""
        self.history = []
        self.history_index = -1

        # API Routes
        @self.app.route('/api/project', methods=['GET'])
        def get_project():
            """Get current project data"""
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
            return jsonify({
                "success": True,
                "data": self.data,
                "file_path": self.file_path
            })

        @self.app.route('/api/project', methods=['POST'])
        def update_project():
            """Update project data with history tracking"""
            try:
                new_data = request.json

                # Add to history for undo/redo
                if self.history_index < len(self.history) - 1:
                    self.history = self.history[:self.history_index + 1]
                self.history.append(json.dumps(self.data))
                self.history_index += 1

                # Update data
                self.data = new_data.get('data', {})

                # Save to file
                if self.file_path:
                    with open(self.file_path, 'w') as f:
                        json.dump(self.data, f, indent=4)

                return jsonify({
                    "success": True,
                    "message": "Project updated successfully",
                    "can_undo": self.history_index > 0,
                    "can_redo": self.history_index < len(self.history) - 1
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route('/api/undo', methods=['POST'])
        def undo():
            """Undo last change"""
            if self.history_index > 0:
                self.history_index -= 1
                self.data = json.loads(self.history[self.history_index])
                if self.file_path:
                    with open(self.file_path, 'w') as f:
                        json.dump(self.data, f, indent=4)
                return jsonify({
                    "success": True,
                    "data": self.data,
                    "can_undo": self.history_index > 0,
                    "can_redo": True
                })
            return jsonify({"success": False, "message": "Nothing to undo"}), 400

        @self.app.route('/api/redo', methods=['POST'])
        def redo():
            """Redo last undone change"""
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.data = json.loads(self.history[self.history_index])
                if self.file_path:
                    with open(self.file_path, 'w') as f:
                        json.dump(self.data, f, indent=4)
                return jsonify({
                    "success": True,
                    "data": self.data,
                    "can_undo": True,
                    "can_redo": self.history_index < len(self.history) - 1
                })
            return jsonify({"success": False, "message": "Nothing to redo"}), 400



        @self.app.route('/api/render', methods=['POST'])
        def render_project():
            """Trigger rendering of the project"""
            try:
                render_data = request.json
                output_path = render_data.get('output_path', 'output.mp4')

                # Get project file path and composition name from data
                project_file = self.data.get('project', {}).get('project_file', '')
                comp_name = self.data.get('project', {}).get('comp_name', 'FinalComposition')

                if not project_file:
                    return jsonify({
                        "success": False,
                        "error": "No project file specified. Please set project_file in project settings."
                    }), 400

                # Convert to absolute path and normalize
                # If it's a relative path, make it relative to the JSON file's directory
                if not os.path.isabs(project_file):
                    if self.file_path:
                        # Make it relative to the JSON file's directory
                        json_dir = os.path.dirname(os.path.abspath(self.file_path))
                        project_file = os.path.join(json_dir, project_file)
                    else:
                        # Make it relative to current working directory
                        project_file = os.path.abspath(project_file)

                # Normalize path (remove ./ and \\ etc)
                project_file = os.path.normpath(project_file)

                # Smart detection: if rendering FinalComposition, prefer ae_automation.aep
                if comp_name == 'FinalComposition':
                    project_dir = os.path.dirname(project_file)
                    ae_automation_file = os.path.join(project_dir, 'ae_automation.aep')

                    if os.path.exists(ae_automation_file):
                        print(f"✓ Found ae_automation.aep with FinalComposition")
                        project_file = ae_automation_file
                    elif not os.path.exists(project_file):
                        return jsonify({
                            "success": False,
                            "error": f"FinalComposition requires ae_automation.aep. File not found.\n\nPlease run the automation first to generate ae_automation.aep with FinalComposition.\n\nSearched for: {ae_automation_file}"
                        }), 400
                    else:
                        # Warn that they're using the wrong file
                        print(f"⚠ WARNING: Using {os.path.basename(project_file)} for FinalComposition")
                        print(f"⚠ FinalComposition is typically in ae_automation.aep")
                        print(f"⚠ If render fails, run the automation first to generate ae_automation.aep")

                # Verify the file exists
                if not os.path.exists(project_file):
                    return jsonify({
                        "success": False,
                        "error": f"Project file not found: {project_file}"
                    }), 400

                # Determine output directory
                if os.path.dirname(output_path):
                    output_dir = os.path.dirname(output_path)
                    filename = os.path.basename(output_path)
                else:
                    output_dir = os.path.dirname(self.file_path) if self.file_path else os.getcwd()
                    filename = output_path

                # Ensure output directory exists
                os.makedirs(output_dir, exist_ok=True)

                # Full output path
                full_output_path = os.path.join(output_dir, filename)

                # Use the renderFile method if available (from afterEffectMixin)
                # Otherwise fall back to direct subprocess call
                print("\n" + "="*70)
                print("RENDER STARTED")
                print("="*70)
                print(f"Project File: {project_file}")
                print(f"Composition:  {comp_name}")
                print(f"Output:       {full_output_path}")
                print("-"*70)

                # Expected output from aerender
                expected_output = os.path.join(output_dir, f"{comp_name}.mp4")

                if hasattr(self, 'renderFile'):
                    # Use the mixin method if available
                    self.renderFile(project_file, comp_name, output_dir)
                else:
                    # Fallback: use subprocess directly
                    print("Using fallback render method (subprocess)")
                    from ae_automation import settings
                    import subprocess

                    render_command = f'"{settings.AERENDER_PATH}" -project "{project_file}" -comp "{comp_name}" -output "{expected_output}" -mem_usage 20 40'

                    print(f"Executing: {render_command}")

                    process = subprocess.Popen(
                        render_command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )

                    # Stream output
                    for line in process.stdout:
                        print(line.rstrip())

                    process.wait()

                    if process.returncode != 0:
                        stderr = process.stderr.read()

                        # Check for composition not found error
                        if "No comp was found" in stderr:
                            project_name = os.path.basename(project_file)
                            error_msg = f"Composition '{comp_name}' not found in {project_name}\n\n"

                            if 'basic_template' in project_name.lower():
                                error_msg += "Available compositions in basic_template.aep:\n"
                                error_msg += "  • IntroTemplate\n"
                                error_msg += "  • OutroTemplate\n\n"
                                error_msg += "For FinalComposition, you need ae_automation.aep.\n"
                                error_msg += "Run the automation first to generate it."
                            elif comp_name == 'FinalComposition':
                                error_msg += "FinalComposition is created by running the automation.\n"
                                error_msg += "Please run the automation to generate ae_automation.aep first."

                            raise Exception(error_msg)
                        else:
                            raise Exception(f"Render failed with code {process.returncode}: {stderr}")

                # Check if the rendered file exists
                if os.path.exists(expected_output):
                    # Rename to user's desired output name if different
                    if expected_output != full_output_path:
                        import shutil
                        shutil.move(expected_output, full_output_path)

                    file_size = os.path.getsize(full_output_path) / (1024 * 1024)  # MB
                    return jsonify({
                        "success": True,
                        "message": "Rendering completed successfully",
                        "output_path": full_output_path,
                        "file_size_mb": round(file_size, 2),
                        "status": "completed"
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": f"Rendering failed. Expected output file not found: {expected_output}",
                        "status": "failed"
                    }), 500

            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"Render error: {error_details}")
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "details": error_details
                }), 500

        @self.app.route('/api/serve-file', methods=['GET'])
        def serve_file():
            """Serve arbitrary files from the filesystem (safe-ish for local tool)"""
            file_path = request.args.get('path')
            if not file_path:
                return jsonify({"error": "No path provided"}), 400
            
            # Normalize path
            file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                return jsonify({"error": "File not found"}), 404
                
            return send_file(file_path)

        # Serve React app
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def serve(path):
            """Serve React build files"""
            if path and os.path.exists(os.path.join(self.dist_dir, path)):
                return send_from_directory(self.dist_dir, path)
            return send_from_directory(self.dist_dir, 'index.html')

    def runVideoEditor(self, file_path, host='127.0.0.1', port=5000, dev_mode=False):
        """
        Run the video editor application

        Args:
            file_path: Path to the project JSON file
            host: Host address
            port: Port number
            dev_mode: If True, expects React dev server on port 5173
        """
        self.file_path = os.path.abspath(file_path)

        # Load initial data
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)

        # Initialize history
        self.history = [json.dumps(self.data)]
        self.history_index = 0

        print(f"Starting Video Editor API at http://{host}:{port}/")
        print(f"Editing file: {self.file_path}")

        if dev_mode:
            print("Development mode: React dev server should be running on http://localhost:5173")
        else:
            print("Production mode: Serving built React app")
            Timer(1.5, self.open_browser, args=[host, port]).start()

        run_simple(host, port, self.app, use_reloader=False, use_debugger=True)

    def open_browser(self, host, port):
        webbrowser.open_new(f'http://{host}:{port}/')
