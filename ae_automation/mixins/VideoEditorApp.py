from flask import Flask, render_template, request, jsonify
import json
import os
from werkzeug.serving import run_simple
import webbrowser
from threading import Timer

class VideoEditorAppMixin:
    def __init__(self):
        # Get absolute path to the videoEditor directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, 'videoEditor')
        static_dir = os.path.join(base_dir, 'videoEditor')
        
        self.app = Flask(
            __name__,
            template_folder=template_dir,  # Absolute path to templates
            static_folder=static_dir       # Absolute path to static files
        )
        self.data = {}
        self.file_path = ""

        @self.app.route('/')
        def index():
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = {}  # Default empty data if file_path is not provided or file does not exist
            return render_template('index.html', data=self.data, file_path=self.file_path)

        @self.app.route('/update', methods=['POST'])
        def update():
            new_data = request.json
            file_path = new_data.pop('file_path', None)
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(new_data, f, indent=4)
                return jsonify({"message": "Data updated successfully", "file_path": file_path})
            else:
                return jsonify({"message": "No file path provided"}), 400

    def runVideoEditor(self, file_path, host='127.0.0.1', port=5000):
        # Ensure file_path is absolute
        self.file_path = os.path.abspath(file_path)
        print(f"Starting server at http://{host}:{port}/")
        print(f"Editing file: {self.file_path}")
        Timer(1.5, self.open_browser, args=[host, port]).start()
        run_simple(host, port, self.app, use_reloader=False, use_debugger=True)

    def open_browser(self, host, port):
        webbrowser.open_new(f'http://{host}:{port}/')

# HTML, CSS, and JavaScript remain the same
