---
name: manage-ae
description: Manage After Effects from Claude — create configs, build compositions, render videos, diagnose issues, and optionally generate AI content via Prompture
metadata:
  author: after-effects-automation
  version: "1.0"
---

# Manage After Effects

This skill lets you directly control Adobe After Effects: create automation configs, run pipelines, render videos, diagnose setup issues, and optionally generate AI-powered content using Prompture.

## What You Can Do

| Action | How |
|--------|-----|
| **Create a config** | Build a JSON config file with project settings, timeline, and custom actions |
| **Run automation** | Execute `ae-automation run <config.json>` to launch AE, build compositions, and render |
| **Render a video** | Use the Python API or CLI to render a specific comp from an .aep file |
| **Diagnose setup** | Run `ae-automation diagnose` to check AE installation, paths, and scripting |
| **Generate template** | Run `ae-automation generate --template <name>` to create .aep files from built-in templates |
| **Export video** | Run `ae-automation export --template <name>` to generate + render in one step |
| **AI content** | Use Prompture to generate text, scripts, scene descriptions, then feed into a config |

## Before Starting

Ask the user:

1. **What do you want to do?** (create a video, update an existing config, render, diagnose, generate content)
2. **Do you have an existing .aep template?** If yes, get the path and composition names
3. **What assets do you need?** (images, audio, video files — get paths)
4. **What content goes into the video?** (titles, body text, colors, timings)
5. **Should we use AI to generate any content?** (text, scene descriptions, scripts via Prompture)

## Step-by-Step: Create and Run an Automation

### Step 1: Gather Information

You need:
- Path to an `.aep` template file (or use `ae-automation generate` to create one)
- Composition names inside the template (the template comps that will be duplicated per scene)
- Layer names within those comps (for text, images, effects)
- Asset file paths (images, audio, video)
- Output directory and filename

### Step 2: Build the Config JSON

Create a JSON file with this structure:

```json
{
  "project": {
    "project_file": "path/to/template.aep",
    "comp_name": "MainComp",
    "comp_fps": 30,
    "comp_width": 1920,
    "comp_height": 1080,
    "comp_start_time": "00:00:00",
    "comp_end_time": 30,
    "output_file": "output.mp4",
    "output_dir": "path/to/output",
    "renderComp": true,
    "debug": false,
    "resources": []
  },
  "timeline": [],
  "templates": {}
}
```

**Important conventions:**
- Paths can be relative (resolved from config file location) or absolute
- Use forward slashes in paths even on Windows
- `comp_name` is the main composition where scenes are assembled
- Set `"debug": true` to test config loading without launching AE

### Step 3: Define Resources

Add external assets to `project.resources`:

```json
"resources": [
  {"type": "image", "name": "bg", "path": "C:/assets/background.png"},
  {"type": "audio", "name": "music", "path": "C:/assets/bgm.mp3"},
  {"type": "video", "name": "clip", "path": "C:/assets/footage.mp4"}
]
```

- `name` is the identifier used to reference this asset in timeline actions
- MP3 duration is auto-detected; for other types, specify `"duration"` manually

### Step 4: Build the Timeline

Each scene duplicates a template composition and applies custom actions:

```json
"timeline": [
  {
    "name": "intro",
    "duration": 5,
    "startTime": 0,
    "template_comp": "IntroTemplate",
    "reverse": false,
    "custom_actions": [
      {
        "change_type": "update_layer_property",
        "comp_name": "IntroTemplate",
        "layer_name": "Title",
        "property_name": "Text.Source Text",
        "property_type": "string",
        "value": "Welcome"
      }
    ]
  }
]
```

**Scene naming:** The duplicated comp is named `slug(scene_folder + " " + template_comp)`. For scene index 0, the folder is `scene-1`, so the comp becomes `scene-1-IntroTemplate`. Use this derived name in `comp_name` for custom actions.

### Step 5: Custom Actions Reference

**8 action types available:**

