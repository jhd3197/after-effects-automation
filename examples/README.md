# After Effects Automation - Examples

Practical, self-contained examples demonstrating After Effects automation capabilities.

## 📁 Structure

Each example is in its own folder with:
- **template.py** - Creates the After Effects template (.aep)
- **run.py** - Runs the automation workflow
- **README.md** - Detailed instructions and explanations

## 🎯 Quick Start

```bash
# Pick an example
cd examples/basic_composition

# Step 1: Create the template
python template.py

# Step 2: Run the automation
python run.py
```

That's it! The automation will create compositions, update text, and optionally render video.

---

## 📚 Examples

### 1. Basic Composition
**Path:** `examples/basic_composition/`
**Difficulty:** ⭐ Beginner
**Time:** ~5 minutes

Learn the fundamentals:
- Creating templates with multiple compositions
- Setting up a timeline with scenes
- Updating text properties
- Complete automation workflow

**Perfect for:** First-time users

```bash
cd examples/basic_composition
python template.py
python run.py
```

[Full Instructions →](basic_composition/README.md)

---

### 2. Text Animation
**Path:** `examples/text_animation/`
**Difficulty:** ⭐ Beginner
**Time:** ~10 minutes

Master text manipulation:
- Multiple text layers with different styles
- Multi-line text with line breaks
- Dynamic content from Python variables
- Advanced text property updates

**Perfect for:** Tutorial videos, social media posts

```bash
cd examples/text_animation
python template.py
python run.py
```

[Full Instructions →](text_animation/README.md)

---

## 🗂️ Legacy Examples

Older numbered examples are still available in the examples folder:
- `01_basic_composition.py` - Generates config only
- `02_text_animation.py` - Generates config only
- `03_resource_management.py` - Resource imports
- `04_markers_and_timing.py` - Precise timing
- `05_advanced_templates.py` - Template system
- `06_complete_workflow.py` - Full production workflow

**Note:** Legacy examples only generate JSON configs. Use the new folder-based examples for complete workflows.

---

## 🎓 Learning Path

### Beginner Path
1. **basic_composition** - Start here to learn the basics
2. **text_animation** - Learn text manipulation

### Intermediate Path (Coming Soon)
3. **resource_management** - Work with images, video, audio
4. **markers_and_timing** - Precise timing control

### Advanced Path (Coming Soon)
5. **template_system** - Reusable templates
6. **complete_workflow** - Production-ready example

---

## 🛠️ Example Structure

Each example folder contains:

```
example_name/
├── template.py              # Creates the .aep template
├── run.py                   # Runs the automation
├── README.md                # Detailed instructions
├── example_template.aep     # Generated template (git-ignored)
├── automation_config.json   # Generated config (git-ignored)
└── output/                  # Output folder (git-ignored)
    └── final_video.mp4      # Rendered video
```

---

## 🚀 Common Workflows

### Create Template Only

```bash
cd examples/basic_composition
python template.py
```

Then open `basic_template.aep` in After Effects to customize.

### Run Automation Without Rendering

In `run.py`, set:
```python
"renderComp": False
```

### Render Video

In `run.py`, set:
```python
"renderComp": True
```

The video will be saved to the `output/` folder.

### Customize Template

1. Run `template.py` to create the .aep file
2. Open in After Effects
3. Customize colors, fonts, animations
4. Save
5. Run `run.py` - it will use your customized template

---

## 📖 Configuration Reference

### Project Settings

```python
"project": {
    "project_file": "path/to/template.aep",  # Template path
    "comp_name": "FinalComposition",         # Output comp name
    "comp_fps": 29.97,                       # Frame rate
    "comp_width": 1920,                      # Resolution width
    "comp_height": 1080,                     # Resolution height
    "auto_time": True,                       # Auto-calculate timing
    "comp_end_time": 10,                     # Total duration (seconds)
    "renderComp": True,                      # Render video?
    "output_file": "output.mp4",             # Output filename
    "output_dir": "./output"                 # Output directory
}
```

### Timeline Scene

```python
{
    "name": "scene_name",              # Scene identifier
    "duration": 5,                     # Duration in seconds
    "startTime": 0,                    # Start time in timeline
    "template_comp": "TemplateName",   # Source composition from template
    "custom_actions": [...]            # Actions to perform on this scene
}
```

### Update Text Action

```python
{
    "change_type": "update_layer_property",
    "comp_name": "CompositionName",
    "layer_name": "LayerName",
    "property_name": "Text.Source Text",
    "property_type": "string",
    "value": "Your text here"
}
```

---

## 🔧 Prerequisites

### Required

1. **After Effects** installed (2024 or 2025)
2. **Python 3.7+** with `ae-automation` package
3. **Startup Script** installed:
   ```bash
   python install_ae_runner.py
   ```

### Setup

1. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your After Effects path
   ```

2. **Install the package:**
   ```bash
   pip install -e .
   ```

3. **Verify setup:**
   ```bash
   ae-automation diagnose
   ```

---

## ❓ Troubleshooting

### "Template not found" error
**Solution:** Run `python template.py` first

### After Effects doesn't start
**Solutions:**
1. Check `.env` has correct `AFTER_EFFECT_FOLDER`
2. Install startup script: `python install_ae_runner.py`
3. Restart After Effects

### "Composition not found"
**Solution:** Template creation may have failed. Delete the .aep file and run `template.py` again.

### Scripts don't execute in After Effects
**Solutions:**
1. Make sure startup script is installed
2. Check **Window > Info** panel in AE for "AE Command Runner" messages
3. Verify scripting is enabled: Edit > Preferences > Scripting & Expressions

### Render fails
**Solutions:**
1. Make sure composition name is correct
2. Check output directory exists and is writable
3. Verify `aerender.exe` path in `.env`

---

## 📝 Creating Your Own Example

Want to create a custom example? Here's the template:

```bash
# Create folder
mkdir examples/my_example

# Create files
touch examples/my_example/template.py
touch examples/my_example/run.py
touch examples/my_example/README.md
```

### template.py structure:
```python
from ae_automation import Client

def create_template():
    client = Client()
    template_config = { ... }
    client.buildTemplate(template_config, "my_template.aep")

if __name__ == "__main__":
    create_template()
```

### run.py structure:
```python
from ae_automation import Client

def run_automation():
    client = Client()
    config = { ... }
    client.startBot(config)

if __name__ == "__main__":
    run_automation()
```

---

## 🔗 Related Documentation

- [Main README](../README.md) - Package overview
- [Export Guide](../EXPORT_GUIDE.md) - Template export workflow
- [CLI Guide](../CLI_GUIDE.md) - Command-line usage
- [Installation](../install_ae_runner.py) - Startup script setup

---

## 🤝 Contributing

Have a useful example? We'd love to include it!

1. Create a new folder: `examples/your_example/`
2. Include `template.py`, `run.py`, and `README.md`
3. Follow the existing structure
4. Test with After Effects 2024/2025
5. Submit a pull request

---

## 📄 License

Examples are part of the After Effects Automation package - MIT License
