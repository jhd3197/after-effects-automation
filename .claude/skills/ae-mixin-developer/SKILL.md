---
name: ae-mixin-developer
description: Add methods to existing mixins or create new mixins for the After Effects automation client
---

# AE Mixin Developer

This skill covers adding methods to the mixin-based Client architecture and creating new mixins. The Client class in `ae_automation/__init__.py` composes six mixins via multiple inheritance.

## Mixin Composition

The Client is assembled in `ae_automation/__init__.py`:

```python
class Client(
    afterEffectMixin,       # ae_automation/mixins/afterEffect.py
    ToolsMixin,             # ae_automation/mixins/tools.py
    botMixin,               # ae_automation/mixins/bot.py
    VideoEditorAppMixin,    # ae_automation/mixins/VideoEditorApp.py
    TemplateGeneratorMixin, # ae_automation/mixins/templateGenerator.py
    ProcessManagerMixin,    # ae_automation/mixins/processManager.py
):
    JS_FRAMEWORK = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Loads settings, creates cache folder, reads json2.js + framework.js
        # Replaces {CACHE_FOLDER} in framework.js with actual path (forward slashes)
```

Methods from any mixin are accessible as `self.methodName()` on the Client instance. All mixins share `self` state.

## The runScript() Pattern

The core bridge between Python and AE. Located in `afterEffect.py`:

```python
def runScript(self, fileName, _remplacements=None, debug=False):
```

### Replacement Dict Rules

