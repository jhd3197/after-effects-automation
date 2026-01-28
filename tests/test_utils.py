"""
Unit tests for utility functions
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()

    def test_slug_function(self):
        """Test slug function for creating URL-safe strings"""
        test_cases = [
            ("Hello World", "hello-world"),
            ("Test Name 123", "test-name-123"),
            ("Special@#$Characters", "specialcharacters"),
            ("Multiple   Spaces", "multiple-spaces"),
            ("UPPERCASE", "uppercase"),
            ("Scene 1", "scene-1"),
        ]

        for input_str, expected_output in test_cases:
            with self.subTest(input=input_str):
                result = self.client.slug(input_str)
                self.assertEqual(
                    result, expected_output, f"slug('{input_str}') returned '{result}', expected '{expected_output}'"
                )

    def test_hex_to_rgba_function(self):
        """Test hexToRGBA color conversion"""
        test_cases = [
            ("#FF0000", ("1.0", "0.0", "0.0")),  # Red
            ("#00FF00", ("0.0", "1.0", "0.0")),  # Green
            ("#0000FF", ("0.0", "0.0", "1.0")),  # Blue
            ("#FFFFFF", ("1.0", "1.0", "1.0")),  # White
            ("#000000", ("0.0", "0.0", "0.0")),  # Black
        ]

        for hex_color, expected_rgb in test_cases:
            with self.subTest(hex=hex_color):
                result = self.client.hexToRGBA(hex_color)
                # Check if result contains expected RGB values
                for expected_value in expected_rgb:
                    self.assertIn(
                        expected_value,
                        result,
                        f"hexToRGBA('{hex_color}') = '{result}' doesn't contain '{expected_value}'",
                    )
                # Check if result ends with ,1 (alpha)
                self.assertTrue(result.endswith(",1"), f"hexToRGBA('{hex_color}') should end with ',1' for alpha")

    def test_file_get_contents(self):
        """Test file_get_contents function"""
        import tempfile

        # Create a temporary file with known content
        test_content = "This is test content\nLine 2\nLine 3"

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(test_content)
            temp_file = f.name

        try:
            result = self.client.file_get_contents(temp_file)
            self.assertEqual(result, test_content, "file_get_contents did not return correct content")
        finally:
            import os

            os.unlink(temp_file)


@unittest.skipUnless(sys.platform == "win32", "Requires Windows (uses TASKLIST command)")
class TestProcessChecking(unittest.TestCase):
    """Test process checking utilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()

    def test_process_exists_with_nonexistent_process(self):
        """Test process_exists with a process that doesn't exist"""
        # Use a process name that almost certainly doesn't exist
        result = self.client.process_exists("nonexistent_process_12345.exe")
        self.assertFalse(result, "process_exists should return False for nonexistent process")

    def test_process_exists_with_system_process(self):
        """Test process_exists with a known Windows system process"""
        # Test with a common Windows process
        result = self.client.process_exists("explorer.exe")
        # This might be True or False depending on the system state
        self.assertIsInstance(result, bool, "process_exists should return a boolean")


class TestSanitizeText(unittest.TestCase):
    """Test sanitize_text_for_ae method"""

    def setUp(self):
        self.client = Client()

    def test_br_lowercase(self):
        result = self.client.sanitize_text_for_ae("Hello<br>World")
        self.assertEqual(result, "Hello\rWorld")

    def test_br_uppercase(self):
        result = self.client.sanitize_text_for_ae("Hello<BR>World")
        self.assertEqual(result, "Hello\rWorld")

    def test_br_self_closing(self):
        result = self.client.sanitize_text_for_ae("Hello<br/>World")
        self.assertEqual(result, "Hello\rWorld")

    def test_br_self_closing_uppercase(self):
        result = self.client.sanitize_text_for_ae("Hello<BR/>World")
        self.assertEqual(result, "Hello\rWorld")

    def test_br_self_closing_space(self):
        result = self.client.sanitize_text_for_ae("Hello<br />World")
        self.assertEqual(result, "Hello\rWorld")

    def test_br_self_closing_space_uppercase(self):
        result = self.client.sanitize_text_for_ae("Hello<BR />World")
        self.assertEqual(result, "Hello\rWorld")

    def test_multiple_br_tags(self):
        result = self.client.sanitize_text_for_ae("Line1<br>Line2<BR/>Line3")
        self.assertEqual(result, "Line1\rLine2\rLine3")

    def test_non_string_int(self):
        result = self.client.sanitize_text_for_ae(42)
        self.assertEqual(result, 42)

    def test_non_string_none(self):
        result = self.client.sanitize_text_for_ae(None)
        self.assertIsNone(result)

    def test_non_string_list(self):
        result = self.client.sanitize_text_for_ae([1, 2, 3])
        self.assertEqual(result, [1, 2, 3])

    def test_empty_string(self):
        result = self.client.sanitize_text_for_ae("")
        self.assertEqual(result, "")

    def test_text_without_br_unchanged(self):
        text = "Hello World, no line breaks here!"
        result = self.client.sanitize_text_for_ae(text)
        self.assertEqual(result, text)


if __name__ == "__main__":
    unittest.main()
