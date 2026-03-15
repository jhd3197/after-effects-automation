"""
Chat Panel Mixin — Flask endpoints for the AE Automation Chat CEP extension.

Provides AI chat via Prompture and translates natural language into AE actions.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

from ae_automation.logging_config import get_logger

logger = get_logger(__name__)

# Add Prompture to path if available
PROMPTURE_PATH = os.environ.get(
    "PROMPTURE_PATH",
    os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "prompture"),
)
if os.path.isdir(PROMPTURE_PATH) and PROMPTURE_PATH not in sys.path:
    sys.path.insert(0, PROMPTURE_PATH)

# System prompt that teaches the AI about AE automation
SYSTEM_PROMPT = """You are an After Effects automation assistant running inside Adobe After Effects.
You help users control AE through natural language commands.

You can perform these actions by including them in your response:
- create_comp: Create a new composition (params: name, width, height, duration, fps)
- edit_text: Change text layer content (params: comp_name, layer_name, value)
- edit_property: Change any layer property (params: comp_name, layer_name, property, value)
- set_color: Set a color property (params: comp_name, layer_name, property, hex)
- add_marker: Add a marker to a layer (params: comp_name, layer_name, name, time)
- save_project: Save the current project
- list_comps: List all compositions
- get_project_info: Get project details
- run_plugin: Run an installed community plugin template (params: name)

When the user asks you to do something in AE, respond with a helpful message AND include
the appropriate actions. Format actions as a JSON array in your response wrapped in
<actions>[...]</actions> tags. Each action has a "type", "label" (human-readable), and "params".

Example:
User: "Create a 1080p comp called Intro that's 10 seconds long"
Response: "I'll create a 1920x1080 composition called 'Intro' at 30fps for 10 seconds.
<actions>[{"type":"create_comp","label":"Create Intro comp","params":{"name":"Intro","width":1920,"height":1080,"duration":10,"fps":30}}]</actions>"

If the user provides project context (compositions, layers), use that information to give
accurate suggestions and target the right compositions/layers.

