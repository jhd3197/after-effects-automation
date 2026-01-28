"""
Unit tests for custom exception classes and logging configuration.
"""

import logging
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation.exceptions import (
    AEAutomationError,
    AENotFoundError,
    AENotResponsiveError,
    ConfigValidationError,
    RenderError,
    ScriptExecutionError,
)
from ae_automation.logging_config import get_logger, setup_logging


class TestExceptionHierarchy(unittest.TestCase):
    """All custom exceptions inherit from AEAutomationError."""

    def test_base_class(self):
        for cls in (AENotFoundError, AENotResponsiveError, ScriptExecutionError, RenderError, ConfigValidationError):
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, AEAutomationError))
                self.assertTrue(issubclass(cls, Exception))


class TestAENotFoundError(unittest.TestCase):
    def test_default_message(self):
        err = AENotFoundError()
        self.assertIn("not found", str(err))

    def test_with_path(self):
        err = AENotFoundError(path="/some/path")
        self.assertEqual(err.path, "/some/path")
        self.assertIn("/some/path", str(err))

    def test_custom_message(self):
        err = AENotFoundError(message="custom msg")
        self.assertEqual(str(err), "custom msg")


class TestAENotResponsiveError(unittest.TestCase):
    def test_default_message(self):
        err = AENotResponsiveError()
        self.assertIn("not responding", str(err))

    def test_with_timeout(self):
        err = AENotResponsiveError(timeout=120)
        self.assertEqual(err.timeout, 120)
        self.assertIn("120", str(err))


class TestScriptExecutionError(unittest.TestCase):
    def test_default_message(self):
        err = ScriptExecutionError()
        self.assertIn("Script execution failed", str(err))

    def test_with_script_name(self):
        err = ScriptExecutionError(script_name="addComp.jsx")
        self.assertEqual(err.script_name, "addComp.jsx")
        self.assertIn("addComp.jsx", str(err))

    def test_with_detail(self):
        err = ScriptExecutionError(script_name="test.jsx", detail="syntax error")
        self.assertIn("syntax error", str(err))
        self.assertEqual(err.detail, "syntax error")


class TestRenderError(unittest.TestCase):
    def test_default_message(self):
        err = RenderError()
        self.assertIn("Render failed", str(err))

    def test_with_all_params(self):
        err = RenderError(project_path="p.aep", comp_name="Intro", detail="exit code 1")
        self.assertEqual(err.project_path, "p.aep")
        self.assertEqual(err.comp_name, "Intro")
        self.assertIn("Intro", str(err))
        self.assertIn("p.aep", str(err))
        self.assertIn("exit code 1", str(err))


class TestConfigValidationError(unittest.TestCase):
    def test_default_message(self):
        err = ConfigValidationError()
        self.assertIn("validation failed", str(err))

    def test_with_field(self):
        err = ConfigValidationError(field="project_file", detail="missing")
        self.assertEqual(err.field, "project_file")
        self.assertIn("project_file", str(err))
        self.assertIn("missing", str(err))


class TestExceptionsAreCatchable(unittest.TestCase):
    """Verify that catching AEAutomationError catches all subtypes."""

    def test_catch_base(self):
        for cls in (AENotFoundError, AENotResponsiveError, ScriptExecutionError, RenderError, ConfigValidationError):
            with self.subTest(cls=cls.__name__):
                with self.assertRaises(AEAutomationError):
                    raise cls()


class TestLoggingSetup(unittest.TestCase):
    def test_get_logger_returns_logger(self):
        lg = get_logger("ae_automation.test")
        self.assertIsInstance(lg, logging.Logger)

    def test_setup_logging_debug(self):
        setup_logging(level=logging.DEBUG)
        root = logging.getLogger("ae_automation")
        self.assertEqual(root.level, logging.DEBUG)

    def test_setup_logging_from_env(self):
        original = os.environ.get("AE_LOG_LEVEL")
        os.environ["AE_LOG_LEVEL"] = "WARNING"
        try:
            setup_logging(level=None)
            root = logging.getLogger("ae_automation")
            self.assertEqual(root.level, logging.WARNING)
        finally:
            if original is None:
                os.environ.pop("AE_LOG_LEVEL", None)
            else:
                os.environ["AE_LOG_LEVEL"] = original
            # Reset to INFO for other tests
            setup_logging(level=logging.INFO)

    def test_setup_logging_default_is_info(self):
        original = os.environ.pop("AE_LOG_LEVEL", None)
        try:
            setup_logging(level=None)
            root = logging.getLogger("ae_automation")
            self.assertEqual(root.level, logging.INFO)
        finally:
            if original is not None:
                os.environ["AE_LOG_LEVEL"] = original


class TestSettingsUsesCustomExceptions(unittest.TestCase):
    """Verify settings.validate_settings raises custom exceptions."""

    def test_validate_settings_raises_ae_not_found(self):
        from ae_automation import settings

        original = settings.AFTER_EFFECT_FOLDER
        settings.AFTER_EFFECT_FOLDER = "/nonexistent/path/to/ae"
        try:
            with self.assertRaises(AENotFoundError):
                settings.validate_settings()
        finally:
            settings.AFTER_EFFECT_FOLDER = original


if __name__ == "__main__":
    unittest.main()
