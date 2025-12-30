"""
Process Manager for After Effects
Handles process detection, window waiting, and readiness checks
"""
import time
import subprocess
import psutil
import os
from pywinauto import Application
from pywinauto.timings import wait_until


class ProcessManagerMixin:
    """
    Mixin for managing After Effects process lifecycle
    """

    def wait_for_process(self, process_name="AfterFX.exe", timeout=30):
        """
        Wait for a process to start

        Args:
            process_name: Name of the process to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Process object if found, None if timeout
        """
        print(f"Waiting for {process_name} to start...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        print(f"✓ Process found: {process_name} (PID: {proc.info['pid']})")
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(0.5)

        print(f"✗ Timeout waiting for {process_name}")
        return None

    def wait_for_window(self, window_title_pattern="After Effects", timeout=60):
        """
        Wait for After Effects main window to appear

        Args:
            window_title_pattern: Pattern to match window title
            timeout: Maximum time to wait in seconds

        Returns:
            True if window found, False if timeout
        """
        print(f"Waiting for After Effects window...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Try to connect to any After Effects window
                # This includes Home screen, project windows, etc.
                app = Application(backend="uia").connect(title_re=f".*{window_title_pattern}.*", timeout=5)
                windows = app.windows()

                if len(windows) > 0:
                    print(f"✓ After Effects window is ready ({len(windows)} window(s) found)")
                    # Give it a moment to fully initialize
                    time.sleep(3)
                    return True
            except Exception as e:
                # Try alternate detection method
                try:
                    import pygetwindow as gw
                    ae_windows = [w for w in gw.getAllWindows() if 'after effects' in w.title.lower()]
                    if ae_windows:
                        print(f"✓ After Effects window is ready (found via alternate method)")
                        time.sleep(3)
                        return True
                except:
                    pass

            time.sleep(1)

        print(f"✗ Timeout waiting for After Effects window")
        return False

    def close_home_screen(self):
        """
        Close the Home screen (Quick Start) if it's open
        After Effects 2024/2025 opens with a Home screen by default

        Returns:
            True if successful
        """
        print("Checking for Home screen...")

        try:
            # Run script to close home screen and ensure we're on a project
            self.runScript("close_home_screen.jsx")
            time.sleep(2)
            print("✓ Home screen handled")
            return True
        except Exception as e:
            print(f"  Note: Could not close home screen: {e}")
            return False

    def is_after_effects_responsive(self, max_retries=5):
        """
        Check if After Effects is responsive by running a simple script

        Args:
            max_retries: Number of times to retry the test

        Returns:
            True if responsive, False otherwise
        """
        print("Testing if After Effects is responsive...")

        for attempt in range(max_retries):
            try:
                # First, try to close the home screen
                if attempt == 0:
                    self.close_home_screen()

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

                print(f"✓ After Effects is responsive (attempt {attempt + 1})")
                return True

            except subprocess.TimeoutExpired:
                print(f"  Attempt {attempt + 1}/{max_retries}: Still loading...")
                time.sleep(3)
            except Exception as e:
                print(f"  Attempt {attempt + 1}/{max_retries}: Waiting...")
                time.sleep(3)

        print("✗ After Effects is not responding")
        return False

    def wait_for_after_effects_ready(self, timeout=120):
        """
        Comprehensive wait for After Effects to be fully loaded and ready

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            True if ready, False if timeout
        """
        print("\n" + "="*60)
        print("Waiting for After Effects to be ready...")
        print("="*60)

        start_time = time.time()

        # Step 1: Wait for process to start
        process = self.wait_for_process("AfterFX.exe", timeout=30)
        if not process:
            return False

        remaining_time = timeout - (time.time() - start_time)
        if remaining_time <= 0:
            print("✗ Timeout reached")
            return False

        # Step 2: Wait for main window
        if not self.wait_for_window("Adobe After Effects", timeout=int(remaining_time)):
            return False

        remaining_time = timeout - (time.time() - start_time)
        if remaining_time <= 0:
            print("✗ Timeout reached")
            return False

        # Step 3: Wait a bit more for plugins to load
        print("Waiting for plugins and UI to initialize...")
        time.sleep(5)

        # Step 4: Check if responsive
        if not self.is_after_effects_responsive(max_retries=3):
            return False

        elapsed = time.time() - start_time
        print("="*60)
        print(f"✓ After Effects is ready! (took {elapsed:.1f}s)")
        print("="*60 + "\n")

        return True

    def ensure_after_effects_running(self, project_file=None, timeout=120, skip_home_screen=True):
        """
        Ensure After Effects is running and ready, start if needed

        Args:
            project_file: Optional project file to open
            timeout: Maximum time to wait
            skip_home_screen: If True, closes the Home screen automatically

        Returns:
            True if running and ready, False otherwise
        """
        # Check if already running
        ae_running = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == 'afterfx.exe':
                    ae_running = True
                    print("After Effects is already running")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not ae_running:
            # Start After Effects
            from ae_automation import settings
            ae_path = os.path.join(settings.AFTER_EFFECT_FOLDER, 'AfterFX.exe')

            if project_file and os.path.exists(project_file):
                print(f"Starting After Effects with project: {project_file}")
                subprocess.Popen([ae_path, project_file])
            else:
                print("Starting After Effects...")
                # Start AE - it will open with Home screen
                subprocess.Popen([ae_path])

        # Wait for it to be ready
        ready = self.wait_for_after_effects_ready(timeout=timeout)

        # Close home screen if requested
        if ready and skip_home_screen:
            print("Ensuring we're past the Home screen...")
            self.close_home_screen()
            time.sleep(2)

        return ready

    def wait_for_script_completion(self, timeout=30):
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

    def safe_script_execution(self, script_name, replacements=None, wait_time=3):
        """
        Execute a script with automatic waiting for completion

        Args:
            script_name: Name of the JSX script
            replacements: Dictionary of replacements
            wait_time: Time to wait after script execution

        Returns:
            True if successful
        """
        print(f"Executing: {script_name}")

        # Run the script
        self.runScript(script_name, replacements)

        # Wait for completion
        time.sleep(wait_time)

        return True
