"""
Custom exception classes for After Effects Automation.

Hierarchy:
    AEAutomationError (base)
    ├── AENotFoundError        -- AE installation not found
    ├── AENotResponsiveError   -- AE launched but not responding
    ├── ScriptExecutionError   -- JSX script failed to execute
    ├── RenderError            -- aerender failed
    └── ConfigValidationError  -- Invalid JSON config or settings
"""


class AEAutomationError(Exception):
    """Base exception for all After Effects Automation errors."""


class AENotFoundError(AEAutomationError):
    """After Effects installation or executable not found."""

    def __init__(self, path=None, message=None):
        if message is None:
            message = "After Effects installation not found"
            if path:
                message += f": {path}"
        self.path = path
        super().__init__(message)


class AENotResponsiveError(AEAutomationError):
    """After Effects launched but is not responding to commands."""

    def __init__(self, timeout=None, message=None):
        if message is None:
            message = "After Effects is not responding"
            if timeout is not None:
                message += f" (waited {timeout}s)"
        self.timeout = timeout
        super().__init__(message)


class ScriptExecutionError(AEAutomationError):
    """A JSX script failed to execute in After Effects."""

    def __init__(self, script_name=None, detail=None, message=None):
        if message is None:
            message = "Script execution failed"
            if script_name:
                message += f": {script_name}"
            if detail:
                message += f" -- {detail}"
        self.script_name = script_name
        self.detail = detail
        super().__init__(message)


class RenderError(AEAutomationError):
    """aerender failed or produced no output."""

    def __init__(self, project_path=None, comp_name=None, detail=None, message=None):
        if message is None:
            message = "Render failed"
            if comp_name:
                message += f" for composition '{comp_name}'"
            if project_path:
                message += f" in project '{project_path}'"
            if detail:
                message += f": {detail}"
        self.project_path = project_path
        self.comp_name = comp_name
        self.detail = detail
        super().__init__(message)


class ConfigValidationError(AEAutomationError):
    """Invalid JSON configuration or missing settings."""

    def __init__(self, field=None, detail=None, message=None):
        if message is None:
            message = "Configuration validation failed"
            if field:
                message += f" for '{field}'"
            if detail:
                message += f": {detail}"
        self.field = field
        self.detail = detail
        super().__init__(message)
