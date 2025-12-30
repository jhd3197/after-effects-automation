"""
Unit tests for JSON configuration parsing
"""
import unittest
import json
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfigurationParsing(unittest.TestCase):
    """Test JSON configuration file parsing"""

    def create_test_config(self, **overrides):
        """Helper to create test configuration"""
        config = {
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
                "output_dir": "/tmp/output",
                "renderComp": False,
                "debug": True,
                "resources": []
            },
            "timeline": []
        }

        # Apply overrides
        if 'project' in overrides:
            config['project'].update(overrides['project'])
        if 'timeline' in overrides:
            config['timeline'] = overrides['timeline']

        return config

    def test_basic_config_structure(self):
        """Test that basic config structure is valid"""
        config = self.create_test_config()

        self.assertIn('project', config)
        self.assertIn('timeline', config)
        self.assertIsInstance(config['project'], dict)
        self.assertIsInstance(config['timeline'], list)

    def test_project_required_fields(self):
        """Test that project has all required fields"""
        config = self.create_test_config()
        project = config['project']

        required_fields = [
            'project_file', 'comp_name', 'comp_fps', 'comp_width',
            'comp_height', 'comp_start_time', 'comp_end_time',
            'output_file', 'output_dir', 'debug', 'resources'
        ]

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, project,
                            f"Project config missing required field: {field}")

    def test_config_with_resources(self):
        """Test configuration with resources"""
        config = self.create_test_config(project={
            'resources': [
                {
                    "type": "audio",
                    "name": "test_audio",
                    "path": "/path/to/audio.mp3",
                    "duration": 10.5
                },
                {
                    "type": "image",
                    "name": "test_image",
                    "path": "/path/to/image.png"
                }
            ]
        })

        resources = config['project']['resources']
        self.assertEqual(len(resources), 2)

        # Check audio resource
        audio = resources[0]
        self.assertEqual(audio['type'], 'audio')
        self.assertEqual(audio['name'], 'test_audio')
        self.assertIn('duration', audio)

        # Check image resource
        image = resources[1]
        self.assertEqual(image['type'], 'image')
        self.assertEqual(image['name'], 'test_image')

    def test_config_with_timeline(self):
        """Test configuration with timeline scenes"""
        timeline = [
            {
                "name": "intro",
                "duration": 5,
                "startTime": 0,
                "template_comp": "IntroTemplate",
                "reverse": False,
                "custom_actions": []
            },
            {
                "name": "outro",
                "duration": 3,
                "startTime": 5,
                "template_comp": "OutroTemplate",
                "reverse": False,
                "custom_actions": []
            }
        ]

        config = self.create_test_config(timeline=timeline)

        self.assertEqual(len(config['timeline']), 2)
        self.assertEqual(config['timeline'][0]['name'], 'intro')
        self.assertEqual(config['timeline'][1]['name'], 'outro')

    def test_config_with_custom_actions(self):
        """Test configuration with custom actions"""
        timeline = [
            {
                "name": "scene1",
                "duration": 5,
                "startTime": 0,
                "template_comp": "Template",
                "reverse": False,
                "custom_actions": [
                    {
                        "change_type": "update_layer_property",
                        "comp_name": "Template",
                        "layer_name": "TextLayer",
                        "property_name": "Text.Source Text",
                        "property_type": "string",
                        "value": "Hello World"
                    },
                    {
                        "change_type": "add_resource",
                        "resource_name": "audio1",
                        "comp_name": "Template",
                        "startTime": "0",
                        "duration": "0"
                    }
                ]
            }
        ]

        config = self.create_test_config(timeline=timeline)

        actions = config['timeline'][0]['custom_actions']
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['change_type'], 'update_layer_property')
        self.assertEqual(actions[1]['change_type'], 'add_resource')

    def test_config_json_serialization(self):
        """Test that config can be serialized to JSON"""
        config = self.create_test_config()

        try:
            json_str = json.dumps(config, indent=2)
            self.assertIsInstance(json_str, str)

            # Test it can be parsed back
            parsed = json.loads(json_str)
            self.assertEqual(parsed, config)
        except Exception as e:
            self.fail(f"Config serialization failed: {e}")

    def test_config_file_io(self):
        """Test reading and writing config to file"""
        config = self.create_test_config()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f, indent=2)
            temp_file = f.name

        try:
            # Read it back
            with open(temp_file, 'r') as f:
                loaded_config = json.load(f)

            self.assertEqual(loaded_config, config)
        finally:
            import os
            os.unlink(temp_file)


class TestTimeFormatParsing(unittest.TestCase):
    """Test time format parsing"""

    def test_time_string_format(self):
        """Test HH:MM:SS time format conversion"""
        from ae_automation import Client
        client = Client()

        test_cases = [
            ("00:00:10", 10.0),
            ("00:01:00", 60.0),
            ("00:10:00", 600.0),
            ("01:00:00", 3600.0),
            ("00:12:30", 750.0),
        ]

        for time_str, expected_seconds in test_cases:
            with self.subTest(time=time_str):
                result = client.time_to_seconds(time_str)
                self.assertEqual(result, expected_seconds,
                               f"time_to_seconds('{time_str}') should return {expected_seconds}")


if __name__ == '__main__':
    unittest.main()
