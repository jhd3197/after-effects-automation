# After Effects Automation - Examples

This directory contains practical examples demonstrating the various features and capabilities of the After Effects Automation package.

## Examples Overview

### 1. Basic Composition (`01_basic_composition.py`)
**Difficulty:** Beginner
**Features:** Client initialization, basic composition setup, timeline configuration

A simple example showing how to create a basic After Effects composition with two scenes. This is the best starting point for new users.

```bash
python examples/01_basic_composition.py
```

**What you'll learn:**
- How to initialize the Client
- Basic JSON configuration structure
- Creating simple timeline with scenes
- Project settings (resolution, FPS, duration)

---

### 2. Text Animation (`02_text_animation.py`)
**Difficulty:** Beginner
**Features:** Text layer manipulation, property updates, multi-line text

Demonstrates how to update text layers in After Effects compositions, including multi-line text with HTML breaks.

```bash
python examples/02_text_animation.py
```

**What you'll learn:**
- Updating text layer properties
- Using `update_layer_property` action
- Multi-line text with `<br>` tags
- Working with multiple text layers

---

### 3. Resource Management (`03_resource_management.py`)
**Difficulty:** Intermediate
**Features:** Importing resources, swapping items, fit-to-screen options

Shows how to import and use external resources (images, audio, video) in your compositions.

```bash
python examples/03_resource_management.py
```

**What you'll learn:**
- Importing different resource types (audio, image, video)
- Swapping placeholder items with resources
- Fit-to-screen options (fit, fit-width, fit-height)
- Resource duration management
- Adding audio to timeline

---

### 4. Markers and Timing (`04_markers_and_timing.py`)
**Difficulty:** Intermediate
**Features:** Adding markers, precise timing control, manual timeline

Demonstrates how to add markers for sync points and control precise timing in your compositions.

```bash
python examples/04_markers_and_timing.py
```

**What you'll learn:**
- Adding markers to layers
- Precise scene timing
- Manual vs automatic timing (`auto_time: false`)
- Using markers for sync points
- Scene transitions

---

### 5. Advanced Templates (`05_advanced_templates.py`)
**Difficulty:** Advanced
**Features:** Template system, variable substitution, reusable actions

Shows how to use the template system to create reusable action sets with variable substitution.

```bash
python examples/05_advanced_templates.py
```

**What you'll learn:**
- Defining reusable templates
- Template variable substitution
- Using templates across multiple scenes
- Reducing configuration redundancy
- Maintaining consistency

---

### 6. Complete Workflow (`06_complete_workflow.py`)
**Difficulty:** Advanced
**Features:** All features combined in a production-ready example

A comprehensive example demonstrating a complete video production workflow using all available features.

```bash
python examples/06_complete_workflow.py
```

**What you'll learn:**
- Complete production workflow
- Combining multiple features
- Best practices for project structure
- Resource management at scale
- Template-based production
- Professional video structure

---

## Running the Examples

All examples generate JSON configuration files. To actually run them with After Effects:

1. **Setup your environment:**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Edit .env with your After Effects paths
   ```

2. **Run an example to generate config:**
   ```bash
   python examples/01_basic_composition.py
   ```

3. **Update the generated config:**
   - Edit paths to match your After Effects project
   - Update resource paths to your actual media files
   - Ensure template composition names match your AE project

4. **Execute with After Effects:**
   ```bash
   python run.py basic_composition_config.json
   # or
   ae-automate basic_composition_config.json
   ```

## Configuration Files

Each example generates a JSON configuration file that can be used with:

- **Command line:** `python run.py config.json`
- **Package entry point:** `ae-automate config.json`
- **Web editor:** `ae-editor config.json` (then edit in browser)

## Common Actions Reference

### Update Layer Property
```json
{
    "change_type": "update_layer_property",
    "comp_name": "CompositionName",
    "layer_name": "LayerName",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": "Your text here"
}
```

### Add Resource
```json
{
    "change_type": "add_resource",
    "resource_name": "resource_name",
    "comp_name": "CompositionName",
    "startTime": "0",
    "duration": "0"
}
```

### Swap Items
```json
{
    "change_type": "swap_items_by_index",
    "layer_name": "resource_name",
    "comp_name": "CompositionName",
    "layer_index": "2",
    "fit_to_screen": true,
    "fit_to_screen_width": false,
    "fit_to_screen_height": false
}
```

### Add Marker
```json
{
    "change_type": "add_marker",
    "comp_name": "CompositionName",
    "layer_name": "layer_name",
    "marker_name": "marker_id",
    "marker_time": 5.5
}
```

### Use Template
```json
{
    "change_type": "template",
    "template_name": "templateName",
    "template_values": {
        "variable1": "value1",
        "variable2": "value2"
    }
}
```

## Property Types

Common property types and their values:

- **Text:** `"Text.Source Text"` - String value, supports `<br>` for line breaks
- **Position:** `"Transform.Position"` - Array `[x, y]` or `[x, y, z]`
- **Scale:** `"Transform.Scale"` - Array `[width%, height%]`
- **Opacity:** `"Transform.Opacity"` - Number 0-100
- **Color:** `"Effects.Fill.Color"` - Array `[r, g, b, a]` (0-1 range)

## Troubleshooting

### "Template composition not found"
Ensure the `template_comp` name in your timeline matches an actual composition in your After Effects project.

### "Resource file not found"
Update resource paths in the configuration to match your actual file locations.

### "Layer not found"
Check that layer names in custom actions match the layers in your template compositions.

### After Effects won't start
Verify that `AFTER_EFFECT_FOLDER` in your `.env` file points to the correct installation directory.

## Version Compatibility

These examples are tested with:
- ✓ After Effects 2024
- ✓ After Effects 2025 (Beta)
- ⚠ Other CC versions (should work but not officially tested)

## Additional Resources

- [Main README](../README.md) - Package documentation
- [API Documentation](../docs/) - Detailed API reference
- [Test Suite](../tests/) - Unit tests for the package
- [Compatibility Test](../test.py) - Test your AE version compatibility

## Contributing Examples

Have a useful example? Contributions are welcome!

1. Create a new example file: `XX_your_example.py`
2. Follow the existing format
3. Include clear comments and documentation
4. Test with After Effects 2024/2025
5. Submit a pull request

## License

These examples are part of the After Effects Automation package and are licensed under the MIT License.
