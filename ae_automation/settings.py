import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

# Get environment variables with defaults
CACHE_FOLDER = os.getenv('CACHE_FOLDER', os.path.join(os.getcwd(), 'cache'))
AFTER_EFFECT_FOLDER = os.getenv('AFTER_EFFECT_FOLDER', 'C:/Program Files/Adobe/Adobe After Effects 2025/Support Files')
AFTER_EFFECT_PROJECT_FOLDER = os.getenv('AFTER_EFFECT_PROJECT_FOLDER', 'au-automate')

# Derive AERENDER_PATH from AFTER_EFFECT_FOLDER
AERENDER_PATH = os.getenv('AERENDER_PATH', os.path.join(AFTER_EFFECT_FOLDER, 'aerender.exe'))

# Ensure cache directory exists
os.makedirs(CACHE_FOLDER, exist_ok=True)

# Package resources path
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_DIR = os.path.join(PACKAGE_DIR, 'mixins', 'js')

def validate_settings():
    """Validate required settings and paths."""
    if not os.path.exists(AFTER_EFFECT_FOLDER):
        raise ValueError(f"After Effects folder not found: {AFTER_EFFECT_FOLDER}")
    
    if not os.path.exists(AERENDER_PATH):
        raise ValueError(f"Aerender executable not found: {AERENDER_PATH}")
    
    if not os.path.exists(JS_DIR):
        raise ValueError(f"JavaScript files directory not found: {JS_DIR}")

# Validate settings on import
validate_settings()
