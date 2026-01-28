# Basic Composition Example

**Difficulty:** Beginner
**Estimated Time:** 5 minutes

## Overview

This example demonstrates a full end-to-end automation pipeline — from template creation to rendered MP4 — using After Effects Automation:
1. Create a template with basic compositions
2. Run automation to customize and render

Perfect starting point for new users!

## What You'll Learn

- Creating After Effects templates programmatically
- Setting up a basic timeline with multiple scenes
- Updating text properties
- Running the complete automation workflow

## Quick Start

### Step 1: Create the Template

```bash
cd examples/basic_composition
python template.py
```

This creates `basic_template.aep` with:
- **IntroTemplate**: Intro scene with title and subtitle
- **OutroTemplate**: Outro scene with closing text

### Step 2: Run the Automation

```bash
python run.py
```

This will:
1. Load the template
2. Create a final composition
3. Add intro and outro scenes
4. Update text content
5. (Optional) Render the final video

## Files in This Example

```
basic_composition/
├── template.py          # Creates the .aep template
├── run.py               # Runs the automation workflow
├── README.md            # This file
├── basic_template.aep   # Generated template (after running template.py)
├── automation_config.json  # Generated config (after running run.py)
└── output/              # Output directory (created automatically)
    └── basic_output.mp4 # Final video (if renderComp is True)
```

## Template Structure

### IntroTemplate
- **Duration:** 5 seconds
- **Layers:**
  - Background (solid, dark blue-gray)
  - MainTitle (text, large)
  - Subtitle (text, smaller)

### OutroTemplate
- **Duration:** 5 seconds
- **Layers:**
  - Background (solid, dark red-gray)
  - ClosingText (text)

## Customization

### Change Text Content

Edit `run.py`, find the `custom_actions` section:

```python
{
    "change_type": "update_layer_property",
    "comp_name": "IntroTemplate",
    "layer_name": "MainTitle",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": "Your Custom Title Here"  # ← Change this
}
```

### Enable Video Rendering

In `run.py`, set:

```python
"renderComp": True,  # Set to True to render the final video
```

### Change Duration

Modify the timeline in `run.py`:

```python
{
    "name": "intro",
    "duration": 8,  # ← Change from 5 to 8 seconds
    "startTime": 0,
    "template_comp": "IntroTemplate",
    ...
}
```

### Customize Template

After running `template.py`, open `basic_template.aep` in After Effects:
- Customize colors, fonts, sizes
- Add animations
- Add effects
- Save and re-run `run.py`

## Troubleshooting

### "Template not found" error
Run `python template.py` first to create the template.

### After Effects doesn't start
1. Make sure After Effects is installed
2. Check your `.env` file has correct `AFTER_EFFECT_FOLDER` path
3. Make sure the startup script is installed: `python install_ae_runner.py`

### "Composition not found" error
The template may not have been created properly. Delete `basic_template.aep` and run `template.py` again.

## Next Steps

Once you're comfortable with this example, try:

1. **text_animation/** - Learn advanced text manipulation
2. **resource_management/** - Import and use images, video, audio
3. **markers_and_timing/** - Precise timing control

## Configuration Reference

### Project Settings

```python
"project": {
    "project_file": "path/to/template.aep",     # Template path
    "comp_name": "FinalComposition",            # Output comp name
    "comp_fps": 29.97,                          # Frame rate
    "comp_width": 1920,                         # Width in pixels
    "comp_height": 1080,                        # Height in pixels
    "auto_time": True,                          # Auto-calculate timing
    "comp_end_time": 10,                        # Total duration (seconds)
    "renderComp": True,                         # Render video?
    "output_file": "output.mp4",                # Output filename
    "output_dir": "./output"                    # Output directory
}
```

### Timeline Scene

```python
{
    "name": "scene_name",                       # Scene identifier
    "duration": 5,                              # Duration in seconds
    "startTime": 0,                             # Start time in timeline
    "template_comp": "TemplateName",            # Source composition
    "reverse": False,                           # Play in reverse?
    "custom_actions": [...]                     # Actions to perform
}
```

## Related Documentation

- [Main README](../../README.md)
- [Export Guide](../../EXPORT_GUIDE.md)
- [CLI Guide](../../CLI_GUIDE.md)
