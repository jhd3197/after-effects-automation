# 🎬 After Effects Automation

![au_automation](https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png)

## 🚀 Overview

After Effects Automation is a powerful Python-based tool that automates the creation and rendering of Adobe After Effects compositions. It allows you to programmatically control Adobe After Effects, making it perfect for batch processing and automated video production workflows.

## ✨ Features

- Automated composition creation and management
- Timeline manipulation and control
- Custom action support for advanced automation
- Template-based composition generation
- Automated rendering capabilities
- Scene management with precise timing control
- Web-based configuration editor
- Python-to-JavaScript bridge for direct After Effects scripting
- Rich library of extensible JavaScript actions

## 🖥️ Compatibility

This tool has been thoroughly tested with:
- Adobe After Effects 2024
- Adobe After Effects 2025 (Beta)

While specifically tested on these versions, the tool should theoretically work with any Adobe After Effects CC version. The JavaScript integration is based on the ExtendScript technology which has been consistent across Creative Cloud releases. If you encounter version-specific issues, please report them in the issue tracker.

## 📁 Project Structure

```
after-effects-automation/
├── example.json           # Example configuration file
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── setup.py             # Package configuration
├── MANIFEST.in          # Package manifest
├── .env                 # Local environment variables
├── .env.example         # Example environment file
├── run.py               # CLI automation script
├── app.py               # Web editor script
└── ae_automation/       # Main package
    ├── __init__.py     
    ├── settings.py      # Environment configuration
    └── mixins/          # Functionality modules
        ├── afterEffect.py # After Effects control
        ├── bot.py        # Automation bot
        ├── tools.py      # Utility functions
        ├── types.py      # Type definitions
        ├── VideoEditorApp.py # Web interface
        ├── js/           # JavaScript files for AE integration
        │   ├── framework.js  # Core JS framework
        │   ├── json2.js      # JSON utilities
        │   ├── actions/      # Custom JS actions
        │   │   ├── textActions.jsx  # Text manipulation scripts
        │   │   ├── layerEffects.jsx # Layer effect scripts
        │   │   ├── compositionActions.jsx # Composition management scripts
        │   │   └── ...       # Various action scripts
        │   └── ...           # Various JSX scripts
        └── videoEditor/  # Web-based editor interface
            ├── index.html
            ├── script.js
            └── style.css
```

## 🛠️ Installation

### Via Pip (Recommended)

```bash
pip install after-effects-automation
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/after-effects-automation.git
cd after-effects-automation
```

2. Install in development mode:
```bash
pip install -e .
```

## ⚙️ Configuration

1. Create a `.env` file in your project directory (copy from `.env.example`):
```bash
cp .env.example .env
```

2. Configure your environment variables in `.env`:
```env
# Cache folder for temporary files
CACHE_FOLDER=/path/to/cache

# After Effects installation folder
AFTER_EFFECT_FOLDER=C:/Program Files/Adobe/Adobe After Effects 2024/Support Files

# Project folder name in After Effects
AFTER_EFFECT_PROJECT_FOLDER=au-automate

# Optional: Override aerender path (default: AFTER_EFFECT_FOLDER/aerender.exe)
# AERENDER_PATH=/custom/path/to/aerender.exe
```

## 📝 Usage

### Command Line Automation

1. Create a JSON configuration file (see `example.json`) that defines your project structure and timeline.

2. Run the automation script:
```bash
# If installed via pip:
ae-automate path/to/your/config.json

# Or if running from source:
python run.py path/to/your/config.json
```

### Web-based Configuration Editor

The project includes a web-based editor for creating and modifying configuration files:

```bash
# If installed via pip:
ae-editor path/to/your/config.json

# Or if running from source:
python app.py path/to/your/config.json
```

Optional arguments:
- `--host`: Host to run the web server on (default: 127.0.0.1)
- `--port`: Port to run the web server on (default: 5000)

Example:
```bash
ae-editor config.json --host 0.0.0.0 --port 8080
```

