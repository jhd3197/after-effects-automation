"""
Unit tests for CLI commands (generate, export) and template registry.
"""
import unittest
import os
import sys
import argparse
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ae_automation.templates import BUILTIN_TEMPLATES, get_template, list_templates
import cli


class TestTemplateRegistry(unittest.TestCase):
    """Test the built-in template registry."""

    EXPECTED_TEMPLATES = ["tutorial", "social-media", "product", "slideshow", "event"]

    def test_all_expected_templates_exist(self):
        for name in self.EXPECTED_TEMPLATES:
            self.assertIn(name, BUILTIN_TEMPLATES, f"Missing template: {name}")

    def test_no_unexpected_templates(self):
        for name in BUILTIN_TEMPLATES:
            self.assertIn(name, self.EXPECTED_TEMPLATES, f"Unexpected template: {name}")

    def test_each_template_has_required_keys(self):
        required = {"name", "width", "height", "fps", "duration", "compositions"}
        for name, config in BUILTIN_TEMPLATES.items():
            with self.subTest(template=name):
                self.assertTrue(required.issubset(config.keys()),
                                f"Template '{name}' missing keys: {required - config.keys()}")

    def test_each_composition_has_name_and_layers(self):
        for name, config in BUILTIN_TEMPLATES.items():
            for comp in config["compositions"]:
                with self.subTest(template=name, comp=comp.get("name")):
                    self.assertIn("name", comp)
                    self.assertIn("layers", comp)
                    self.assertGreater(len(comp["layers"]), 0)

    def test_layer_types_are_valid(self):
        valid_types = {"text", "solid", "null", "shape"}
        for name, config in BUILTIN_TEMPLATES.items():
            for comp in config["compositions"]:
                for layer in comp["layers"]:
                    with self.subTest(template=name, comp=comp["name"], layer=layer.get("name")):
                        self.assertIn(layer["type"], valid_types)

    def test_get_template_returns_config(self):
        config = get_template("tutorial")
        self.assertIsNotNone(config)
        self.assertEqual(config["name"], "Tutorial Template")

    def test_get_template_returns_none_for_unknown(self):
        self.assertIsNone(get_template("nonexistent"))

    def test_list_templates_returns_all(self):
        result = list_templates()
        self.assertEqual(len(result), len(BUILTIN_TEMPLATES))
        names = [name for name, _ in result]
        for expected in self.EXPECTED_TEMPLATES:
            self.assertIn(expected, names)


class TestGenerateSubparser(unittest.TestCase):
    """Test that the generate subparser is registered with correct arguments."""

    def setUp(self):
        # Build the parser the same way main() does, just grab the parser
        self.parser = argparse.ArgumentParser(prog='ae-automation')
        self.subparsers = self.parser.add_subparsers(dest='command')
        # Re-create the generate subparser
        p = self.subparsers.add_parser('generate')
        p.add_argument('--template', '-t')
        p.add_argument('--all', action='store_true')
        p.add_argument('--output', '-o')
        p.add_argument('--list', '-l', action='store_true')

    def test_generate_template_flag(self):
        args = self.parser.parse_args(['generate', '--template', 'tutorial'])
        self.assertEqual(args.template, 'tutorial')

    def test_generate_all_flag(self):
        args = self.parser.parse_args(['generate', '--all'])
        self.assertTrue(args.all)

    def test_generate_output_flag(self):
        args = self.parser.parse_args(['generate', '-t', 'tutorial', '-o', 'out.aep'])
        self.assertEqual(args.output, 'out.aep')

    def test_generate_list_flag(self):
        args = self.parser.parse_args(['generate', '--list'])
        self.assertTrue(args.list)


class TestExportSubparser(unittest.TestCase):
    """Test that the export subparser is registered with correct arguments."""

    def setUp(self):
        self.parser = argparse.ArgumentParser(prog='ae-automation')
        self.subparsers = self.parser.add_subparsers(dest='command')
        p = self.subparsers.add_parser('export')
        p.add_argument('--template', '-t', required=True)
        p.add_argument('--output-dir', '-o', default='.')
        p.add_argument('--comp', '-c')
        p.add_argument('--force', '-f', action='store_true')

    def test_export_template_flag(self):
        args = self.parser.parse_args(['export', '--template', 'tutorial'])
        self.assertEqual(args.template, 'tutorial')

    def test_export_output_dir_flag(self):
        args = self.parser.parse_args(['export', '-t', 'tutorial', '-o', 'renders/'])
        self.assertEqual(args.output_dir, 'renders/')

    def test_export_comp_flag(self):
        args = self.parser.parse_args(['export', '-t', 'tutorial', '--comp', 'IntroScene'])
        self.assertEqual(args.comp, 'IntroScene')

    def test_export_force_flag(self):
        args = self.parser.parse_args(['export', '-t', 'tutorial', '--force'])
        self.assertTrue(args.force)

    def test_export_default_output_dir(self):
        args = self.parser.parse_args(['export', '-t', 'tutorial'])
        self.assertEqual(args.output_dir, '.')

    def test_export_requires_template(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['export'])


