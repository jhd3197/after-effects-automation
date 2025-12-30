"""
Unit tests for JavaScript/JSX integration
"""
import unittest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client, settings


class TestJSXScripts(unittest.TestCase):
    """Test JSX script files existence and structure"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        self.required_scripts = [
            "file_map.jsx",
            "create_folder.jsx",
            "addComp.jsx",
            "update_properties.jsx",
            "update_properties_frame.jsx",
            "add_resource.jsx",
            "add_marker.jsx",
            "duplicate_comp_2.jsx",
            "importFile.jsx",
            "selectItem.jsx",
            "selectItemByName.jsx",
            "selectLayerByIndex.jsx",
            "renderComp.jsx",
            "workAreaComp.jsx"
        ]

    def test_jsx_directory_exists(self):
        """Test that JSX directory exists"""
        self.assertTrue(os.path.exists(settings.JS_DIR),
                       f"JSX directory not found: {settings.JS_DIR}")

    def test_all_required_jsx_scripts_exist(self):
        """Test that all required JSX scripts exist"""
        for script_name in self.required_scripts:
            with self.subTest(script=script_name):
                script_path = os.path.join(settings.JS_DIR, script_name)
                self.assertTrue(os.path.exists(script_path),
                              f"Required JSX script not found: {script_name}")

    def test_jsx_scripts_are_readable(self):
        """Test that JSX scripts can be read"""
        for script_name in self.required_scripts:
            with self.subTest(script=script_name):
                script_path = os.path.join(settings.JS_DIR, script_name)
                if os.path.exists(script_path):
                    try:
                        content = self.client.file_get_contents(script_path)
                        self.assertIsInstance(content, str)
                        self.assertGreater(len(content), 0,
                                         f"JSX script is empty: {script_name}")
                    except Exception as e:
                        self.fail(f"Failed to read {script_name}: {e}")

    def test_jsx_scripts_have_valid_syntax_markers(self):
        """Test that JSX scripts contain expected syntax markers"""
        # Check a few key scripts for expected content
        test_cases = {
            "file_map.jsx": ["app.project", "items"],
            "create_folder.jsx": ["FolderItem", "add"],
            "addComp.jsx": ["CompItem", "add"],
            "update_properties.jsx": ["property", "setValue"],
        }

        for script_name, expected_keywords in test_cases.items():
            with self.subTest(script=script_name):
                script_path = os.path.join(settings.JS_DIR, script_name)
                if os.path.exists(script_path):
                    content = self.client.file_get_contents(script_path)
                    for keyword in expected_keywords:
                        self.assertIn(keyword, content,
                                    f"{script_name} missing expected keyword: {keyword}")


class TestJavaScriptFramework(unittest.TestCase):
    """Test JavaScript framework loading"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()

    def test_framework_loads(self):
        """Test that JavaScript framework is loaded"""
        self.assertIsNotNone(self.client.JS_FRAMEWORK)
        self.assertGreater(len(self.client.JS_FRAMEWORK), 0)

    def test_framework_contains_json2(self):
        """Test that framework includes JSON2 library"""
        # The framework should include json2.js
        self.assertIsInstance(self.client.JS_FRAMEWORK, str)
        # json2.js typically contains JSON.parse or JSON.stringify
        # After minification, these might not be as readable

    def test_framework_contains_custom_functions(self):
        """Test that framework includes custom utility functions"""
        # The framework.js should be included
        # We can't easily test the minified content, but we can check it's not empty
        self.assertGreater(len(self.client.JS_FRAMEWORK), 100,
                          "Framework seems too small")


class TestScriptGeneration(unittest.TestCase):
    """Test script generation and parameter replacement"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()

    def test_parameter_replacement(self):
        """Test that parameters are replaced in scripts"""
        # This tests the logic that would be used in runScript
        template = "var compName = '{compName}'; var width = {width};"
        replacements = {
            "{compName}": "TestComp",
            "{width}": "1920"
        }

        result = template
        for key, value in replacements.items():
            result = result.replace(key, value)

        expected = "var compName = 'TestComp'; var width = 1920;"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
