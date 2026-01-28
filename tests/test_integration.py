"""
Mock-based integration tests that verify orchestration without After Effects
"""
import unittest
import json
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation import Client


class TestCheckIfItemExists(unittest.TestCase):
    """Test checkIfItemExists logic"""

    def setUp(self):
        self.client = Client()

    def test_returns_true_when_item_not_in_list(self):
        """Returns True (needs creation) when item is not in the list"""
        self.client.afterEffectItems = [
            {"name": "Folder1", "id": 1},
            {"name": "Folder2", "id": 2},
        ]
        result = self.client.checkIfItemExists("NewItem")
        self.assertTrue(result)

    def test_returns_false_when_item_found(self):
        """Returns False (already exists) when item is found"""
        self.client.afterEffectItems = [
            {"name": "Folder1", "id": 1},
            {"name": "MyComp", "id": 2},
        ]
        result = self.client.checkIfItemExists("MyComp")
        self.assertFalse(result)

    def test_empty_list(self):
        """Returns True when item list is empty"""
        self.client.afterEffectItems = []
        result = self.client.checkIfItemExists("Anything")
        self.assertTrue(result)


class TestGetResourceDuration(unittest.TestCase):
    """Test getResourceDuration logic"""

    def setUp(self):
        self.client = Client()

    def test_returns_correct_duration(self):
        """Returns correct float duration for a known resource"""
        self.client.afterEffectResource = [
            {"name": "audio1", "duration": 10.5},
            {"name": "audio2", "duration": 22.3},
        ]
        result = self.client.getResourceDuration("audio1")
        self.assertEqual(result, 10.5)

    def test_returns_zero_for_unknown(self):
        """Returns 0 for an unknown resource"""
        self.client.afterEffectResource = [
            {"name": "audio1", "duration": 10.5},
        ]
        result = self.client.getResourceDuration("unknown")
        self.assertEqual(result, 0)

    def test_empty_list(self):
        """Returns 0 when resource list is empty"""
        self.client.afterEffectResource = []
        result = self.client.getResourceDuration("anything")
        self.assertEqual(result, 0)


class TestStartBotFlow(unittest.TestCase):
    """Test startBot orchestration flow"""

    def setUp(self):
        self.client = Client()

    @patch.object(Client, 'startAfterEffect')
    def test_startbot_calls_start_after_effect(self, mock_start_ae):
        """startBot calls startAfterEffect with parsed config data"""
        config = {
            "project": {
                "project_file": "test.aep",
                "comp_name": "TestComp",
                "debug": True,
                "output_dir": "/tmp/output",
                "resources": []
            },
            "timeline": []
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            self.client.startBot(temp_path)
            mock_start_ae.assert_called_once()
            call_data = mock_start_ae.call_args[0][0]
            self.assertEqual(call_data["project"]["comp_name"], "TestComp")
        finally:
            os.unlink(temp_path)

    @patch.object(Client, 'startAfterEffect')
    def test_startbot_resolves_relative_paths(self, mock_start_ae):
        """startBot resolves relative paths to absolute"""
        config = {
            "project": {
                "project_file": "relative/test.aep",
                "output_dir": "relative/output",
                "debug": True,
                "resources": []
            },
            "timeline": []
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            self.client.startBot(temp_path)
            call_data = mock_start_ae.call_args[0][0]
            self.assertTrue(os.path.isabs(call_data["project"]["project_file"]))
            self.assertTrue(os.path.isabs(call_data["project"]["output_dir"]))
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