Keys **must include braces**. Values **must be strings** (it's string replacement, not formatting):

```python
self.runScript("my_script.jsx", {
    "{comp_name}": str(comp_name),
    "{layer_name}": str(layer_name),
    "{startTime}": str(start_time),
    "{duration}": str(duration),
    "{value}": str(value),
})
```

**Common mistake:** Forgetting braces in keys.

```python
# WRONG -- placeholder won't be found
{"comp_name": str(comp_name)}

# CORRECT
{"{comp_name}": str(comp_name)}
```

### What runScript() Does

1. Reads the JSX file from `settings.JS_DIR`
2. Applies all replacements from the dict
3. Prepends minified `JS_FRAMEWORK` (json2.js + framework.js)
4. Wraps in `try { ... } catch(e) { ... } outputLogs(_error);`
5. Writes composed script to `settings.CACHE_FOLDER`
6. Sends to AE via the file-based queue system
7. Returns a UUID string (useful for reading log output)

## Text Sanitization

Always call `self.sanitize_text_for_ae()` on any user-facing text before passing it to JSX. This method:

- Converts HTML `<br>` tags (all variants) to AE carriage returns (`\r`)
- Preserves straight quotes to avoid UTF-8 encoding issues

```python
def myMethod(self, comp_name, layer_name, text):
    sanitized = self.sanitize_text_for_ae(text)
    self.runScript("my_script.jsx", {
        "{comp_name}": str(comp_name),
        "{layer_name}": str(layer_name),
        "{value}": str(sanitized),
    })
```

**When to call it:** Any time the value comes from user input or config and might contain HTML or special characters. The existing `editComp()` and `editLayerAtKey()` methods call it automatically.

## Path Handling

JavaScript/ExtendScript requires forward slashes in file paths. When constructing paths for JSX:

```python
# Convert backslashes to forward slashes for JS
js_path = path.replace("\\", "/")

self.runScript("import_file.jsx", {
    "{filePath}": js_path,
})
```

The settings module handles this for `CACHE_FOLDER` already (see `__init__.py` constructor), but any new paths you construct must be converted manually.

## Color Handling

`self.hexToRGBA()` converts hex color strings to AE's normalized RGBA format:

```python
color = self.hexToRGBA("#FF0000")
# Returns: "1.0,0.0,0.0,1"
```

The returned string is comma-separated with values in 0.0-1.0 range, with alpha always `1`. This is the format AE expects for color properties.

In `parseCustomActions()`, this conversion happens automatically when `property_type == "color"`:

```python
if "property_type" in custom_edit:
    if custom_edit["property_type"] == "color":
        custom_edit["value"] = self.hexToRGBA(custom_edit["value"])
```

## Method Naming Conventions

The codebase uses mixed conventions. Follow the convention of the mixin you're modifying:

| Mixin | Convention | Examples |
|-------|------------|----------|
| `afterEffectMixin` | camelCase | `startAfterEffect()`, `createComp()`, `editComp()`, `runScript()` |
| `ToolsMixin` | camelCase | `hexToRGBA()`, `testFunction()`, `previewLogs()` |
| `botMixin` | camelCase | `startBot()` |
| `ProcessManagerMixin` | snake_case | `wait_for_process()`, `is_after_effects_responsive()` |
| `TemplateGeneratorMixin` | camelCase | `createNewProject()`, `saveProject()`, `addTextLayer()` |
| `VideoEditorAppMixin` | camelCase | Flask routes |

When creating a **new** mixin, prefer snake_case (the modern convention used in `ProcessManagerMixin`).

## Wait Patterns

After calling `runScript()`, you need to wait for AE to execute the script. The wait time depends on operation complexity:

```python
# Simple property change
self.runScript("update_properties.jsx", replacements)
time.sleep(1)

# File import or composition creation
self.runScript("add_resource.jsx", replacements)
time.sleep(2)

# Complex operation (duplication, rendering setup)
self.runScript("duplicate_comp_2.jsx", replacements)
time.sleep(3)

# Very complex (full project creation)
self.runScript("create_new_project.jsx", replacements)
time.sleep(5)
```

The base `runScript()` already has a `time.sleep(1)` at the end. Additional sleeps in your method are on top of that.

For more reliable waiting, use the `ProcessManagerMixin` pattern:

```python
self.safe_script_execution("my_script.jsx", replacements, wait_time=3)
```

## Reading Data Back from AE

JSX scripts can write data files that Python reads:

### JSX side (in your `.jsx` file):
```javascript
var result = { items: [] };
// ... populate result ...
saveFile("my_output.json", JSON.stringify(result));
```

### Python side (in your mixin method):
```python
import json
from ae_automation import settings

def getMyData(self, comp_name):
    self.runScript("my_data_script.jsx", {
        "{comp_name}": str(comp_name),
    })
    time.sleep(2)  # wait for AE to write the file

    output_path = os.path.join(settings.CACHE_FOLDER, "my_output.json")
    with open(output_path, "r", encoding="utf-8") as f:
        return json.load(f)
```

## Creating a New Mixin

### 1. Create the mixin file

`ae_automation/mixins/my_feature.py`:

```python
"""
My Feature Mixin
Provides functionality for [description]
"""
import os
import time
from ae_automation import settings


class MyFeatureMixin:
    """Mixin that adds [feature] capabilities to the Client."""

    def do_something(self, comp_name, value):
        """
        Description of what this method does.

        Args:
            comp_name: Name of the target composition
            value: The value to set
        """
        sanitized_value = self.sanitize_text_for_ae(value)

        self.runScript("my_script.jsx", {
            "{comp_name}": str(comp_name),
            "{value}": str(sanitized_value),
        })
        time.sleep(2)

    def get_data(self):
        """Retrieve data from AE."""
        self.runScript("get_data.jsx")
        time.sleep(2)

        output_path = os.path.join(settings.CACHE_FOLDER, "data_output.json")
        import json
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)
```

### 2. Register the mixin in `__init__.py`

Add the import and include it in the Client class:

```python
from ae_automation.mixins.my_feature import MyFeatureMixin

class Client(
    afterEffectMixin,
    ToolsMixin,
    botMixin,
    VideoEditorAppMixin,
    TemplateGeneratorMixin,
    ProcessManagerMixin,
    MyFeatureMixin,          # Add here
):
```

### 3. Create corresponding JSX scripts

Place them in `ae_automation/mixins/js/` following the patterns in the jsx-script-creator skill.

## Settings Module Constants

Available via `from ae_automation import settings`:

| Constant | Description |
|----------|-------------|
| `settings.CACHE_FOLDER` | Cache directory for temp files and script output |
| `settings.QUEUE_FOLDER` | Queue directory monitored by AE command runner |
| `settings.AFTER_EFFECT_FOLDER` | AE installation path |
| `settings.AFTER_EFFECT_PROJECT_FOLDER` | AE project folder name |
| `settings.AERENDER_PATH` | Path to `aerender.exe` |
| `settings.PACKAGE_DIR` | Root directory of the ae_automation package |
| `settings.JS_DIR` | Directory containing JSX/JS scripts |

## Adding a New change_type

To add a new action type to the config system:

### 1. Add the handler in `parseCustomActions()`

In `ae_automation/mixins/afterEffect.py`, add a new `if` block:

```python
def parseCustomActions(self, custom_edit, scene_folder, itemTimeline, data):
    # ... existing handlers ...

    if custom_edit["change_type"] == "my_new_action":
        self.myNewAction(
            self.slug(scene_folder) + "_" + custom_edit["comp_name"],
            custom_edit["other_field"],
        )
```

**Note the `self.slug()` prefix pattern:** Scene-specific compositions are named `{scene_slug}_{template_comp}`. The `slug()` method (from `ToolsMixin`) creates a URL-safe version of the scene folder name.

### 2. Implement the method

```python
def myNewAction(self, comp_name, other_field):
    self.runScript("my_new_action.jsx", {
        "{comp_name}": str(comp_name),
        "{other_field}": str(other_field),
    })
    time.sleep(2)
```

### 3. Create the JSX script

`ae_automation/mixins/js/my_new_action.jsx` -- see the jsx-script-creator skill.

### 4. Document in config schema

Add the new change_type to the config-schema reference.

## Complete Example: Adding a Layer Visibility Toggle

### JSX script (`ae_automation/mixins/js/toggle_layer_visibility.jsx`):

```javascript
//
// Toggle Layer Visibility
// ------------------------------------------------------------
// Language: javascript
//

function toggleLayerVisibility(compName, layerName, visible) {
    var comp = FindItemByName(compName);
    if (!comp) {
        print("Composition not found: " + compName);
        return;
    }
    var layer = FindLayerByComp(compName, layerName);
    if (!layer) {
        print("Layer not found: " + layerName);
        return;
    }
    layer.enabled = visible;
    print("Set " + layerName + " visibility to " + visible);
}

toggleLayerVisibility("{comp_name}", "{layer_name}", {visible});
```

### Python method (in `afterEffect.py` or a new mixin):

```python
def toggleLayerVisibility(self, comp_name, layer_name, visible):
    self.runScript("toggle_layer_visibility.jsx", {
        "{comp_name}": str(comp_name),
        "{layer_name}": str(layer_name),
        "{visible}": "true" if visible else "false",
    })
    time.sleep(1)
```

### Config integration (in `parseCustomActions()`):

```python
if custom_edit["change_type"] == "toggle_visibility":
    self.toggleLayerVisibility(
        self.slug(scene_folder) + "_" + custom_edit["comp_name"],
        custom_edit["layer_name"],
        custom_edit.get("visible", True),
    )
```

### Config usage:

```json
{
  "change_type": "toggle_visibility",
  "comp_name": "IntroTemplate",
  "layer_name": "Watermark",
  "visible": false
}
```
