"""
Test configuration and platform helpers
"""
import sys
import unittest

IS_WINDOWS = sys.platform == 'win32'

skip_unless_windows = unittest.skipUnless(IS_WINDOWS, "Requires Windows")