The editor will automatically open in your default web browser. You can:
- Edit project settings
- Manage scenes and timelines
- Configure custom actions
- Save changes directly to your configuration file

## 🔌 Python-JavaScript Integration System

This project features a robust Python-JavaScript bridge that allows Python code to directly control Adobe After Effects through its scripting interface. This integration is achieved through:

1. **JavaScript Action Library**: A comprehensive collection of JavaScript scripts (.jsx files) that perform specific actions within After Effects
2. **Python Execution Engine**: A system that sends JavaScript commands to After Effects and retrieves results
3. **Configuration-driven Scripting**: The ability to define JavaScript actions in the JSON configuration file

### How JavaScript Integration Works

1. Python code prepares the JavaScript parameters based on the configuration
2. The appropriate JavaScript script is selected from the library
3. Parameters are injected into the JavaScript code
4. The script is passed to After Effects via the ExtendScript Toolkit bridge
5. Results and feedback are captured and returned to Python

### Available JavaScript Script Categories

- **Composition Management**: Creating, modifying, and rendering compositions
- **Layer Manipulation**: Managing layers, their properties and timing
- **Text Operations**: Text layer creation and styling
- **Effect Application**: Adding and configuring effects
- **Property Animation**: Creating keyframes and controlling animations
- **Resource Management**: Importing and organizing project resources
- **Rendering Controls**: Configuration of render settings and queue management

### Custom JavaScript Integration

You can extend the system with your own JavaScript actions:

1. Add your JSX script to the `ae_automation/mixins/js/actions/` directory
2. Register the script in the JavaScript action registry
3. Reference your custom action in the configuration file

Example of a custom JSX script:
```jsx
// Custom text effect script
function applyTextEffect(layerName, effectName, intensity) {
    var comp = app.project.activeItem;
    var layer = comp.layer(layerName);
    var effect = layer.Effects.addProperty(effectName);
    effect.property("Intensity").setValue(intensity);
    return "Applied " + effectName + " to " + layerName;
}
```

### 📋 Configuration Structure

The automation is controlled through a JSON configuration file that defines:
- Project settings (After Effects project file and main composition)
- Timeline with multiple scenes
- Custom actions for each scene
- Timing and duration controls

See `example.json` for a complete example configuration.

## ⚙️ Configuration Options

### Project Settings
- `project_file`: Path to your After Effects project file
- `comp_name`: Name of the main composition
- `comp_width`: Width of the composition in pixels (default: 1920)
- `comp_height`: Height of the composition in pixels (default: 1080)
- `comp_fps`: Frame rate of the composition (default: 29.97)
- `auto_time`: Enable/disable automatic timing calculation (boolean)
- `comp_start_time`: Start time of the composition in "HH:MM:SS" format
- `comp_end_time`: Duration of the composition in seconds or "HH:MM:SS" format
- `output_file`: Name of the output rendered file
- `output_dir`: Directory where rendered files will be saved
- `renderComp`: Enable/disable automatic rendering after processing (boolean)
- `debug`: Enable/disable debug mode (boolean)
- `resources`: Array of resources to import into the project, with type specification

### Resource Properties
- `type`: Type of resource (audio, image, video)
- `name`: Identifier for the resource
- `path`: File path to the resource
- `duration`: Length of audio/video resources in seconds (only for audio/video types)

### Scene Properties
- `name`: Scene identifier
- `duration`: Length of the scene in seconds
- `startTime`: Start time in the timeline
- `template_comp`: Template composition to use
- `reverse`: Enable/disable reverse playback (boolean)
- `custom_actions`: Array of custom actions to apply to the scene

## 🎮 Custom Actions

Custom actions allow you to modify compositions and layers programmatically. Here are the available action types:

### Update Layer Property
Updates a layer's property at a specific time:
```json
{
    "change_type": "update_layer_property",
    "comp_name": "TitleSequence",
    "layer_name": "MainTitle",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": "Product Launch 2025<br>New Features Revealed"
}
```

