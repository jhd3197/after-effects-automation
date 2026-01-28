---
name: ae-config-builder
description: Create and validate JSON automation configs for the After Effects automation pipeline
---

# AE Config Builder

This skill covers creating and validating JSON configuration files that drive the After Effects automation pipeline. Configs are loaded by `botMixin.startBot()` and control the entire workflow from project setup through rendering.

## Top-Level Structure

```json
{
  "project": { ... },
  "timeline": [ ... ],
  "templates": { ... }
}
```

- **`project`** (required) -- Output settings, composition parameters, and resource definitions
- **`timeline`** (required) -- Array of scene objects, each with custom actions
- **`templates`** (optional) -- Reusable action templates with variable substitution

## Project Section

All fields and their types:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project_file` | string | Yes | Path to `.aep` file (relative to config file or absolute) |
| `comp_name` | string | Yes | Main composition name in the AE project |
| `comp_fps` | number | Yes | Frame rate (e.g., `29.97`, `30`, `60`) |
| `comp_width` | number | Yes | Composition width in pixels |
| `comp_height` | number | Yes | Composition height in pixels |
| `comp_start_time` | string | No | Start time as `"HH:MM:SS"` |
| `comp_end_time` | number or string | No | End time -- seconds (e.g., `15`) or `"HH:MM:SS"` format |
| `auto_time` | boolean | No | Auto-calculate composition duration from timeline |
| `output_file` | string | Yes | Output filename (e.g., `"output.mp4"`) |
| `output_dir` | string | Yes | Output directory path (relative to config or absolute) |
| `renderComp` | boolean | No | Whether to render after building (default: `true`) |
| `debug` | boolean | No | Skip AE launch and UI interaction for testing |
| `resources` | array | No | External assets to import (see below) |

### comp_end_time Dual Format

```json
"comp_end_time": 15
"comp_end_time": "00:00:15"
```

Both are valid. The number format specifies seconds directly. The string format is parsed by `timeToFrames()`.

### Debug Mode

Setting `"debug": true` prevents AE from launching and skips all UI interaction. Useful for:
- Validating config structure
- Testing config loading
- CI/CD pipelines
- Dry-run validation

### Path Resolution

Paths in `project_file` and `output_dir` can be relative. They are resolved relative to the **config file's directory** by `startBot()`:

```json
{
  "project": {
    "project_file": ".\\my_template.aep",
    "output_dir": ".\\output"
  }
}
```

Use `.\` or `./` prefix for relative paths. Forward slashes work on all platforms.

### Resources Array

Resources are external assets (images, audio, video) imported into the AE project:

```json
"resources": [
  {
    "type": "image",
    "name": "background",
    "path": "C:/assets/bg.png"
  },
  {
    "type": "audio",
    "name": "bgm",
    "path": "C:/assets/music.mp3",
    "duration": 30
  },
  {
    "type": "video",
    "name": "footage",
    "path": "C:/assets/clip.mp4"
  }
]
```

- `type` -- `"image"`, `"audio"`, or `"video"`
- `name` -- Identifier used to reference this resource in timeline actions
- `path` -- Absolute path to the asset file
- `duration` -- Optional; for MP3 audio the duration is auto-detected if omitted

## Timeline Section

An array of scene objects processed in order:

```json
"timeline": [
  {
    "name": "intro_scene",
    "duration": 5,
    "startTime": 0,
    "template_comp": "IntroTemplate",
    "reverse": false,
    "custom_actions": [ ... ]
  },
  {
    "name": "content_scene",
    "duration": 10,
    "startTime": 5,
    "template_comp": "ContentTemplate",
    "reverse": false,
    "custom_actions": [ ... ]
  }
]
```

### Scene Object Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Scene identifier (used for folder naming via `slug()`) |
| `duration` | number | Yes | Scene duration in seconds |
| `startTime` | number | Yes | Scene start time in seconds within the main comp |
| `template_comp` | string | Yes | Name of the AE template composition to duplicate |
| `reverse` | boolean | No | Reverse the scene playback |
| `custom_actions` | array | Yes | Array of action objects to apply to this scene |

## Custom Actions

Each action object must have a `change_type` field that routes to the corresponding handler. See [references/config-schema.md](references/config-schema.md) for the complete catalogue of all 8 change types with full field definitions.

### Quick Reference

| `change_type` | Purpose |
|----------------|---------|
| `update_layer_property` | Set a layer property (text, color, position, etc.) |
| `update_layer_property_at_frame` | Set a keyframe value at a specific frame |
| `add_resource` | Add an imported resource to the timeline |
| `edit_resource` | Modify an existing resource layer's timing |
| `swap_items_by_index` | Replace a layer's source item |
| `add_marker` | Add a composition marker |
| `add_comp` | Add a nested composition to the timeline |
| `template` | Apply a reusable template with variable substitution |

## Property Dot-Notation

Layer properties use dot-separated paths that `propertyParser()` traverses:

```
"Text.Source Text"          -- Text layer content
"Text.Path Options.Path"    -- Text path
"Transform.Position"        -- Layer position [x,y]
"Transform.Scale"           -- Layer scale [x,y]
"Transform.Opacity"         -- Layer opacity (0-100)
"Transform.Rotation"        -- Layer rotation in degrees
"Effects.Color_01.Color"    -- Effect parameter (effect name.property)
"Effects.Slider_01.Slider"  -- Effect slider value
```

The first segment selects the property group, subsequent segments drill into sub-properties.

## Value Formats

### Strings
```json
"value": "Hello World"
```

### Hex Colors
```json
"value": "#FF0000",
"property_type": "color"
```

When `property_type` is `"color"`, the hex value is auto-converted to AE's normalized RGBA format (`"1.0,0.0,0.0,1"`) by `hexToRGBA()` before being sent to JSX.

### Arrays (as strings)
```json
"value": "[960,540]"
```

Arrays are passed as string representations. The `valueParser()` function in `framework.js` detects the `[` prefix and parses them into actual arrays.

### Numbers
```json
"value": "100"
```

Numeric values are also passed as strings and parsed by `valueParser()`.

## Templates Section

Define reusable action groups with `{key}` variable substitution:

```json
{
  "templates": {
    "update_title": {
      "custom_actions": [
        {
          "change_type": "update_layer_property",
          "comp_name": "{comp}",
          "layer_name": "Title",
          "property_name": "Text.Source Text",
          "property_type": "string",
          "value": "{title_text}"
        },
        {
          "change_type": "update_layer_property",
          "comp_name": "{comp}",
          "layer_name": "Title",
          "property_name": "Effects.Color_01.Color",
          "property_type": "color",
          "value": "{title_color}"
        }
      ]
    }
  },
  "timeline": [
    {
      "name": "scene_1",
      "template_comp": "SceneTemplate",
      "duration": 5,
      "startTime": 0,
      "custom_actions": [
        {
          "change_type": "template",
          "template_name": "update_title",
          "template_values": {
            "comp": "scene_1_SceneTemplate",
            "title_text": "Welcome",
            "title_color": "#FFFFFF"
          }
        }
      ]
    }
  ]
}
```

The `template` change_type looks up `data["templates"][template_name]`, replaces all `{key}` placeholders with `template_values`, then recursively processes each resulting action through `parseCustomActions()`.
