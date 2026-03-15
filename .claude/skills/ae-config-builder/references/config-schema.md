# Config Schema Reference

Complete catalogue of all `change_type` values with required and optional fields.

## 1. `update_layer_property`

Set a property on a named layer within a composition.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"update_layer_property"` | Yes | Action identifier |
| `comp_name` | string | Yes | Target composition name |
| `layer_name` | string | Yes | Target layer name |
| `property_name` | string | Yes | Dot-notation property path (e.g., `"Text.Source Text"`) |
| `property_type` | string | Yes | `"string"`, `"color"`, `"number"`, `"array"` |
| `value` | string | Yes | The value to set |

**Python handler:** `editComp()` -> `update_properties.jsx`

```json
{
  "change_type": "update_layer_property",
  "comp_name": "scene_1_IntroTemplate",
  "layer_name": "MainTitle",
  "property_name": "Text.Source Text",
  "property_type": "string",
  "value": "Hello World"
}
```

---

## 2. `update_layer_property_at_frame`

Set a keyframe value at a specific frame number.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"update_layer_property_at_frame"` | Yes | Action identifier |
| `comp_name` | string | Yes | Target composition name |
| `layer_name` | string | Yes | Target layer name |
| `property_name` | string | Yes | Dot-notation property path |
| `value` | string | Yes | The keyframe value |
| `frame` | number | Yes | Frame number for the keyframe |

**Python handler:** `editLayerAtKey()` -> `update_properties_frame.jsx`

```json
{
  "change_type": "update_layer_property_at_frame",
  "comp_name": "scene_1_IntroTemplate",
  "layer_name": "Animator",
  "property_name": "Transform.Position",
  "value": "[960,540]",
  "frame": 15
}
```

---

## 3. `add_resource`

Add an imported resource (image, video, audio) to the timeline.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"add_resource"` | Yes | Action identifier |
| `resource_name` | string | Yes | Name matching a resource in `project.resources` |
| `comp_name` | string | Yes | Target composition to add the resource to |
| `startTime` | number | Yes | Start time in seconds within the composition |
| `duration` | number | Yes | Duration in seconds |
| `moveToEnd` | boolean | No | Move layer to bottom of layer stack |

**Python handler:** `addResourceToTimeline()` -> `add_resource.jsx`

```json
{
  "change_type": "add_resource",
  "resource_name": "background_image",
  "comp_name": "scene_1_IntroTemplate",
  "startTime": 0,
  "duration": 5,
  "moveToEnd": true
}
```

---

## 4. `edit_resource`

Modify timing properties of an existing resource layer by index.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"edit_resource"` | Yes | Action identifier |
| `comp_name` | string | Yes | Target composition name |
| `layerIndex` | number | Yes | 1-based layer index |
| `startTime` | number | Yes | New start time in seconds |
| `duration` | number | Yes | New duration in seconds |
| `moveToEnd` | boolean | No | Move layer to bottom of layer stack |

**Python handler:** `updateLayerProperties()` -> `update_resource.jsx`

```json
{
  "change_type": "edit_resource",
  "comp_name": "scene_1_IntroTemplate",
  "layerIndex": 3,
  "startTime": 2,
  "duration": 8,
  "moveToEnd": false
}
```

---

## 5. `swap_items_by_index`

Replace a layer's source item (swap footage/image/comp).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"swap_items_by_index"` | Yes | Action identifier |
| `comp_name` | string | Yes | Target composition name |
| `layer_index` | number | Yes | 1-based layer index to swap |
| `layer_name` | string | Yes | Name of the new source item |
| `fit_to_screen` | boolean | No | Auto-fit the new item to comp dimensions |
| `fit_to_screen_width` | number | No | Target width for fit-to-screen |
| `fit_to_screen_height` | number | No | Target height for fit-to-screen |

**Python handler:** `swapItem()` (uses pyautogui for fit-to-screen hotkeys)

```json
{
  "change_type": "swap_items_by_index",
  "comp_name": "scene_1_IntroTemplate",
  "layer_index": 2,
  "layer_name": "new_footage",
  "fit_to_screen": true,
  "fit_to_screen_width": 1920,
  "fit_to_screen_height": 1080
}
```

---

## 6. `add_marker`

Add a marker to a layer in a composition.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"add_marker"` | Yes | Action identifier |
| `comp_name` | string | Yes | Target composition name |
| `layer_name` | string | Yes | Target layer name |
| `marker_name` | string | Yes | Marker comment text |
| `marker_time` | number | Yes | Time position in seconds |

**Python handler:** `addMarker()` -> `add_marker.jsx`

```json
{
  "change_type": "add_marker",
  "comp_name": "scene_1_IntroTemplate",
  "layer_name": "Controller",
  "marker_name": "transition_start",
  "marker_time": 2.5
}
```

---

## 7. `template`

Apply a reusable template with variable substitution.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"template"` | Yes | Action identifier |
| `template_name` | string | Yes | Key in the top-level `"templates"` object |
| `template_values` | object | Yes | Key-value pairs for `{placeholder}` replacement |

