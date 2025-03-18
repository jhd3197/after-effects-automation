import pathlib
import gc
import os
from dotenv import load_dotenv

from ae_automation.mixins.afterEffect import afterEffectMixin
from ae_automation.mixins.tools import ToolsMixin
from ae_automation.mixins.bot import botMixin
from ae_automation.mixins.VideoEditorApp import VideoEditorAppMixin

# Load environment variables from .env file
load_dotenv()

class Client(
    afterEffectMixin,
    ToolsMixin,
    botMixin,
    VideoEditorAppMixin,
):
    JS_FRAMEWORK=""
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Get environment variables with defaults
        cache_folder = os.environ.get('CACHE_FOLDER', 'cache')
        
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
        framework_js = framework_js.replace('{CACHE_FOLDER}', cache_folder.replace('\\', '/'))
        self.JS_FRAMEWORK += framework_js