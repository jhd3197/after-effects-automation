---
name: jsx-script-creator
description: Create ExtendScript/JSX files that integrate with the Python-to-AE file-based command bridge
---

# JSX Script Creator

This skill covers creating `.jsx` ExtendScript files for the After Effects automation bridge. Scripts live in `ae_automation/mixins/js/` and are executed by Python's `runScript()` method.

## How Scripts Are Executed

Python's `runScript()` in `ae_automation/mixins/afterEffect.py` does the following before sending a script to AE:

1. Reads the `.jsx` file from `ae_automation/mixins/js/`
2. Applies placeholder replacements from a `_remplacements` dict
3. **Prepends** minified `json2.js` + `framework.js` (all utility functions are available)
4. **Wraps** the script body in `try { ... } catch(e) { _error = e.lineNumber + ' ' + e.toString(); } outputLogs(_error);`
5. Writes the composed script to the cache folder
6. Copies it to the queue folder for AE to pick up

**Critical implication:** Your scripts must NOT include top-level try/catch or error handling. The wrapper handles that. Your script body is inserted directly into the `try` block.

## Header Comment Convention

Use this format at the top of every new JSX file:

```javascript
//
// <Descriptive Title>
// ------------------------------------------------------------
// Language: javascript
//
```

For simpler utility scripts, a shorter header is acceptable:

```javascript
// <One-line description>
// Parameters: {param1}, {param2}, ...
```

## Placeholder Syntax (Critical)

Placeholders use `{name}` notation. The distinction between quoted and bare is essential:

### String parameters -- QUOTED: `"{paramName}"`

```javascript
var comp = FindItemByName("{comp_name}");
var layer = FindLayerByComp("{comp_name}", "{layer_name}");
saveFile("{output_file}", JSON.stringify(data));
```

When Python does `fileContent.replace("{comp_name}", "MyComp")`, the result is `"MyComp"` -- a valid JS string literal.

### Numeric parameters -- BARE: `{paramName}`

```javascript
var c = app.project.items.addComp("{compName}", {compWidth}, {compHeight}, {pixelAspect}, {duration}, {frameRate});
layer.startTime = {startTime};
layer.stretch = {stretch};
```

When Python replaces `{compWidth}` with `1920`, the result is the bare number `1920` -- a valid JS number literal.

### Rule of thumb

- If the value should be a JavaScript string: wrap placeholder in double quotes `"{param}"`
- If the value should be a JavaScript number: use bare `{param}`
- If the value could be either (e.g., a property value): use `"{param}"` and parse at runtime with `valueParser()`

### Python-side replacement dict

Keys in the `_remplacements` dict **must include the braces**:

```python
self.runScript("my_script.jsx", {
    "{comp_name}": str(comp_name),
    "{layer_name}": str(layer_name),
    "{startTime}": str(start_time),  # str() even for numbers -- it's string replacement
    "{duration}": str(duration),
})
```

## Available framework.js Utilities

These functions are automatically available in every script (prepended by `runScript()`):

| Function | Signature | Description |
|----------|-----------|-------------|
| `FindItemByName` | `FindItemByName(name)` | Returns the AE project item matching `name`, or `null` |
| `FindItemIdByName` | `FindItemIdByName(name)` | Returns 1-based index of item matching `name`, or `null` |
| `FindLayerByComp` | `FindLayerByComp(compName, layerName)` | Finds a layer by name within a named composition |
| `FindLayerByLayerIndex` | `FindLayerByLayerIndex(compName, layerIndex)` | Finds a layer by 1-based index within a named composition |
| `slugify` | `slugify(str)` | Converts string to URL-safe lowercase slug |
| `saveFile` | `saveFile(fileName, fileContent)` | Writes content to a file in `CACHE_FOLDER` |
| `print` | `print(log, log2, log3)` | Appends timestamped log entry (up to 3 args) to internal log buffer |
| `outputLogs` | `outputLogs(finalLog, debug)` | Writes accumulated logs to `.log` file (called automatically by wrapper) |
| `decodeHTMLEntities` | `decodeHTMLEntities(text)` | Decodes `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&apos;`, `&#44;`, `&nbsp;` |
| `propertyParser` | `propertyParser(property, propertyName)` | Traverses AE property hierarchy by splitting `propertyName` on `.` |
| `valueParser` | `valueParser(propertyValue)` | Parses string value: detects `[x,y,z]` arrays or decodes HTML entities |
| `deselectAll` | `deselectAll()` | Deselects all items in the AE project panel |
| `deselectAllLayers` | `deselectAllLayers()` | Deselects all layers in the active composition |

