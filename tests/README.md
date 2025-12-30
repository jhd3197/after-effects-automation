# After Effects Automation - Test Suite

This directory contains unit tests for the After Effects Automation package.

## Running Tests

### Run all tests:
```bash
python -m unittest discover tests
```

### Run specific test file:
```bash
python -m unittest tests.test_client
python -m unittest tests.test_utils
python -m unittest tests.test_config
python -m unittest tests.test_jsx_integration
```

### Run specific test class:
```bash
python -m unittest tests.test_client.TestClientInitialization
```

### Run specific test method:
```bash
python -m unittest tests.test_client.TestClientInitialization.test_client_can_be_instantiated
```

### Run with verbose output:
```bash
python -m unittest discover tests -v
```

## Test Files

### `test_client.py`
Tests for Client initialization and basic functionality:
- Client instantiation
- JavaScript framework loading
- Required methods existence
- Cache folder creation

### `test_utils.py`
Tests for utility functions:
- String slugification
- Hex to RGBA color conversion
- File reading
- Process checking

### `test_config.py`
Tests for JSON configuration parsing:
- Configuration structure validation
- Required fields checking
- Resource handling
- Timeline parsing
- Custom actions
- Time format conversion

### `test_jsx_integration.py`
Tests for JavaScript/JSX integration:
- JSX script file existence
- Script readability
- Syntax validation
- Framework loading
- Parameter replacement

## Requirements

Tests require the package to be installed:
```bash
pip install -e .
```

Or install test dependencies:
```bash
pip install -r requirements.txt
```

## Continuous Integration

These tests are designed to run in CI/CD environments without requiring After Effects to be installed. Tests that require After Effects will be skipped or will test only the Python-side logic.

## Coverage

To run with coverage:
```bash
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html
```

Then open `htmlcov/index.html` in a browser to see detailed coverage.

## Version Compatibility

These tests are version-agnostic and should work with:
- After Effects 2024
- After Effects 2025
- Other CC versions (with potential warnings)

For version-specific compatibility testing, see the main `test.py` file in the root directory.
