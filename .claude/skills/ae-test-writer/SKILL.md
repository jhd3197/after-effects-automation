---
name: ae-test-writer
description: Write unit tests following the project's existing patterns and conventions
---

# AE Test Writer

This skill covers writing tests for the After Effects automation project. Tests use Python's built-in `unittest` framework and live in the `tests/` directory.

## Test File Boilerplate

Every test file follows this exact import pattern:

```python
"""
Test description
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


class TestMyFeature(unittest.TestCase):
    """Tests for [feature description]."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()

    def test_something(self):
        """Test that something works correctly."""
        result = self.client.someMethod()
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
```

Key points:
- The `sys.path.insert` is required because tests run from the repo root
- Always import `Client` from `ae_automation`, not individual mixins
- Tests are organized by feature, not by mixin

## Client Instantiation

The `Client()` constructor is lightweight -- it does NOT launch After Effects. It only:
- Loads settings
- Creates cache/queue folders if missing
- Reads `json2.js` and `framework.js` into `JS_FRAMEWORK`

This means **every test class can safely create a Client in `setUp()`** without needing AE installed:

```python
def setUp(self):
    self.client = Client()
```

Some test classes also include teardown:

```python
def setUp(self):
    self.client = None
    self.client = Client()

def tearDown(self):
    del self.client
```

## Platform Skip Decorators

For tests that require Windows-specific functionality (e.g., process checking via `TASKLIST`, AE interaction):

```python
@unittest.skipUnless(sys.platform == 'win32', "Requires Windows")
class TestWindowsFeature(unittest.TestCase):
    ...
```

The project also has a shared decorator in `tests/conftest.py`:

```python
from tests.conftest import skip_unless_windows

@skip_unless_windows
class TestWindowsFeature(unittest.TestCase):
    ...
```

Use the inline `@unittest.skipUnless` for clarity, or import from `conftest.py` for consistency with existing tests.

## Mock-Based Integration Tests

For testing flows that would normally interact with After Effects, use `unittest.mock`:

```python
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


class TestBotFlow(unittest.TestCase):
    """Test bot flow without launching After Effects."""

    def setUp(self):
        self.client = Client()

    @patch.object(Client, 'startAfterEffect')
    def test_startbot_calls_start_after_effect(self, mock_start):
        """Verify startBot delegates to startAfterEffect."""
        import json
        import tempfile
        import os

        config = {
            "project": {
                "project_file": "test.aep",
                "comp_name": "TestComp",
                "comp_fps": 30,
                "comp_width": 1920,
                "comp_height": 1080,
                "output_file": "out.mp4",
                "output_dir": ".",
                "debug": True
            },
            "timeline": []
        }

        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        try:
            json.dump(config, tmp)
            tmp.close()
            self.client.startBot(tmp.name)
            mock_start.assert_called_once()
        finally:
            os.unlink(tmp.name)
```

### What to mock

- `Client.startAfterEffect` -- prevents AE launch
- `Client.runScript` -- prevents JSX execution
- `Client._execute_script_in_running_ae` -- prevents queue writes
- `Client.process_exists` -- avoids Windows TASKLIST dependency
- Any method that interacts with the filesystem or AE process

## subTest Pattern for Parameterized Tests

Use `self.subTest()` when testing multiple inputs with the same assertion logic:

```python
def test_slugify_various_inputs(self):
    """Test slug generation with various inputs."""
    test_cases = [
        ("Hello World", "hello-world"),
        ("Test_Case", "test_case"),
        ("UPPER case", "upper-case"),
        ("special!@#chars", "specialchars"),
    ]
    for input_str, expected in test_cases:
        with self.subTest(input=input_str):
            result = self.client.slug(input_str)
            self.assertEqual(result, expected)

def test_hex_to_rgba_colors(self):
    """Test hex color conversion to RGBA."""
    test_cases = [
        ("#FF0000", "1.0,0.0,0.0,1"),
        ("#00FF00", "0.0,1.0,0.0,1"),
        ("#0000FF", "0.0,0.0,1.0,1"),
    ]
    for hex_color, expected in test_cases:
        with self.subTest(hex=hex_color):
            result = self.client.hexToRGBA(hex_color)
            self.assertEqual(result, expected)
```

Each `subTest` runs independently -- a failure in one doesn't stop the others, and the failure message includes the `subTest` parameters.

## Config Helper Pattern

Create a helper function for building test configs with sensible defaults:

```python
def create_test_config(**overrides):
    """Create a test configuration with defaults."""
    config = {
        "project": {
            "project_file": "test.aep",
            "comp_name": "TestComp",
            "comp_fps": 30,
            "comp_width": 1920,
            "comp_height": 1080,
            "output_file": "output.mp4",
            "output_dir": "./output",
            "renderComp": False,
            "debug": True,
            "resources": []
        },
        "timeline": []
    }
    config["project"].update(overrides)
    return config
```

Usage:

```python
def test_custom_fps(self):
    config = create_test_config(comp_fps=60)
    self.assertEqual(config["project"]["comp_fps"], 60)

def test_debug_mode(self):
    config = create_test_config(debug=False)
    self.assertFalse(config["project"]["debug"])
```

Place the helper at the module level (outside any class) so all test classes in the file can use it.

## What to Test vs. What NOT to Test

### DO test (pure logic, no AE needed):

