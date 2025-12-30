"""
After Effects Automation - Compatibility Test Suite
====================================================
Tests package functionality across different After Effects versions.
Reports what works and what doesn't for your specific AE version.

Usage:
    python test.py
    python test.py --version "2024"
    python test.py --verbose
"""

import os
import sys
import json
import tempfile
import traceback
from pathlib import Path
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class TestResult:
    """Store test results"""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.skipped = []
        self.warnings = []
        self.ae_version = "Unknown"

    def add_pass(self, test_name, message=""):
        self.passed.append({"name": test_name, "message": message})

    def add_fail(self, test_name, error):
        self.failed.append({"name": test_name, "error": str(error)})

    def add_skip(self, test_name, reason):
        self.skipped.append({"name": test_name, "reason": reason})

    def add_warning(self, test_name, message):
        self.warnings.append({"name": test_name, "message": message})


class AfterEffectsCompatibilityTest:
    """Test suite for After Effects compatibility"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.result = TestResult()
        self.client = None

    def log(self, message, level="INFO"):
        """Log messages based on verbosity"""
        colors = {
            "INFO": Colors.BLUE,
            "SUCCESS": Colors.GREEN,
            "ERROR": Colors.RED,
            "WARNING": Colors.YELLOW
        }

        if self.verbose or level in ["SUCCESS", "ERROR", "WARNING"]:
            color = colors.get(level, Colors.RESET)
            print(f"{color}{level}: {message}{Colors.RESET}")

    def test_import(self):
        """Test if the package can be imported"""
        try:
            from ae_automation import Client
            self.log("Package import successful", "SUCCESS")
            self.result.add_pass("Package Import", "ae_automation imported successfully")
            return True
        except Exception as e:
            self.log(f"Package import failed: {e}", "ERROR")
            self.result.add_fail("Package Import", e)
            return False

    def test_environment_setup(self):
        """Test environment configuration"""
        try:
            # Check for .env file
            env_path = Path(".env")
            if not env_path.exists():
                self.result.add_warning("Environment File", ".env file not found - using defaults")
                self.log(".env file not found", "WARNING")
            else:
                self.result.add_pass("Environment File", ".env exists")
                self.log(".env file found", "SUCCESS")

            # Check required environment variables
            from ae_automation import settings
            required_vars = ["AFTER_EFFECT_FOLDER", "CACHE_FOLDER"]

            for var in required_vars:
                value = getattr(settings, var, None)
                if value:
                    self.result.add_pass(f"Environment Variable: {var}", f"Set to: {value}")
                    self.log(f"{var} is set to: {value}", "INFO")
                else:
                    self.result.add_fail(f"Environment Variable: {var}", f"{var} not set")
                    self.log(f"{var} is not set", "ERROR")

            return True
        except Exception as e:
            self.log(f"Environment setup test failed: {e}", "ERROR")
            self.result.add_fail("Environment Setup", e)
            return False

    def test_client_initialization(self):
        """Test Client initialization"""
        try:
            from ae_automation import Client
            self.client = Client()
            self.log("Client initialized successfully", "SUCCESS")
            self.result.add_pass("Client Initialization", "Client created successfully")
            return True
        except Exception as e:
            self.log(f"Client initialization failed: {e}", "ERROR")
            self.result.add_fail("Client Initialization", e)
            return False

    def test_javascript_framework_loading(self):
        """Test if JavaScript framework loads correctly"""
        try:
            if self.client and hasattr(self.client, 'JS_FRAMEWORK'):
                if self.client.JS_FRAMEWORK:
                    self.log("JavaScript framework loaded", "SUCCESS")
                    self.result.add_pass("JS Framework Loading", "Framework loaded successfully")
                else:
                    self.log("JavaScript framework is empty", "ERROR")
                    self.result.add_fail("JS Framework Loading", "Framework is empty")
            else:
                self.log("Client not initialized or JS_FRAMEWORK not found", "ERROR")
                self.result.add_fail("JS Framework Loading", "Client or framework not available")
        except Exception as e:
            self.log(f"JS framework loading test failed: {e}", "ERROR")
            self.result.add_fail("JS Framework Loading", e)

    def test_utility_functions(self):
        """Test utility functions"""
        if not self.client:
            self.result.add_skip("Utility Functions", "Client not initialized")
            return

        try:
            # Test slug function
            slug_result = self.client.slug("Test Name 123")
            if slug_result == "test-name-123":
                self.result.add_pass("Slug Function", "Slugify working correctly")
                self.log("Slug function works", "SUCCESS")
            else:
                self.result.add_fail("Slug Function", f"Expected 'test-name-123', got '{slug_result}'")
                self.log(f"Slug function failed: {slug_result}", "ERROR")

            # Test hexToRGBA function
            rgba = self.client.hexToRGBA("#FF0000")
            if "1.0,0.0,0.0,1" in rgba or "1,0,0,1" in rgba:
                self.result.add_pass("HexToRGBA Function", "Color conversion working")
                self.log("HexToRGBA function works", "SUCCESS")
            else:
                self.result.add_fail("HexToRGBA Function", f"Unexpected result: {rgba}")
                self.log(f"HexToRGBA failed: {rgba}", "ERROR")

        except Exception as e:
            self.log(f"Utility functions test failed: {e}", "ERROR")
            self.result.add_fail("Utility Functions", e)

    def test_json_config_parsing(self):
        """Test JSON configuration parsing"""
        try:
            # Create a minimal test configuration
            test_config = {
                "project": {
                    "project_file": "test.aep",
                    "comp_name": "TestComp",
                    "comp_fps": 29.97,
                    "comp_width": 1920,
                    "comp_height": 1080,
                    "auto_time": True,
                    "comp_start_time": "00:00:00",
                    "comp_end_time": 10,
                    "output_file": "test.mp4",
                    "output_dir": tempfile.gettempdir(),
                    "renderComp": False,
                    "debug": True,
                    "resources": []
                },
                "timeline": []
            }

            # Write to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test_config, f)
                temp_file = f.name

            # Try to parse it
            with open(temp_file, 'r') as f:
                data = json.load(f)

            # Cleanup
            os.unlink(temp_file)

            self.log("JSON config parsing works", "SUCCESS")
            self.result.add_pass("JSON Config Parsing", "Configuration parsed successfully")

        except Exception as e:
            self.log(f"JSON config parsing failed: {e}", "ERROR")
            self.result.add_fail("JSON Config Parsing", e)

    def test_after_effects_detection(self):
        """Test After Effects installation detection"""
        try:
            from ae_automation import settings
            ae_path = settings.AFTER_EFFECT_FOLDER

            if not ae_path or not os.path.exists(ae_path):
                self.result.add_warning("After Effects Detection",
                    f"After Effects not found at: {ae_path}")
                self.log(f"After Effects not found at: {ae_path}", "WARNING")
                return False

            # Try to detect version from path
            path_str = str(ae_path)
            for year in range(2020, 2030):
                if str(year) in path_str:
                    self.result.ae_version = str(year)
                    self.log(f"Detected After Effects {year}", "SUCCESS")
                    self.result.add_pass("After Effects Detection",
                        f"Found AE {year} at {ae_path}")
                    return True

            self.result.add_pass("After Effects Detection",
                f"Found at {ae_path} (version unknown)")
            self.log("After Effects found but version unknown", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"After Effects detection failed: {e}", "ERROR")
            self.result.add_fail("After Effects Detection", e)
            return False

    def test_jsx_scripts_existence(self):
        """Test if JSX scripts are available"""
        try:
            from ae_automation import settings

            jsx_scripts = [
                "file_map.jsx",
                "create_folder.jsx",
                "addComp.jsx",
                "update_properties.jsx",
                "add_resource.jsx",
                "duplicate_comp_2.jsx",
                "importFile.jsx",
                "selectItem.jsx"
            ]

            missing_scripts = []
            found_scripts = []

            for script in jsx_scripts:
                script_path = os.path.join(settings.JS_DIR, script)
                if os.path.exists(script_path):
                    found_scripts.append(script)
                else:
                    missing_scripts.append(script)

            if not missing_scripts:
                self.result.add_pass("JSX Scripts", f"All {len(jsx_scripts)} scripts found")
                self.log(f"All {len(jsx_scripts)} JSX scripts found", "SUCCESS")
            else:
                self.result.add_fail("JSX Scripts",
                    f"Missing scripts: {', '.join(missing_scripts)}")
                self.log(f"Missing JSX scripts: {missing_scripts}", "ERROR")

            if found_scripts:
                self.log(f"Found scripts: {', '.join(found_scripts)}", "INFO")

        except Exception as e:
            self.log(f"JSX scripts test failed: {e}", "ERROR")
            self.result.add_fail("JSX Scripts", e)

    def test_dependencies(self):
        """Test if all required dependencies are installed"""
        dependencies = {
            "pyautogui": "GUI automation",
            "pydirectinput": "Direct input",
            "pywinauto": "Windows automation",
            "pandas": "Data handling",
            "pydantic": "Data validation",
            "jsmin": "JavaScript minification",
            "mutagen": "Audio metadata",
            "moviepy": "Video processing",
            "flask": "Web interface",
            "slugify": "String slugification"
        }

        for module, description in dependencies.items():
            try:
                __import__(module)
                self.result.add_pass(f"Dependency: {module}", description)
                self.log(f"{module} installed", "SUCCESS")
            except ImportError:
                self.result.add_fail(f"Dependency: {module}",
                    f"{description} - Module not found")
                self.log(f"{module} not installed", "ERROR")

    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Colors.BOLD}{'='*60}")
        print(f"After Effects Automation - Compatibility Test Suite")
        print(f"{'='*60}{Colors.RESET}\n")

        # Run tests in order
        if not self.test_import():
            print(f"\n{Colors.RED}Cannot continue - package import failed{Colors.RESET}")
            return self.result

        self.test_environment_setup()
        self.test_client_initialization()
        self.test_javascript_framework_loading()
        self.test_utility_functions()
        self.test_json_config_parsing()
        self.test_after_effects_detection()
        self.test_jsx_scripts_existence()
        self.test_dependencies()

        return self.result

    def generate_report(self):
        """Generate a detailed test report"""
        result = self.result

        print(f"\n{Colors.BOLD}{'='*60}")
        print(f"TEST RESULTS SUMMARY")
        print(f"{'='*60}{Colors.RESET}\n")

        if result.ae_version != "Unknown":
            print(f"{Colors.BLUE}After Effects Version: {result.ae_version}{Colors.RESET}\n")

        # Summary
        total = len(result.passed) + len(result.failed) + len(result.skipped)
        print(f"{Colors.GREEN}✓ Passed:  {len(result.passed)}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed:  {len(result.failed)}{Colors.RESET}")
        print(f"{Colors.YELLOW}⊘ Skipped: {len(result.skipped)}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠ Warnings: {len(result.warnings)}{Colors.RESET}")
        print(f"Total Tests: {total}\n")

        # Failed tests details
        if result.failed:
            print(f"{Colors.BOLD}{Colors.RED}FAILED TESTS:{Colors.RESET}")
            for item in result.failed:
                print(f"  ✗ {item['name']}")
                print(f"    {Colors.RED}Error: {item['error']}{Colors.RESET}")
            print()

        # Warnings
        if result.warnings:
            print(f"{Colors.BOLD}{Colors.YELLOW}WARNINGS:{Colors.RESET}")
            for item in result.warnings:
                print(f"  ⚠ {item['name']}")
                print(f"    {Colors.YELLOW}{item['message']}{Colors.RESET}")
            print()

        # Passed tests (only in verbose mode)
        if self.verbose and result.passed:
            print(f"{Colors.BOLD}{Colors.GREEN}PASSED TESTS:{Colors.RESET}")
            for item in result.passed:
                print(f"  ✓ {item['name']}")
                if item['message']:
                    print(f"    {item['message']}")
            print()

        # Compatibility notes
        print(f"{Colors.BOLD}COMPATIBILITY NOTES:{Colors.RESET}")
        if result.ae_version in ["2024", "2025"]:
            print(f"{Colors.GREEN}✓ Your After Effects version is officially supported{Colors.RESET}")
        elif result.ae_version != "Unknown":
            print(f"{Colors.YELLOW}⚠ After Effects {result.ae_version} may work but is not officially tested{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ After Effects not detected - some features require AE to be installed{Colors.RESET}")

        print()

        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.json"

        report_data = {
            "timestamp": timestamp,
            "ae_version": result.ae_version,
            "summary": {
                "passed": len(result.passed),
                "failed": len(result.failed),
                "skipped": len(result.skipped),
                "warnings": len(result.warnings)
            },
            "details": {
                "passed": result.passed,
                "failed": result.failed,
                "skipped": result.skipped,
                "warnings": result.warnings
            }
        }

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"Detailed report saved to: {report_file}\n")

        # Return exit code
        return 0 if len(result.failed) == 0 else 1


def main():
    """Main test runner"""
    import argparse

    parser = argparse.ArgumentParser(description='Test After Effects Automation compatibility')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    parser.add_argument('--version', type=str,
                       help='Specify After Effects version for testing')

    args = parser.parse_args()

    # Run tests
    tester = AfterEffectsCompatibilityTest(verbose=args.verbose)
    tester.run_all_tests()
    exit_code = tester.generate_report()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