### Add Resource
Adds a resource (like audio or video) to the composition:
```json
{
    "change_type": "add_resource",
    "resource_name": "intro_voice",
    "comp_name": "TitleSequence",
    "startTime": "1.5",
    "duration": "0"
}
```

### Swap Items by Index
Replaces a layer with another item:
```json
{
    "change_type": "swap_items_by_index",
    "layer_name": "hero_image",
    "comp_name": "TitleSequence",
    "layer_index": "4",
    "fit_to_screen": false,
    "fit_to_screen_width": true,
    "fit_to_screen_height": false
}
```

### Add Marker
Adds a marker to the timeline:
```json
{
    "change_type": "add_marker",
    "comp_name": "myComp",
    "layer_name": "timeline",
    "marker_name": "transition",
    "marker_time": 5.5
}
```

### Add Composition
Adds a new composition to the timeline:
```json
{
    "change_type": "add_comp",
    "comp_name": "newComp",
    "startTime": 0,
    "duration": 30
}
```

## 📝 Template System

The template system allows you to create reusable sets of actions with dynamic values:

```json
{
    "change_type": "template",
    "template_name": "titleCard",
    "template_values": {
        "title": "My Custom Title",
        "subtitle": "Custom Subtitle",
        "duration": 5
    }
}
```

Templates are defined in the configuration file under the `templates` section:

```json
{
    "templates": {
        "titleCard": [
            {
                "change_type": "update_layer_property",
                "comp_name": "titleComp",
                "layer_name": "mainTitle",
                "property_name": "Source Text",
                "value": "{title}"
            },
            {
                "change_type": "update_layer_property",
                "comp_name": "titleComp",
                "layer_name": "subtitle",
                "property_name": "Source Text",
                "value": "{subtitle}"
            }
        ]
    }
}
```

## 🎨 Property Types and Values

### Text Properties
- Property name: "Text.Source Text"
- Property type: "string"
- Value: String (supports HTML tags like `<br>` for line breaks)
```json
"property_name": "Text.Source Text",
"property_type": "string",
"value": "Your Text Here<br>Second Line"
```

### Position Properties
- Property name: "Transform.Position"
- Property type: "array"
- Value: Array [x, y] or [x, y, z]
```json
"property_name": "Transform.Position",
"property_type": "array",
"value": [960, 540]
```

### Scale Properties
- Property name: "Transform.Scale"
- Property type: "array"
- Value: Array [width%, height%]
```json
"property_name": "Transform.Scale",
"property_type": "array",
"value": [100, 100]
```

### Color Properties
- Property name: "Effects.Fill.Color"
- Property type: "array"
- Value: Array [r, g, b, a] (0-1 range)
```json
"property_name": "Effects.Fill.Color",
"property_type": "array",
"value": [1, 0, 0, 1]
```

### Time Values
- Used in startTime, duration
- Value: Number (seconds) or String (for exact time specification)
```json
"startTime": 5.5
```
or
```json
"startTime": "1.5"
```

## 🔍 Troubleshooting

### Common Issues

1. **Environment Variables Not Loading**
   - Ensure `.env` file exists in your project directory
   - Check that all required variables are set
   - Verify file permissions

2. **After Effects Not Found**
   - Verify AFTER_EFFECT_FOLDER path in `.env`
   - Check that After Effects is properly installed

3. **Script Execution Errors**
   - Make sure After Effects is not running when starting the automation
   - Check the console for JavaScript errors

4. **Resource Import Failures**
   - Verify that all file paths in your configuration are correct and accessible
   - Ensure file formats are compatible with After Effects

5. **Rendering Issues**
   - Check that aerender.exe path is correct
   - Ensure you have sufficient disk space for rendered files
   - Verify that the composition name in your config matches the actual comp name

6. **Web Editor Issues**
   - Make sure no other service is using the specified port
   - Check that the configuration file is writable
   - Clear browser cache if the interface isn't updating

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
