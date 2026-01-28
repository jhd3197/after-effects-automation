"""
Template Generator Mixin
Provides functionality to create After Effects project templates (.aep files)
"""
import time
import os
from ae_automation.logging_config import get_logger
from ae_automation.exceptions import AENotResponsiveError, ScriptExecutionError

logger = get_logger(__name__)


class TemplateGeneratorMixin:
    """
    Mixin for generating After Effects project templates
    """

    def createNewProject(self):
        """
        Create a new After Effects project
        """
        logger.info("Creating new project...")
        self.runScript("create_new_project.jsx")
        time.sleep(1)  # Brief wait for script execution

    def saveProject(self, project_path):
        """
        Save the current project to a file

        Args:
            project_path: Path where the project will be saved
        """
        logger.info("Saving project to: %s", project_path)

        # Ensure directory exists
        project_dir = os.path.dirname(project_path)
        if project_dir and not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Convert to forward slashes for AE
        project_path = project_path.replace('\\', '/')

        _replace = {
            "{projectPath}": str(project_path)
        }
        self.runScript("save_project.jsx", _replace)
        time.sleep(2)  # Wait for save operation to complete

        # Verify the file was actually created
        original_path = project_path.replace('/', '\\')
        for i in range(10):  # Try checking 10 times with delays
            if os.path.exists(original_path):
                logger.info("Project saved successfully")
                return
            time.sleep(0.5)

        raise ScriptExecutionError(script_name="save_project.jsx", detail=f"File was not created at {original_path}")

    def addTextLayer(self, comp_name, layer_name, text_content="Sample Text",
                     x_position=960, y_position=540, font_size=72):
        """
        Add a text layer to a composition

        Args:
            comp_name: Name of the composition
            layer_name: Name for the text layer
            text_content: Initial text content
            x_position: X position in pixels
            y_position: Y position in pixels
            font_size: Font size in points
        """
        logger.info("Adding text layer '%s' to %s", layer_name, comp_name)
        _replace = {
            "{comp_name}": str(comp_name),
            "{layer_name}": str(layer_name),
            "{text_content}": str(text_content),
            "{x_position}": str(x_position),
            "{y_position}": str(y_position),
            "{font_size}": str(font_size)
        }
        self.runScript("add_text_layer.jsx", _replace)
        time.sleep(1)

    def addSolidLayer(self, comp_name, layer_name, color_r=1, color_g=1, color_b=1,
                     width=1920, height=1080):
        """
        Add a solid layer to a composition

        Args:
            comp_name: Name of the composition
            layer_name: Name for the solid layer
            color_r: Red value (0-1)
            color_g: Green value (0-1)
            color_b: Blue value (0-1)
            width: Width in pixels
            height: Height in pixels
        """
        logger.info("Adding solid layer '%s' to %s", layer_name, comp_name)
        _replace = {
            "{comp_name}": str(comp_name),
            "{layer_name}": str(layer_name),
            "{color_r}": str(color_r),
            "{color_g}": str(color_g),
            "{color_b}": str(color_b),
            "{width}": str(width),
            "{height}": str(height)
        }
        self.runScript("add_solid_layer.jsx", _replace)
        time.sleep(1)

    def addNullLayer(self, comp_name, layer_name):
        """
        Add a null object layer to a composition

        Args:
            comp_name: Name of the composition
            layer_name: Name for the null layer
        """
        logger.info("Adding null layer '%s' to %s", layer_name, comp_name)
        _replace = {
            "{comp_name}": str(comp_name),
            "{layer_name}": str(layer_name)
        }
        self.runScript("add_null_layer.jsx", _replace)
        time.sleep(1)

    def addShapeLayer(self, comp_name, layer_name, width=500, height=500,
                     color_r=0.5, color_g=0.5, color_b=0.5):
        """
        Add a shape layer with a rectangle to a composition

        Args:
            comp_name: Name of the composition
            layer_name: Name for the shape layer
            width: Rectangle width
            height: Rectangle height
            color_r: Red value (0-1)
            color_g: Green value (0-1)
            color_b: Blue value (0-1)
        """
        logger.info("Adding shape layer '%s' to %s", layer_name, comp_name)
        _replace = {
            "{comp_name}": str(comp_name),
            "{layer_name}": str(layer_name),
            "{width}": str(width),
            "{height}": str(height),
            "{color_r}": str(color_r),
            "{color_g}": str(color_g),
            "{color_b}": str(color_b)
        }
        self.runScript("add_shape_layer.jsx", _replace)
        time.sleep(1)

    def buildTemplate(self, template_config, output_path):
        """
        Build a complete template project from a configuration

        Args:
            template_config: Dictionary with template configuration
            output_path: Path where the .aep file will be saved

        Template config structure:
        {
            "name": "Template Name",
            "width": 1920,
            "height": 1080,
            "fps": 29.97,
            "duration": 120,
            "compositions": [
                {
                    "name": "CompName",
                    "width": 1920,
                    "height": 1080,
                    "duration": 10,
                    "fps": 29.97,
                    "layers": [
                        {
                            "type": "text",
                            "name": "LayerName",
                            "text": "Sample",
                            "x": 960,
                            "y": 540,
                            "fontSize": 72
                        },
                        {
                            "type": "solid",
                            "name": "Background",
                            "color": [0, 0, 0],
                            "width": 1920,
                            "height": 1080
                        }
                    ]
                }
            ]
        }
        """
        logger.info("Building template: %s", template_config.get('name', 'Unnamed Template'))

        # Ensure After Effects is running and ready
        if not self.ensure_after_effects_running(timeout=120):
            raise AENotResponsiveError(timeout=120)

        # Create new project
        self.createNewProject()

        # Create project folder structure
        project_folder = template_config.get('name', 'Template')
        self.createFolder(project_folder)

        # Create compositions
        for comp_config in template_config.get('compositions', []):
            comp_name = comp_config['name']
            comp_width = comp_config.get('width', template_config.get('width', 1920))
            comp_height = comp_config.get('height', template_config.get('height', 1080))
            comp_duration = comp_config.get('duration', template_config.get('duration', 120))
            comp_fps = comp_config.get('fps', template_config.get('fps', 29.97))

            logger.info("Creating composition: %s", comp_name)
            self.createComp(
                comp_name,
                compWidth=comp_width,
                compHeight=comp_height,
                duration=comp_duration,
                frameRate=comp_fps,
                folderName=project_folder
            )

            # Add layers to composition
            for layer_config in comp_config.get('layers', []):
                layer_type = layer_config.get('type', 'text')
                layer_name = layer_config['name']

                if layer_type == 'text':
                    self.addTextLayer(
                        comp_name,
                        layer_name,
                        text_content=layer_config.get('text', 'Sample Text'),
                        x_position=layer_config.get('x', 960),
                        y_position=layer_config.get('y', 540),
                        font_size=layer_config.get('fontSize', 72)
                    )
                elif layer_type == 'solid':
                    color = layer_config.get('color', [1, 1, 1])
                    self.addSolidLayer(
                        comp_name,
                        layer_name,
                        color_r=color[0],
                        color_g=color[1],
                        color_b=color[2],
                        width=layer_config.get('width', comp_width),
                        height=layer_config.get('height', comp_height)
                    )
                elif layer_type == 'null':
                    self.addNullLayer(comp_name, layer_name)
                elif layer_type == 'shape':
                    color = layer_config.get('color', [0.5, 0.5, 0.5])
                    self.addShapeLayer(
                        comp_name,
                        layer_name,
                        width=layer_config.get('width', 500),
                        height=layer_config.get('height', 500),
                        color_r=color[0],
                        color_g=color[1],
                        color_b=color[2]
                    )

        # Save the project
        self.saveProject(output_path)

        logger.info("Template created successfully! Saved to: %s", output_path)
