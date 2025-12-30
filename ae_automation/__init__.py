import pathlib
import gc
import os
from dotenv import load_dotenv

from ae_automation.mixins.afterEffect import afterEffectMixin
from ae_automation.mixins.tools import ToolsMixin
from ae_automation.mixins.bot import botMixin
from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin
from ae_automation.mixins.templateGenerator import TemplateGeneratorMixin
from ae_automation.mixins.processManager import ProcessManagerMixin

# Load environment variables from .env file
load_dotenv()

class Client(
    afterEffectMixin,
    ToolsMixin,
    botMixin,
    VideoEditorAppMixin,
    TemplateGeneratorMixin,
    ProcessManagerMixin,
):
    JS_FRAMEWORK=""
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Get environment variables with defaults
        from ae_automation import settings
        cache_folder = settings.CACHE_FOLDER
        
        # Create cache folder if it doesn't exist
        pathlib.Path(cache_folder).mkdir(parents=True, exist_ok=True) 
        gc.collect()
        
        # Get base directory for this package
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load JS framework files using relative paths
        js_path = os.path.join(base_dir, 'mixins', 'js')
        self.JS_FRAMEWORK = self.file_get_contents(os.path.join(js_path, 'json2.js'))
        framework_js = self.file_get_contents(os.path.join(js_path, 'framework.js'))
        
        # Replace cache folder placeholder
        # Ensure path has trailing slash for JS string concatenation
        cache_path = cache_folder.replace('\\', '/')
        if not cache_path.endswith('/'):
            cache_path += '/'
            
        framework_js = framework_js.replace('{CACHE_FOLDER}', cache_path)
        self.JS_FRAMEWORK += framework_js

# Export the Client class with multiple names for convenience
AfterEffectsAutomation = Client
__all__ = ['Client', 'AfterEffectsAutomation']