**Python handler:** Recursive -- looks up template, substitutes values, then re-processes each action through `parseCustomActions()`.

```json
{
  "change_type": "template",
  "template_name": "set_scene_text",
  "template_values": {
    "comp": "scene_1_SceneTemplate",
    "heading": "Introduction",
    "subheading": "Welcome to the tutorial"
  }
}
```

---

## 8. `add_comp`

Add a nested composition to the timeline (duplicates a template comp and places it).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `change_type` | `"add_comp"` | Yes | Action identifier |
| `comp_name` | string | Yes | Template composition name to duplicate |
| `startTime` | number | Yes | Start time in seconds |
| `duration` | number | Yes | Duration in seconds |

**Python handler:** `addCompToTimeline()` -> `duplicate_comp_2.jsx`

```json
{
  "change_type": "add_comp",
  "comp_name": "OverlayTemplate",
  "startTime": 3,
  "duration": 7
}
```

---

## Complete Example Config

A config demonstrating every change_type:

```json
{
  "project": {
    "project_file": ".\\demo_template.aep",
    "comp_name": "MainComp",
    "comp_fps": 30,
    "comp_width": 1920,
    "comp_height": 1080,
    "comp_start_time": "00:00:00",
    "comp_end_time": 30,
    "auto_time": false,
    "output_file": "demo_output.mp4",
    "output_dir": ".\\output",
    "renderComp": true,
    "debug": false,
    "resources": [
      {
        "type": "image",
        "name": "hero_bg",
        "path": "C:/assets/hero.png"
      },
      {
        "type": "audio",
        "name": "bgm",
        "path": "C:/assets/music.mp3",
        "duration": 30
      }
    ]
  },
  "templates": {
    "set_title": {
      "custom_actions": [
        {
          "change_type": "update_layer_property",
          "comp_name": "{comp}",
          "layer_name": "Title",
          "property_name": "Text.Source Text",
          "property_type": "string",
          "value": "{text}"
        }
      ]
    }
  },
  "timeline": [
    {
      "name": "intro",
      "duration": 10,
      "startTime": 0,
      "template_comp": "IntroTemplate",
      "reverse": false,
      "custom_actions": [
        {
          "change_type": "update_layer_property",
          "comp_name": "intro_IntroTemplate",
          "layer_name": "Heading",
          "property_name": "Text.Source Text",
          "property_type": "string",
          "value": "Welcome to the Demo"
        },
        {
          "change_type": "update_layer_property",
          "comp_name": "intro_IntroTemplate",
          "layer_name": "Background",
          "property_name": "Effects.Color_01.Color",
          "property_type": "color",
          "value": "#1A1A2E"
        },
        {
          "change_type": "update_layer_property_at_frame",
          "comp_name": "intro_IntroTemplate",
          "layer_name": "Animator",
          "property_name": "Transform.Position",
          "value": "[960,540]",
          "frame": 30
        },
        {
          "change_type": "add_resource",
          "resource_name": "hero_bg",
          "comp_name": "intro_IntroTemplate",
          "startTime": 0,
          "duration": 10,
          "moveToEnd": true
        },
        {
          "change_type": "add_marker",
          "comp_name": "intro_IntroTemplate",
          "layer_name": "Controller",
          "marker_name": "fade_in",
          "marker_time": 0.5
        }
      ]
    },
    {
      "name": "content",
      "duration": 15,
      "startTime": 10,
      "template_comp": "ContentTemplate",
      "reverse": false,
      "custom_actions": [
        {
          "change_type": "template",
          "template_name": "set_title",
          "template_values": {
            "comp": "content_ContentTemplate",
            "text": "Main Content"
          }
        },
        {
          "change_type": "edit_resource",
          "comp_name": "content_ContentTemplate",
          "layerIndex": 2,
          "startTime": 0,
          "duration": 15,
          "moveToEnd": false
        },
        {
          "change_type": "swap_items_by_index",
          "comp_name": "content_ContentTemplate",
          "layer_index": 3,
          "layer_name": "hero_bg",
          "fit_to_screen": true,
          "fit_to_screen_width": 1920,
          "fit_to_screen_height": 1080
        },
        {
          "change_type": "add_comp",
          "comp_name": "OverlayTemplate",
          "startTime": 2,
          "duration": 10
        }
      ]
    }
  ]
}
```