| `change_type` | Purpose | Key fields |
|---|---|---|
| `update_layer_property` | Set text, color, position | `comp_name`, `layer_name`, `property_name`, `property_type`, `value` |
| `update_layer_property_at_frame` | Set keyframe at specific frame | Same + `frame` |
| `add_resource` | Add imported asset to comp | `resource_name`, `comp_name`, `startTime`, `duration` |
| `edit_resource` | Modify resource layer timing | `comp_name`, `layerIndex`, `startTime`, `duration` |
| `swap_items_by_index` | Replace layer source | `comp_name`, `layer_index`, `layer_name` |
| `add_marker` | Add composition marker | `comp_name`, `layer_name`, `marker_name`, `marker_time` |
| `add_comp` | Nest a composition | `comp_name`, `startTime`, `duration` |
| `template` | Apply reusable template | `template_name`, `template_values` |

**Property dot-notation paths:**
- `Text.Source Text` — text content
- `Transform.Position` — `[x,y]`
- `Transform.Scale` — `[x,y]`
- `Transform.Opacity` — 0-100
- `Transform.Rotation` — degrees
- `Effects.ColorEffect.Color` — effect color
- `Effects.SliderControl.Slider` — effect slider

**Value formats:**
- Strings: `"value": "Hello"`
- Colors: `"value": "#FF0000"` with `"property_type": "color"` (auto-converted to AE RGBA)
- Arrays: `"value": "[960,540]"` (string representation, parsed by framework.js)
- Numbers: `"value": "100"` (string, parsed by valueParser)
- Line breaks: Use `<br>` in text — converted to AE carriage returns (`\r`)

### Step 6: Run the Automation

```bash
# Full pipeline: launch AE, build, render
ae-automation run config.json

# Dry run (validate config without launching AE)
# Set "debug": true in the config, then:
ae-automation run config.json

# Or via Python:
python -c "from ae_automation import Client; Client().startBot('config.json')"
```

### Step 7: Render Only

If you already have a built .aep and just want to render:

```python
from ae_automation import Client
client = Client()
output = client.renderFile("project.aep", "MainComp", "output_dir/")
print(f"Rendered to: {output}")
```

Or use the CLI export:
```bash
ae-automation export --template tutorial --output-dir renders/
```

## Diagnose Issues

Run diagnostics when things aren't working:

```bash
ae-automation diagnose
```

This checks:
- AE installation path and version
- aerender.exe availability
- Scripting preferences (Allow Scripts to Write Files)
- Queue folder accessibility
- Startup script installation

## Generate Built-in Templates

```bash
# List available templates
ae-automation generate --list

# Generate a specific template
ae-automation generate --template tutorial --output my_project.aep

# Generate all templates
ae-automation generate --all
```

## AI Content Generation with Prompture (Optional)

When the user wants AI-generated content for their videos, use Prompture to generate text, scene breakdowns, or scripts. Prompture is available at `C:\Users\Juan\Documents\GitHub\prompture`.

### Generate Video Script / Scene Text

```python
import sys
sys.path.insert(0, r"C:\Users\Juan\Documents\GitHub\prompture")

from prompture import extract_with_model
from pydantic import BaseModel

class VideoScene(BaseModel):
    title: str
    body_text: str
    duration_seconds: float
    transition_note: str

class VideoScript(BaseModel):
    scenes: list[VideoScene]
    total_duration: float

script = extract_with_model(
    VideoScript,
    "Create a 30-second product launch video script for a tech gadget. "
    "Include 4 scenes: intro, features, demo, and outro.",
    model_name="openai/gpt-4o"  # or any configured provider
)

# Now convert to AE automation config
timeline = []
current_time = 0
for i, scene in enumerate(script.json_object.scenes):
    timeline.append({
        "name": scene.title,
        "duration": scene.duration_seconds,
        "startTime": current_time,
        "template_comp": "SceneTemplate",  # user's template comp
        "reverse": False,
        "custom_actions": [
            {
                "change_type": "update_layer_property",
                "comp_name": "SceneTemplate",
                "layer_name": "Title",
                "property_name": "Text.Source Text",
                "property_type": "string",
                "value": scene.title
            },
            {
                "change_type": "update_layer_property",
                "comp_name": "SceneTemplate",
                "layer_name": "Body",
                "property_name": "Text.Source Text",
                "property_type": "string",
                "value": scene.body_text
            }
        ]
    })
    current_time += scene.duration_seconds
```

