

# Text Animation Example

**Difficulty:** Beginner
**Estimated Time:** 10 minutes

## Overview

Learn how to manipulate text layers in After Effects using configuration-driven automation. Define your text content in Python, and the platform handles template creation, layer updates, and rendering automatically. This example shows you how to:
- Update text content dynamically
- Work with multiple text layers
- Create multi-line text with line breaks
- Use variables for dynamic content

## What You'll Learn

- Updating text layer properties
- Using `update_layer_property` action
- Multi-line text with `<br>` tags
- Working with multiple text layers in different compositions
- Dynamic text from Python variables

## Quick Start

### Step 1: Create the Template

```bash
cd examples/text_animation
python template.py
```

This creates `text_animation_template.aep` with three compositions:
- **TitleTemplate**: Multiple text layers with different styles
- **DescriptionTemplate**: Multi-line text layout
- **CreditsTemplate**: Credits with roles and names

### Step 2: Run the Automation

```bash
python run.py
```

This will update all text layers with custom content.

## Files in This Example

```
text_animation/
├── template.py                  # Creates the .aep template
├── run.py                       # Runs the automation
├── README.md                    # This file
├── text_animation_template.aep  # Generated template
├── automation_config.json       # Generated config
└── output/                      # Output directory
```

## Template Structure

### TitleTemplate
- **MainTitle**: Large title text (120px)
- **SubtitleText**: Medium subtitle (60px)
- **SmallText**: Small additional info (36px)

### DescriptionTemplate
- **Heading**: Section title
- **Description**: Multi-line body text

### CreditsTemplate
- **Role1** / **Name1**: First credit pair
- **Role2** / **Name2**: Second credit pair

## Key Concepts

### Updating Text Content

```python
{
    "change_type": "update_layer_property",
    "comp_name": "TitleTemplate",
    "layer_name": "MainTitle",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": "Your text here"
}
```

### Multi-Line Text

Use `<br>` to create line breaks:

```python
lines = [
    "First line",
    "Second line",
    "Third line"
]

value = "<br>".join(lines)
# Result: "First line<br>Second line<br>Third line"
```

### Dynamic Content from Variables

```python
video_title = "My Video Title"
video_subtitle = "Episode 1"

# Use variables in custom actions
{
    "change_type": "update_layer_property",
    "comp_name": "TitleTemplate",
    "layer_name": "MainTitle",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": video_title  # ← Use the variable
}
```

## Customization Examples

### Example 1: Tutorial Video

```python
video_title = "Python Tutorial"
video_subtitle = "Learn the Basics"
description_lines = [
    "• Variables and Data Types",
    "• Control Flow",
    "• Functions and Modules"
]
```

### Example 2: Product Demo

```python
video_title = "New Product Launch"
video_subtitle = "Revolutionary Features"
description_lines = [
    "✓ 10x Faster Performance",
    "✓ Easy to Use Interface",
    "✓ Cloud Integration"
]
```

### Example 3: Social Media Post

```python
video_title = "Daily Motivation"
video_subtitle = "Monday Inspiration"
description_lines = [
    "Success is not final",
    "Failure is not fatal",
    "Continue with courage"
]
```

## Common Text Properties

You can update these text properties:

| Property Name | Type | Description | Example Value |
|--------------|------|-------------|---------------|
| `Text.Source Text` | string | Text content | `"Hello World"` |
| `Text.Font` | string | Font name | `"Arial-Bold"` |
| `Text.Font Size` | number | Font size | `72` |
| `Transform.Position` | array | X, Y position | `[960, 540]` |
| `Transform.Opacity` | number | Opacity (0-100) | `80` |
| `Transform.Scale` | array | Scale % | `[150, 150]` |

## Advanced: Text Color

To change text color, you need to update the fill color:

```python
{
    "change_type": "update_layer_property",
    "comp_name": "TitleTemplate",
    "layer_name": "MainTitle",
    "property_name": "Text.Fill Color",  # Note: property path may vary
    "property_type": "color",
    "value": [1, 0, 0, 1]  # Red (R, G, B, A) in 0-1 range
}
```

## Tips & Tricks

### 1. Use String Formatting

```python
episode_number = 5
title = f"Episode {episode_number}: Advanced Techniques"
```

### 2. Read from File/Database

```python
import json

# Load from JSON file
with open('video_data.json') as f:
    data = json.load(f)

video_title = data['title']
video_subtitle = data['subtitle']
```

### 3. Template Variables

```python
def create_description(features):
    return "<br>".join([f"• {feature}" for feature in features])

features = ["Fast", "Reliable", "Secure"]
description = create_description(features)
# Result: "• Fast<br>• Reliable<br>• Secure"
```

## Troubleshooting

### Text doesn't update
- Check that `comp_name` and `layer_name` exactly match the template
- Property name must be exactly `"Text.Source Text"`
- Make sure `property_type` is `"string"`

### Line breaks don't work
- Use `<br>` for line breaks (not `\n`)
- Make sure text is in quotes: `"Line 1<br>Line 2"`

### Special characters appear wrong
- Ensure your strings use proper encoding
- Avoid emojis and special Unicode characters

## Next Steps

Try these other examples:

1. **resource_management/** - Add images and videos to your text
2. **markers_and_timing/** - Sync text animations with markers
3. **basic_composition/** - Start with simpler setup

## Related Documentation

- [Main README](../../README.md)
- [Examples Guide](../README.md)
- [CLI Guide](../../CLI_GUIDE.md)
