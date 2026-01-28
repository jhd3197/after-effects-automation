from __future__ import annotations

import json
from ae_automation.logging_config import get_logger
from ae_automation.exceptions import ConfigValidationError

logger = get_logger(__name__)


class botMixin:
    """
    Bot Mixin
    """

    def startBot(self, file_name: str) -> None:
        """
        startBot
        """
        logger.info("Starting bot")

        import os

        try:
            with open(file_name, encoding="utf8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            raise ConfigValidationError(field="config_file", detail=f"File not found: {file_name}")
        except json.JSONDecodeError as e:
            raise ConfigValidationError(field="config_file", detail=f"Invalid JSON in {file_name}: {e}")
            
        # Resolve relative paths relative to the config file location
        config_dir = os.path.dirname(os.path.abspath(file_name))
        
        if "project" in data:
            # Resolve project file path
            if "project_file" in data["project"]:
                proj_path = data["project"]["project_file"]
                if not os.path.isabs(proj_path):
                    data["project"]["project_file"] = os.path.abspath(os.path.join(config_dir, proj_path))
                    logger.info("Resolved project path: %s", data['project']['project_file'])
            
            # Resolve output directory
            if "output_dir" in data["project"]:
                out_dir = data["project"]["output_dir"]
                if not os.path.isabs(out_dir):
                    data["project"]["output_dir"] = os.path.abspath(os.path.join(config_dir, out_dir))
                    logger.info("Resolved output dir: %s", data['project']['output_dir'])

        self.startAfterEffect(data)