### Generate Color Palettes

```python
from pydantic import BaseModel

class ColorPalette(BaseModel):
    primary: str      # hex
    secondary: str    # hex
    accent: str       # hex
    background: str   # hex
    text: str         # hex

palette = extract_with_model(
    ColorPalette,
    "Generate a modern, professional color palette for a tech product video",
    model_name="openai/gpt-4o"
)

# Use in config actions:
# {"change_type": "update_layer_property", "property_type": "color", "value": palette.json_object.primary}
```

### Generate Titles and Copy

```python
from pydantic import BaseModel

class VideoCopy(BaseModel):
    headline: str
    subheadline: str
    cta_text: str
    bullet_points: list[str]

copy = extract_with_model(
    VideoCopy,
    f"Write compelling video copy for: {user_description}",
    model_name="openai/gpt-4o"
)
```

## Python API Quick Reference

```python
from ae_automation import Client

client = Client()

# Full pipeline from config
client.startBot("config.json")

# Individual operations (requires AE running)
client.createComp("MyComp", compWidth=1920, compHeight=1080, duration=30, frameRate=30)
client.editComp("MyComp", "Title", "Text.Source Text", "Hello World")
client.addMarker("MyComp", "Controller", "intro", 0.5)
client.renderFile("project.aep", "MyComp", "output/")

# Diagnostics
client.run_full_diagnostic()

# Template generation
from ae_automation.templates import BUILTIN_TEMPLATES
client.buildTemplate(BUILTIN_TEMPLATES["tutorial"], "output.aep")
```

## Common Patterns

### Batch Video Production

Create multiple videos from a data source:

```python
import json
from ae_automation import Client

# Load base config
with open("base_config.json") as f:
    base = json.load(f)

videos = [
    {"title": "Episode 1", "subtitle": "Getting Started", "color": "#FF5733"},
    {"title": "Episode 2", "subtitle": "Advanced Tips", "color": "#33FF57"},
]

for i, video in enumerate(videos):
    config = json.loads(json.dumps(base))  # deep copy
    config["project"]["output_file"] = f"episode_{i+1}.mp4"

    for scene in config["timeline"]:
        for action in scene["custom_actions"]:
            if action.get("layer_name") == "Title":
                action["value"] = video["title"]
            if action.get("layer_name") == "Subtitle":
                action["value"] = video["subtitle"]

    config_path = f"config_ep{i+1}.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    Client().startBot(config_path)
```

### Template Variables for Reuse

Use the `templates` section to avoid repeating actions:

```json
{
  "templates": {
    "set_scene_text": {
      "custom_actions": [
        {
          "change_type": "update_layer_property",
          "comp_name": "{comp}",
          "layer_name": "Title",
          "property_name": "Text.Source Text",
          "property_type": "string",
          "value": "{title}"
        },
        {
          "change_type": "update_layer_property",
          "comp_name": "{comp}",
          "layer_name": "Body",
          "property_name": "Text.Source Text",
          "property_type": "string",
          "value": "{body}"
        }
      ]
    }
  }
}
```

Then reference in timeline:
```json
{
  "change_type": "template",
  "template_name": "set_scene_text",
  "template_values": {
    "comp": "scene-1-ContentTemplate",
    "title": "Welcome",
    "body": "This is the intro"
  }
}
```

## Important Notes

- **Windows only** — AE automation requires Windows with After Effects installed
- **AE must not be running** when starting automation (the pipeline launches it)
- **Install startup script first** — Run `python install_ae_runner.py` to enable the file-based command queue
- **Forward slashes** in paths sent to JavaScript
- **Text sanitization** — `<br>` tags become AE carriage returns; straight quotes are preserved
- **Rendering** requires `aerender.exe` — set `AERENDER_PATH` in `.env` if not in default location
- **Debug mode** (`"debug": true`) skips AE launch — good for testing config structure
- When using Prompture for AI content, make sure the provider is configured (API keys in `.env`)