- **Utility functions:** `slug()`, `hexToRGBA()`, `sanitize_text_for_ae()`, `file_get_contents()`
- **Config parsing:** Loading JSON, field validation, time format conversion
- **Text sanitization:** HTML br replacement, quote handling
- **Path handling:** Forward slash conversion, relative path resolution
- **Data structure construction:** Replacement dicts, config merging
- **JSX template validation:** That `.jsx` files exist and contain expected placeholders
- **Method existence:** That expected methods are available on the Client

### DO NOT test directly (requires running AE):

- `runScript()` execution results
- Composition creation/modification
- Rendering output
- AE process management (on non-Windows)
- File-based queue communication

For AE-dependent flows, use mocks (see mock section above).

## Temp File Cleanup

When tests create temporary files, always clean up with `try/finally`:

```python
def test_config_loading(self):
    """Test loading a config from a temp file."""
    import tempfile
    import json
    import os

    config = create_test_config()
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    )
    try:
        json.dump(config, tmp)
        tmp.close()

        # Test the actual functionality
        loaded = self.client.startBot(tmp.name)
        # ... assertions ...
    finally:
        os.unlink(tmp.name)
```

Do NOT rely on `tearDown` for temp file cleanup -- if `setUp` or the test itself fails before creating the file reference, `tearDown` would crash.

## Test Class Naming and File Organization

### File naming
- `test_<feature>.py` -- e.g., `test_client.py`, `test_utils.py`, `test_config.py`
- Group related tests in one file

### Class naming
- `Test<Feature><Aspect>` -- e.g., `TestClientInitialization`, `TestConfigurationParsing`, `TestUtilityFunctions`
- Multiple test classes per file is normal and encouraged

### Method naming
- `test_<what_is_being_tested>` -- e.g., `test_slug_basic`, `test_hex_to_rgba_red`
- Be descriptive; the method name should explain what's being verified

### Existing test file inventory

| File | Classes | What it tests |
|------|---------|---------------|
| `test_client.py` | `TestClientInitialization`, `TestClientCacheFolder` | Client construction, attribute availability |
| `test_config.py` | `TestConfigurationParsing`, `TestTimeFormatParsing` | Config loading, field validation, time format parsing |
| `test_jsx_integration.py` | `TestJSXScripts`, `TestJavaScriptFramework`, `TestScriptGeneration` | JSX file existence, framework function detection, placeholder validation |
| `test_utils.py` | `TestUtilityFunctions`, `TestProcessChecking`, `TestSanitizeText` | slug, hexToRGBA, process_exists, sanitize_text_for_ae |
| `test_integration.py` | `TestCheckIfItemExists`, `TestGetResourceDuration`, `TestStartBotFlow` | Mock-based integration tests |

## Run Commands

```bash
# Run all tests
python -m unittest discover tests -v

# Run a specific test file
python -m unittest tests.test_client -v

# Run a specific test class
python -m unittest tests.test_client.TestClientInitialization -v

# Run a specific test method
python -m unittest tests.test_client.TestClientInitialization.test_client_creation -v
```

## Complete Example: New Test File

```python
"""
Tests for layer visibility toggle feature.
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


def create_test_config(**overrides):
    """Create a test configuration with defaults."""
    config = {
        "project": {
            "project_file": "test.aep",
            "comp_name": "TestComp",
            "comp_fps": 30,
            "comp_width": 1920,
            "comp_height": 1080,
            "output_file": "output.mp4",
            "output_dir": "./output",
            "renderComp": False,
            "debug": True,
            "resources": []
        },
        "timeline": []
    }
    config["project"].update(overrides)
    return config


class TestToggleVisibility(unittest.TestCase):
    """Tests for the layer visibility toggle feature."""

    def setUp(self):
        self.client = Client()

    @patch.object(Client, 'runScript')
    def test_toggle_visibility_calls_runscript(self, mock_run):
        """Verify toggleLayerVisibility calls runScript with correct args."""
        self.client.toggleLayerVisibility("MyComp", "Layer1", True)
        mock_run.assert_called_once()
        args = mock_run.call_args
        self.assertEqual(args[0][0], "toggle_layer_visibility.jsx")
        replacements = args[0][1]
        self.assertEqual(replacements["{comp_name}"], "MyComp")
        self.assertEqual(replacements["{layer_name}"], "Layer1")
        self.assertEqual(replacements["{visible}"], "true")

    @patch.object(Client, 'runScript')
    def test_toggle_visibility_false(self, mock_run):
        """Verify visible=False passes 'false' to JSX."""
        self.client.toggleLayerVisibility("MyComp", "Layer1", False)
        args = mock_run.call_args
        replacements = args[0][1]
        self.assertEqual(replacements["{visible}"], "false")

    def test_replacement_dict_keys_have_braces(self):
        """Verify replacement dict keys include braces."""
        # This tests the convention, not execution
        replacements = {
            "{comp_name}": "test",
            "{layer_name}": "test",
            "{visible}": "true",
        }
        for key in replacements:
            with self.subTest(key=key):
                self.assertTrue(
                    key.startswith("{") and key.endswith("}"),
                    f"Key '{key}' must be wrapped in braces"
                )


class TestToggleVisibilityConfig(unittest.TestCase):
    """Tests for toggle_visibility config parsing."""

    def setUp(self):
        self.client = Client()

    def test_config_with_visibility_action(self):
        """Test that toggle_visibility action has required fields."""
        action = {
            "change_type": "toggle_visibility",
            "comp_name": "IntroTemplate",
            "layer_name": "Watermark",
            "visible": False,
        }
        required_fields = ["change_type", "comp_name", "layer_name"]
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, action)


if __name__ == '__main__':
    unittest.main()
```
