"""
Unit tests for Client initialization and basic functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


class TestClientInitialization(unittest.TestCase):
    """Test Client class initialization"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = None

    def tearDown(self):
        """Clean up after tests"""
        if self.client:
            del self.client

    def test_client_can_be_instantiated(self):
        """Test that Client can be created"""
        try:
            self.client = Client()
            self.assertIsNotNone(self.client)
        except Exception as e:
            self.fail(f"Client instantiation failed: {e}")

    def test_client_has_js_framework(self):
        """Test that Client loads JavaScript framework"""
        self.client = Client()
        self.assertTrue(hasattr(self.client, "JS_FRAMEWORK"))
        self.assertIsNotNone(self.client.JS_FRAMEWORK)
        self.assertIsInstance(self.client.JS_FRAMEWORK, str)
        self.assertGreater(len(self.client.JS_FRAMEWORK), 0)

    def test_client_has_required_methods(self):
        """Test that Client has all required methods"""
        self.client = Client()

        required_methods = [
            "startAfterEffect",
            "createFolder",
            "createComp",
            "editComp",
            "addCompToTimeline",
            "importFile",
            "renderFile",
            "runScript",
            "slug",
            "hexToRGBA",
            "getFolderItems",
            "searchFolderItems",
            "duplicateFolderItems",
            "applyTemplateValues",
            "addTransition",
        ]

        for method_name in required_methods:
            with self.subTest(method=method_name):
                self.assertTrue(hasattr(self.client, method_name), f"Client missing method: {method_name}")
                self.assertTrue(callable(getattr(self.client, method_name)), f"Client.{method_name} is not callable")


class TestClientCacheFolder(unittest.TestCase):
    """Test cache folder creation"""

    def test_cache_folder_creation(self):
        """Test that cache folder is created"""
        import importlib

        import ae_automation.settings as settings_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            test_cache = os.path.join(tmpdir, "test_cache")
            original_cache = os.environ.get("CACHE_FOLDER")
            os.environ["CACHE_FOLDER"] = test_cache

            try:
                # Reload settings so it picks up the new env var
                importlib.reload(settings_mod)
                # Client should create cache folder on init
                Client()
                self.assertTrue(os.path.exists(test_cache), "Cache folder was not created")
            finally:
                if original_cache:
                    os.environ["CACHE_FOLDER"] = original_cache
                elif "CACHE_FOLDER" in os.environ:
                    del os.environ["CACHE_FOLDER"]
                # Reload again to restore original settings
                importlib.reload(settings_mod)


if __name__ == "__main__":
    unittest.main()