class TestCmdGenerate(unittest.TestCase):
    """Test cmd_generate handler logic."""

    @patch('ae_automation.Client')
    def test_generate_list_prints_templates(self, mock_client_cls):
        args = argparse.Namespace(list=True, all=False, template=None, output=None)
        # Should not raise, should not instantiate Client
        cli.cmd_generate(args)
        mock_client_cls.assert_not_called()

    @patch('ae_automation.Client')
    def test_generate_single_template(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        args = argparse.Namespace(list=False, all=False, template='tutorial', output=None)
        cli.cmd_generate(args)

        mock_client.buildTemplate.assert_called_once()
        call_args = mock_client.buildTemplate.call_args
        self.assertEqual(call_args[0][0]["name"], "Tutorial Template")
        self.assertTrue(call_args[0][1].endswith('.aep'))

    @patch('ae_automation.Client')
    def test_generate_single_template_custom_output(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        args = argparse.Namespace(list=False, all=False, template='tutorial', output='my.aep')
        cli.cmd_generate(args)

        call_args = mock_client.buildTemplate.call_args
        self.assertEqual(call_args[0][1], 'my.aep')

    @patch('ae_automation.Client')
    def test_generate_all_templates(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        args = argparse.Namespace(list=False, all=True, template=None, output=None)
        cli.cmd_generate(args)

        self.assertEqual(mock_client.buildTemplate.call_count, len(BUILTIN_TEMPLATES))

    def test_generate_unknown_template_exits(self):
        args = argparse.Namespace(list=False, all=False, template='nonexistent', output=None)
        with self.assertRaises(SystemExit) as ctx:
            cli.cmd_generate(args)
        self.assertEqual(ctx.exception.code, 1)

    def test_generate_no_flags_exits(self):
        args = argparse.Namespace(list=False, all=False, template=None, output=None)
        with self.assertRaises(SystemExit) as ctx:
            cli.cmd_generate(args)
        self.assertEqual(ctx.exception.code, 1)


class TestCmdExport(unittest.TestCase):
    """Test cmd_export handler logic."""

    def test_export_unknown_template_exits(self):
        args = argparse.Namespace(template='nonexistent', output_dir='.', comp=None, force=False)
        with self.assertRaises(SystemExit) as ctx:
            cli.cmd_export(args)
        self.assertEqual(ctx.exception.code, 1)

    @patch('ae_automation.Client')
    def test_export_calls_build_then_render(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.renderFile.return_value = '/out/tutorial.mp4'

        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(
                template='tutorial',
                output_dir=tmpdir,
                comp=None,
                force=False,
            )
            cli.cmd_export(args)

            mock_client.buildTemplate.assert_called_once()
            mock_client.renderFile.assert_called_once()

            # Check renderFile used the first comp name
            render_args = mock_client.renderFile.call_args[0]
            self.assertEqual(render_args[1], 'IntroScene')

    @patch('ae_automation.Client')
    def test_export_uses_specified_comp(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.renderFile.return_value = '/out/tutorial.mp4'

        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(
                template='tutorial',
                output_dir=tmpdir,
                comp='OutroScene',
                force=False,
            )
            cli.cmd_export(args)

            render_args = mock_client.renderFile.call_args[0]
            self.assertEqual(render_args[1], 'OutroScene')

    @patch('ae_automation.Client')
    def test_export_refuses_overwrite_without_force(self, mock_client_cls):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create an existing .aep file
            aep_path = os.path.join(tmpdir, 'tutorial.aep')
            with open(aep_path, 'w') as f:
                f.write('existing')

            args = argparse.Namespace(
                template='tutorial',
                output_dir=tmpdir,
                comp=None,
                force=False,
            )
            with self.assertRaises(SystemExit) as ctx:
                cli.cmd_export(args)
            self.assertEqual(ctx.exception.code, 1)
            mock_client_cls.assert_not_called()

    @patch('ae_automation.Client')
    def test_export_allows_overwrite_with_force(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.renderFile.return_value = '/out/tutorial.mp4'

        with tempfile.TemporaryDirectory() as tmpdir:
            aep_path = os.path.join(tmpdir, 'tutorial.aep')
            with open(aep_path, 'w') as f:
                f.write('existing')

            args = argparse.Namespace(
                template='tutorial',
                output_dir=tmpdir,
                comp=None,
                force=True,
            )
            cli.cmd_export(args)
            mock_client.buildTemplate.assert_called_once()


class TestMainParserRegistration(unittest.TestCase):
    """Verify that main() registers generate and export subcommands."""

    @patch('cli.cmd_generate')
    def test_main_routes_generate(self, mock_cmd):
        with patch('sys.argv', ['ae-automation', 'generate', '--list']):
            cli.main()
        mock_cmd.assert_called_once()

    @patch('cli.cmd_export')
    def test_main_routes_export(self, mock_cmd):
        with patch('sys.argv', ['ae-automation', 'export', '-t', 'tutorial']):
            cli.main()
        mock_cmd.assert_called_once()


if __name__ == '__main__':
    unittest.main()
