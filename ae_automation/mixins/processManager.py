"""
Process Manager for After Effects
Handles process detection, window waiting, and readiness checks
"""
from __future__ import annotations

import time
import subprocess
import psutil
import os
from ae_automation.logging_config import get_logger
from ae_automation.exceptions import AENotFoundError

logger = get_logger(__name__)

try:
    from pywinauto import Application
except ImportError:
    Application = None

try:
    from pywinauto.timings import wait_until
except ImportError:
    wait_until = None


class ProcessManagerMixin:
    """
    Mixin for managing After Effects process lifecycle
    """

    def wait_for_process(self, process_name: str = "AfterFX.exe", timeout: int = 30) -> psutil.Process | None:
        """
        Wait for a process to start

        Args:
            process_name: Name of the process to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Process object if found, None if timeout
        """
        logger.info("Waiting for %s to start...", process_name)
        start_time = time.time()

        while time.time() - start_time < timeout:
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        logger.info("Process found: %s (PID: %s)", process_name, proc.info['pid'])
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(0.5)

        logger.warning("Timeout waiting for %s", process_name)
        return None

    def wait_for_window(self, window_title_pattern: str = "After Effects", timeout: int = 60) -> bool:
        """
        Wait for After Effects main window to appear

        Args:
            window_title_pattern: Pattern to match window title
            timeout: Maximum time to wait in seconds

        Returns:
            True if window found, False if timeout
        """
        logger.info("Waiting for After Effects window...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Try to connect to any After Effects window
                # This includes Home screen, project windows, etc.
                app = Application(backend="uia").connect(title_re=f".*{window_title_pattern}.*", timeout=5)
                windows = app.windows()

                if len(windows) > 0:
                    logger.info("After Effects window is ready (%d window(s) found)", len(windows))
                    # Give it a moment to fully initialize
                    time.sleep(3)
                    return True
            except Exception as e:
                # Try alternate detection method
                try:
                    import pygetwindow as gw
                    ae_windows = [w for w in gw.getAllWindows() if 'after effects' in w.title.lower()]
                    if ae_windows:
                        logger.info("After Effects window is ready (found via alternate method)")
                        time.sleep(3)
                        return True
                except Exception:
                    pass

            time.sleep(1)

        logger.warning("Timeout waiting for After Effects window")
        return False

    def is_after_effects_responsive(self, max_retries: int = 5) -> bool:
        """
        Check if After Effects is responsive by running a simple script

        Args:
            max_retries: Number of times to retry the test

        Returns:
            True if responsive, False otherwise
        """
        logger.info("Testing if After Effects is responsive...")

        for attempt in range(max_retries):
            try:

                # Run a very simple test script
                test_script = "app.project ? 'ready' : 'no project';"

                from ae_automation import settings
                test_file = os.path.join(settings.CACHE_FOLDER, "_ae_ready_test.jsx")

                with open(test_file, 'w') as f:
                    f.write(test_script)

                ae_path = os.path.join(settings.AFTER_EFFECT_FOLDER, 'AfterFX.exe')

                # Run the test script
                result = subprocess.run(
                    [ae_path, '-s', f"var f = new File('{test_file}'); f.open(); eval(f.read());"],
                    capture_output=True,
                    timeout=10
                )

                # Clean up test file
                if os.path.exists(test_file):
                    os.remove(test_file)

                logger.info("After Effects is responsive (attempt %d)", attempt + 1)
                return True

            except subprocess.TimeoutExpired:
                logger.debug("Attempt %d/%d: Still loading...", attempt + 1, max_retries)
                time.sleep(3)
            except Exception as e:
                logger.debug("Attempt %d/%d: Waiting... (%s)", attempt + 1, max_retries, e)
                time.sleep(3)

        logger.warning("After Effects is not responding")
        return False

    def handle_crash_dialog(self) -> None:
        """
        Check for and handle "Crash Repair Options" / "Safe Mode" dialog
        Presses Space to select the default option (usually Start Normally or Continue)
        """
        try:
            # We blindly send Space/Enter if we suspect a dialog based on timing
            # Ideally we would check for window title "Adobe After Effects" with specific size
            # But just pressing Space is often safe enough during startup
            logger.debug("Checking for Crash/Safe Mode dialog...")
            import pyautogui
            # Focus AE window if possible (optional, might need win32gui)

            # Send Space key to dismiss "Start Safe Mode" dialog or "Crash Repair"
            pyautogui.press('space')
            logger.debug("Sent SPACE key to handle potential dialog")
            time.sleep(1)
        except Exception as e:
            logger.debug("Failed to handle crash dialog: %s", e)

    def wait_for_after_effects_ready(self, timeout: int = 120) -> bool:
        """
        Comprehensive wait for After Effects to be fully loaded and ready

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            True if ready, False if timeout
        """
        logger.info("Waiting for After Effects to be ready...")

        start_time = time.time()

        # Step 1: Wait for process to start
        process = self.wait_for_process("AfterFX.exe", timeout=30)
        if not process:
            return False

        remaining_time = timeout - (time.time() - start_time)
        if remaining_time <= 0:
            logger.warning("Timeout reached")
            return False
            
        # Attempt to handle crash dialog early
        time.sleep(5)
        self.handle_crash_dialog()

        # Step 2: Wait for main window
        if not self.wait_for_window("Adobe After Effects", timeout=int(remaining_time)):
            # Try handling dialog again if window wait fails or takes too long
            self.handle_crash_dialog()
            # Retry wait? No, let's just proceed to plugin wait
        
        # Step 3: Wait a bit more for plugins to load
        logger.info("Waiting for plugins and UI to initialize...")
        time.sleep(5)

        # Step 4: Check if responsive
        if not self.is_after_effects_responsive(max_retries=3):
            # One last try to clear dialogs
            self.handle_crash_dialog()
            if not self.is_after_effects_responsive(max_retries=2):
                return False

        elapsed = time.time() - start_time
        logger.info("After Effects is ready (took %.1fs)", elapsed)

        return True

    def ensure_after_effects_running(self, project_file: str | None = None, timeout: int = 120, skip_home_screen: bool = True) -> bool:
        """
        Ensure After Effects is running and ready, start if needed

        Args:
            project_file: Optional project file to open
            timeout: Maximum time to wait
            skip_home_screen: If True, closes the Home screen automatically

        Returns:
            True if running and ready, False otherwise
        """
        from ae_automation import settings
        settings.validate_settings()
        # Check if already running
        ae_running = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == 'afterfx.exe':
                    ae_running = True
                    logger.info("After Effects is already running")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not ae_running:
            # Start After Effects
            from ae_automation import settings
            ae_path = os.path.join(settings.AFTER_EFFECT_FOLDER, 'AfterFX.exe')

            if project_file and os.path.exists(project_file):
                logger.info("Starting After Effects with project: %s", project_file)
                subprocess.Popen([ae_path, project_file])
            else:
                logger.info("Starting After Effects...")
                # Start AE - it will open with Home screen
                subprocess.Popen([ae_path])

        # Wait for it to be ready
        ready = self.wait_for_after_effects_ready(timeout=timeout)

        return ready

    def wait_for_script_completion(self, timeout: int = 30) -> bool:
        """
        Wait for a script to complete execution

        This is useful after running a script to ensure it finishes
        before running the next one

        Args:
            timeout: Maximum time to wait

        Returns:
            True if completed, False if timeout
        """
        # Check for the existence of a completion marker file
        from ae_automation import settings
        marker_file = os.path.join(settings.CACHE_FOLDER, "_script_complete.txt")

        start_time = time.time()

        # First, remove any existing marker
        if os.path.exists(marker_file):
            os.remove(marker_file)

        while time.time() - start_time < timeout:
            if os.path.exists(marker_file):
                os.remove(marker_file)
                return True
            time.sleep(0.1)

        return False

    def safe_script_execution(self, script_name: str, replacements: dict[str, str] | None = None, wait_time: int = 3) -> bool:
        """
        Execute a script with automatic waiting for completion

        Args:
            script_name: Name of the JSX script
            replacements: Dictionary of replacements
            wait_time: Time to wait after script execution

        Returns:
            True if successful
        """
        logger.info("Executing: %s", script_name)

        # Run the script
        self.runScript(script_name, replacements)

        # Wait for completion
        time.sleep(wait_time)

        return True

    def test_script_execution(self) -> bool:
        """
        Test if After Effects can execute scripts
        Shows an alert dialog in AE if scripts are working

        Returns:
            True if test was sent (check AE for alert dialog)
        """
        print("\n" + "="*60)
        print("Testing Script Execution")
        print("="*60)
        print("Running test script...")
        print("(You should see an alert dialog in After Effects)\n")

        try:
            self.runScript("test_script_execution.jsx")
            time.sleep(3)

            print("Test script sent to After Effects")
            print("\nIMPORTANT: Did you see an alert dialog in After Effects?")
            print("  - If YES: Scripts are working!")
            print("  - If NO: Scripts are NOT executing - check preferences")
            print("="*60 + "\n")
            return True
        except Exception as e:
            logger.error("Failed to run test script: %s", e)
            print("="*60 + "\n")
            return False

    def check_scripting_settings(self) -> bool:
        """
        Check After Effects scripting settings
        Shows a detailed alert dialog in AE with current settings

        Returns:
            True if check was sent (read alert dialog in AE for details)
        """
        print("\n" + "="*60)
        print("Checking Scripting Settings")
        print("="*60)
        print("Running settings check...")
        print("(You should see a detailed alert in After Effects)\n")

        try:
            self.runScript("check_scripting_enabled.jsx")
            time.sleep(3)

            print("Settings check sent to After Effects")
            print("\nRead the alert dialog in After Effects for details")
            print("="*60 + "\n")
            return True
        except Exception as e:
            logger.error("Failed to check settings: %s", e)
            print("="*60 + "\n")
            return False

    def test_composition_creation(self) -> bool:
        """
        Test composition creation with debug alerts
        Shows multiple alert dialogs showing progress

        Returns:
            True if test was sent (check AE for alerts and composition)
        """
        print("\n" + "="*60)
        print("Testing Composition Creation (Debug Mode)")
        print("="*60)
        print("Attempting to create a test composition...")
        print("(You should see multiple alert dialogs showing progress)\n")

        try:
            replacements = {
                "{compName}": "DEBUG_TEST_COMP",
                "{compWidth}": "1920",
                "{compHeight}": "1080",
                "{pixelAspect}": "1",
                "{duration}": "10",
                "{frameRate}": "29.97",
                "{folderName}": ""
            }

            self.runScript("debug_create_comp.jsx", replacements)
            time.sleep(5)

            print("Debug comp creation script sent")
            print("\nCheck After Effects:")
            print("  - Did you see alert dialogs?")
            print("  - Was a composition created?")
            print("  - Check the Project panel for 'DEBUG_TEST_COMP'")
            print("="*60 + "\n")
            return True
        except Exception as e:
            logger.error("Failed to create debug comp: %s", e)
            print("="*60 + "\n")
            return False

    def run_full_diagnostic(self) -> bool:
        """
        Run complete diagnostic suite
        Tests process, window detection, script execution, and settings

        Returns:
            True if diagnostics completed
        """
        print("\n" + "="*60)
        print("After Effects Automation - Full Diagnostic")
        print("="*60 + "\n")

        # Step 1: Check if AE is running
        print("Step 1: Checking After Effects Process")
        print("-" * 60)

        ae_running = False
        ae_pid = None

        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'].lower() == 'afterfx.exe':
                    ae_running = True
                    ae_pid = proc.info['pid']
                    print(f"After Effects is running (PID: {ae_pid})")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not ae_running:
            print("After Effects is not running")
            print("\nStarting After Effects...")

            if not self.ensure_after_effects_running(timeout=120):
                print("Failed to start After Effects")
                return False

        # Step 2: Check window detection
        print("\nStep 2: Checking Window Detection")
        print("-" * 60)

        try:
            import pygetwindow as gw
            ae_windows = [w for w in gw.getAllWindows() if 'after effects' in w.title.lower()]

            if ae_windows:
                print(f"Found {len(ae_windows)} After Effects window(s):")
                for i, window in enumerate(ae_windows, 1):
                    print(f"  {i}. {window.title}")
            else:
                print("No After Effects windows found")
        except Exception as e:
            print(f"Could not detect windows: {e}")

        # Step 3: Test script execution
        self.test_script_execution()

        # Step 4: Check scripting settings
        self.check_scripting_settings()

        # Step 5: Test composition creation
        self.test_composition_creation()

        # Summary
        print("\n" + "="*60)
        print("Summary and Recommendations")
        print("="*60 + "\n")

        print("If you saw alert dialogs:")
        print("  ✓ Scripts ARE executing - the system is working!")
        print("  ✓ Check After Effects for the created items")
        print("")
        print("If you did NOT see alert dialogs:")
        print("  ✗ Scripts are NOT executing properly")
        print("")
        print("  Common fixes:")
        print("  1. Enable scripting in After Effects:")
        print("     Edit > Preferences > Scripting & Expressions")
        print("     ☑ Allow Scripts to Write Files and Access Network")
        print("")
        print("  2. Restart After Effects after enabling")
        print("")
        print("  3. Check that After Effects is not showing any error dialogs")
        print("")
        print("  4. Try running After Effects as Administrator")
        print("")
        print("  5. Check antivirus isn't blocking script execution")
        print("")

        print("="*60)
        print("Next Steps")
        print("="*60 + "\n")

        print("1. Review the alert dialogs in After Effects")
        print("2. If scripting is disabled, enable it and restart AE")
        print("3. Run diagnostics again: ae-automation diagnose")
        print("4. Once scripts work, try: ae-automation generate --template tutorial")
        print("")

        return True