Keep responses concise — this runs in a small panel inside AE."""


class ChatPanelMixin:
    """Mixin that adds chat panel API endpoints to the Flask app."""

    chat_app: Flask
    _chat_history: list[dict[str, str]]

    def _init_chat(self) -> None:
        """Initialize the chat Flask app with all endpoints."""
        self.chat_app = Flask(__name__)
        CORS(self.chat_app, origins=["http://localhost:*", "http://127.0.0.1:*"])
        self._chat_history = []
        self._prompture_available = False
        self._extract_fn = None

        # Try to import Prompture
        try:
            from prompture import extract_with_model

            self._extract_fn = extract_with_model
            self._prompture_available = True
            logger.info("Prompture loaded successfully")
        except ImportError:
            logger.warning(
                "Prompture not found at %s — AI chat will be limited. Set PROMPTURE_PATH env var or install prompture.",
                PROMPTURE_PATH,
            )

        self._register_chat_routes()

    def _register_chat_routes(self) -> None:
        """Register all chat API endpoints."""

        @self.chat_app.route("/api/chat/status", methods=["GET"])
        def chat_status():
            return jsonify(
                {
                    "success": True,
                    "status": "online",
                    "prompture": self._prompture_available,
                }
            )

        @self.chat_app.route("/api/chat/message", methods=["POST"])
        def chat_message():
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "Invalid or missing JSON body"}), 400
                message = data.get("message", "")
                history = data.get("history", [])
                model = data.get("model", "openai/gpt-4o")
                ae_context = data.get("ae_context")

                if not message:
                    return jsonify({"success": False, "error": "Empty message"}), 400

                response_text, actions = self._process_chat(message, history, model, ae_context)

                return jsonify(
                    {
                        "success": True,
                        "response": response_text,
                        "actions": actions,
                    }
                )
            except Exception as e:
                logger.error("Chat error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/execute", methods=["POST"])
        def chat_execute():
            """Execute an AE action via the command queue (fallback when no CSInterface)."""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "Invalid or missing JSON body"}), 400
                action = data.get("action", {})
                result = self._execute_action(action)
                return jsonify(result)
            except Exception as e:
                logger.error("Execute error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/render-progress", methods=["GET"])
        def render_progress():
            """Return current render progress as JSON."""
            try:
                progress = self.get_render_progress()
                return jsonify({"success": True, **progress})
            except Exception as e:
                logger.error("Render progress error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/batch", methods=["POST"])
        def batch_queue():
            """Accept a list of config paths to queue for batch processing."""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "Invalid or missing JSON body"}), 400
                configs = data.get("configs", [])
                if not configs:
                    return jsonify({"success": False, "error": "No configs provided"}), 400
                total = self.queue_configs(configs)
                self.start_batch()
                return jsonify(
                    {"success": True, "queued": total, "message": f"Queued {total} configs and started batch"}
                )
            except Exception as e:
                logger.error("Batch queue error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/batch-status", methods=["GET"])
        def batch_status():
            """Return current batch processing status."""
            try:
                status = self.get_batch_status()
                return jsonify({"success": True, **status})
            except Exception as e:
                logger.error("Batch status error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/plugins", methods=["GET"])
        def chat_plugins():
            """List all installed plugins."""
            try:
                from ae_automation.plugins import PluginRegistry

                registry = PluginRegistry()
                plugins = registry.list_plugins()
                # Strip internal _dir key before sending to client
                safe = [{k: v for k, v in p.items() if not k.startswith("_")} for p in plugins]
                return jsonify({"success": True, "plugins": safe})
            except Exception as e:
                logger.error("Plugins list error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        @self.chat_app.route("/api/chat/plugins/run", methods=["POST"])
        def chat_plugins_run():
            """Run a plugin by name."""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "Invalid or missing JSON body"}), 400
                name = data.get("name", "")
                if not name:
                    return jsonify({"success": False, "error": "Plugin name required"}), 400
                result = self._execute_action({"type": "run_plugin", "params": {"name": name}})
                return jsonify(result)
            except Exception as e:
                logger.error("Plugin run error: %s", e, exc_info=True)
                return jsonify({"success": False, "error": str(e)}), 500

        # Also serve static files for the extension (for dev/testing)
        ext_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "extension",
            "client",
        )

        @self.chat_app.route("/", defaults={"path": ""})
        @self.chat_app.route("/<path:path>")
        def serve_panel(path):
            from flask import send_from_directory

            if path and os.path.exists(os.path.join(ext_dir, path)):
                return send_from_directory(ext_dir, path)
            return send_from_directory(ext_dir, "index.html")

    def _process_chat(
        self,
        message: str,
        history: list[dict[str, str]],
        model: str,
        ae_context: dict[str, Any] | None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Process a chat message, return (response_text, actions)."""

        # Build context-aware prompt
        context_block = ""
        if ae_context:
            context_block = f"\n\nCurrent AE project context:\n```json\n{json.dumps(ae_context, indent=2)}\n```\n"

        if self._prompture_available and self._extract_fn:
            return self._process_with_prompture(message, history, model, context_block)
        else:
            return self._process_fallback(message, ae_context)

    def _process_with_prompture(
        self,
        message: str,
        history: list[dict[str, str]],
        model: str,
        context_block: str,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Use Prompture to generate AI response with actions."""
        from pydantic import BaseModel, Field

        class AEAction(BaseModel):
            type: str = Field(
                description="Action type: create_comp, edit_text, edit_property, set_color, add_marker, save_project, list_comps, get_project_info"
            )
            label: str = Field(description="Human-readable description of the action")
            params: dict[str, Any] = Field(default_factory=dict, description="Action parameters")

        class ChatResponse(BaseModel):
            message: str = Field(description="Response message to display to the user")
            actions: list[AEAction] = Field(default_factory=list, description="AE actions to execute")

        # Build conversation for extraction
        conversation = SYSTEM_PROMPT + context_block + "\n\n"
        for msg in history[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            conversation += f"{role}: {content}\n"
        conversation += f"user: {message}\n"
        conversation += "Respond with a helpful message. Include actions if the user wants to do something in AE."

        try:
            result = self._extract_fn(
                ChatResponse,
                conversation,
                model_name=model,
            )
            response = result.json_object
            actions = [a.model_dump() for a in response.actions]
            return response.message, actions
        except Exception as e:
            logger.error("Prompture extraction failed: %s", e)
            return f"I understood your request but hit an error: {e}", []

    def _process_fallback(
        self,
        message: str,
        ae_context: dict[str, Any] | None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Simple keyword-based fallback when Prompture is unavailable."""
        msg_lower = message.lower()
        actions: list[dict[str, Any]] = []

        if "list" in msg_lower and "comp" in msg_lower:
            actions.append({"type": "list_comps", "label": "List compositions", "params": {}})
            return "Let me list the compositions in your project.", actions

        if "project info" in msg_lower or "project details" in msg_lower:
            actions.append({"type": "get_project_info", "label": "Get project info", "params": {}})
            return "Getting your project information.", actions

        if "save" in msg_lower:
            actions.append({"type": "save_project", "label": "Save project", "params": {}})
            return "I'll save your project.", actions

        if "create" in msg_lower and "comp" in msg_lower:
            actions.append(
                {
                    "type": "create_comp",
                    "label": "Create composition",
                    "params": {
                        "name": "New Composition",
                        "width": 1920,
                        "height": 1080,
                        "duration": 10,
                        "fps": 30,
                    },
                }
            )
            return (
                "I'll create a new 1920x1080 composition. "
                "For smarter responses, install Prompture or set PROMPTURE_PATH.",
                actions,
            )

        # No match
        if self._prompture_available:
            return "I'm not sure how to help with that. Could you be more specific?", []

        return (
            "I can help with basic commands (list comps, save, create comp). "
            "For full AI chat, install Prompture:\n"
            "  pip install prompture\n"
            "Or set PROMPTURE_PATH to your local Prompture directory.",
            [],
        )

    def _execute_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """Execute an AE action via the file-based command queue."""
        action_type = action.get("type", "")
        params = action.get("params", {})

        try:
            if action_type == "create_comp":
                self.createComp(
                    params.get("name", "New Comp"),
                    compWidth=params.get("width", 1920),
                    compHeight=params.get("height", 1080),
                    duration=params.get("duration", 10),
                    frameRate=params.get("fps", 30),
                )
                return {"success": True, "message": f"Created comp: {params.get('name')}"}

            elif action_type == "edit_text":
                self.editComp(
                    params["comp_name"],
                    params["layer_name"],
                    "Text.Source Text",
                    params["value"],
                )
                return {"success": True, "message": "Text updated"}

            elif action_type == "edit_property":
                self.editComp(
                    params["comp_name"],
                    params["layer_name"],
                    params["property"],
                    params["value"],
                )
                return {"success": True, "message": "Property updated"}

            elif action_type == "set_color":
                hex_value = params.get("hex", "#FFFFFF")
                rgba = self.hexToRGBA(hex_value)
                self.editComp(
                    params["comp_name"],
                    params["layer_name"],
                    params["property"],
                    rgba,
                )
                return {"success": True, "message": f"Color set to {hex_value}"}

            elif action_type == "add_marker":
                self.addMarker(
                    params["comp_name"],
                    params["layer_name"],
                    params.get("name", "marker"),
                    params.get("time", 0),
                )
                return {"success": True, "message": "Marker added"}

            elif action_type == "save_project":
                self.runScript("save_project.jsx")
                return {"success": True, "message": "Project saved"}

            elif action_type == "list_comps":
                self.getProjectMap()
                comps = [item for item in self.afterEffectItems if item.get("type") == "CompItem"]
                return {"success": True, "comps": comps}

            elif action_type == "get_project_info":
                data = self.getProjectMap()
                return {"success": True, "project": data}

            elif action_type == "render":
                project_path = params.get("project_path", "")
                comp_name = params.get("comp_name", "")
                output_dir = params.get("output_dir", "")
                if not project_path or not comp_name or not output_dir:
                    return {"success": False, "error": "render requires project_path, comp_name, and output_dir"}
                output_path = self.renderFileWithProgress(project_path, comp_name, output_dir)
                return {"success": True, "message": f"Render started, output: {output_path}"}

            elif action_type == "run_plugin":
                plugin_name = params.get("name", "")
                if not plugin_name:
                    return {"success": False, "error": "run_plugin requires a 'name' param"}
                self.run_plugin(plugin_name)
                return {"success": True, "message": f"Plugin '{plugin_name}' executed"}

            else:
                return {"success": False, "error": f"Unknown action: {action_type}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def runChatPanel(self, host: str = "127.0.0.1", port: int = 5001) -> None:
        """Start the chat panel backend server."""
        import webbrowser
        from threading import Timer

        from werkzeug.serving import run_simple

        self._init_chat()

        print("\nAE Automation Chat Backend")
        print("=" * 40)
        print(f"Server:    http://{host}:{port}/")
        print(f"Prompture: {'Available' if self._prompture_available else 'Not found'}")
        print("")
        print("The AE panel connects to this server.")
        print(f"Open in browser for testing: http://{host}:{port}/")
        print("Press Ctrl+C to stop.\n")

        Timer(1.5, lambda: webbrowser.open(f"http://{host}:{port}/")).start()
        run_simple(host, port, self.chat_app, use_reloader=False, use_debugger=False)