### Global variables

- `CACHE_FODLER` -- Path to cache directory (note: typo is intentional, do not fix)
- `LOG_OUTPUT` -- Boolean flag for log output
- `_LOGS` -- Internal log accumulator string

## AE 1-Based Indexing

After Effects uses **1-based indexing** everywhere:

```javascript
// Project items: app.project.item(1) is the first item
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
}

// Layers: comp.layer(1) is the topmost layer
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
}
```

**New layers are always added at index 1** (topmost position in the layer stack).

## Data Return Pattern

To send data back from AE to Python:

### In JSX:
```javascript
var result = {};
result.items = [];
for (var i = 1; i <= app.project.numItems; i++) {
    result.items.push({ name: app.project.item(i).name, index: i });
}
saveFile("output.json", JSON.stringify(result));
```

### In Python:
```python
import json
from ae_automation import settings

random_name = self.runScript("my_script.jsx", replacements)
time.sleep(2)  # wait for AE to finish

output_path = os.path.join(settings.CACHE_FOLDER, "output.json")
with open(output_path, "r") as f:
    data = json.load(f)
```

## Structural Patterns

### Pattern 1: Function + Call (preferred for complex logic)

```javascript
//
// Update Layer Opacity
// ------------------------------------------------------------
// Language: javascript
//

function updateOpacity(compName, layerName, opacity) {
    var comp = FindItemByName(compName);
    if (!comp) {
        print("Comp not found: " + compName);
        return;
    }
    var layer = FindLayerByComp(compName, layerName);
    if (!layer) {
        print("Layer not found: " + layerName);
        return;
    }
    layer.opacity.setValue(opacity);
    print("Set opacity to " + opacity);
}

updateOpacity("{comp_name}", "{layer_name}", {opacity});
```

### Pattern 2: Inline Script (for simple operations)

```javascript
//
// Select Item By Name
// ------------------------------------------------------------
// Language: javascript
//

deselectAll();
var _id = FindItemIdByName("{itemName}");
if (_id !== null) {
    app.project.item(_id).selected = true;
    print("Selected: {itemName}");
}
```

## ES3 Constraints

After Effects ExtendScript uses **ECMAScript 3**. The following modern JS features are NOT available:

| Forbidden | Use instead |
|-----------|-------------|
| `let` / `const` | `var` |
| Arrow functions `() => {}` | `function() {}` |
| Template literals `` `${x}` `` | String concatenation `"" + x` |
| `Array.forEach()` | `for` loop with index |
| `Array.map()` / `filter()` / `reduce()` | Manual `for` loop |
| `Array.indexOf()` (unreliable) | Manual `for` loop comparison |
| `Object.keys()` | `for (var k in obj)` with `hasOwnProperty` |
| `JSON.parse()` / `JSON.stringify()` | Available via `json2.js` (auto-included) |
| `===` / `!==` | Works, but be aware ExtendScript has quirks |
| `try/catch` at top level | Handled by wrapper -- do NOT add your own |
| Default parameters | Check with `if (param === undefined)` |

## Complete Example: New JSX Script

Here is a complete example of a script that collects composition info:

```javascript
//
// Get Composition Details
// ------------------------------------------------------------
// Language: javascript
//

function getCompDetails(compName) {
    var comp = FindItemByName(compName);
    if (!comp) {
        print("Composition not found: " + compName);
        return;
    }

    var details = {
        name: comp.name,
        width: comp.width,
        height: comp.height,
        duration: comp.duration,
        frameRate: comp.frameRate,
        numLayers: comp.numLayers,
        layers: []
    };

    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        details.layers.push({
            index: i,
            name: layer.name,
            inPoint: layer.inPoint,
            outPoint: layer.outPoint,
            enabled: layer.enabled
        });
    }

    saveFile("comp_details.json", JSON.stringify(details));
    print("Saved details for " + compName + " with " + comp.numLayers + " layers");
}

getCompDetails("{comp_name}");
```

And the Python side to call it:

```python
def getCompDetails(self, comp_name):
    self.runScript("get_comp_details.jsx", {
        "{comp_name}": str(comp_name),
    })
    time.sleep(2)

    output_path = os.path.join(settings.CACHE_FOLDER, "comp_details.json")
    with open(output_path, "r") as f:
        return json.load(f)
```
