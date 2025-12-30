# After Effects Automation - Examples

Quick, practical examples showing what you can build with After Effects automation.

## 🚀 Quick Start

```bash
# 1. Pick an example
cd examples/basic_composition

# 2. Run it (auto-creates template if needed)
python run.py
```

**That's it!** The script will:
- Create the After Effects template automatically
- Open After Effects
- Build your composition
- Render the final video

Perfect for creating GIF demos! 🎬

---

## 📊 Examples at a Glance

| Example | What It Does | Time | Command |
|---------|-------------|------|---------|
| **basic_composition** | Creates intro + outro scenes | ~2 min | `python run.py` |
| **text_animation** | Multi-layer text with styles | ~2 min | `python run.py` |
| **render_only** | Renders .aep files (no automation) | ~10 sec | `python render.py` |

---

## 📚 Detailed Examples

### 1. Basic Composition
**📁** `examples/basic_composition/` | **⭐ Beginner** | **⏱️ 2 minutes**

**What You'll Learn:**
- Automated template creation
- Timeline setup with scenes
- Text property updates
- Full automation workflow

**Quick Start:**
```bash
cd examples/basic_composition
python run.py
```

**Output:** 10-second video with intro and outro scenes

**What Happens:**
1. Checks for template, creates if missing
2. Opens After Effects
3. Creates FinalComposition with 2 scenes
4. Updates text in each scene
5. Renders to `output/FinalComposition.mp4`

[📖 Full Guide →](basic_composition/README.md)

---

### 2. Text Animation
**📁** `examples/text_animation/` | **⭐ Beginner** | **⏱️ 2 minutes**

**What You'll Learn:**
- Multiple text layers
- Different text styles
- Multi-line text with line breaks
- Dynamic content from Python

**Quick Start:**
```bash
cd examples/text_animation
python run.py
```

**Perfect For:** Tutorial videos, social media posts

**Output:** Video with multiple styled text layers

[📖 Full Guide →](text_animation/README.md)

---

### 3. Render Only
**📁** `examples/render_only/` | **⭐ Beginner** | **⏱️ 10 seconds**

**What You'll Learn:**
- Rendering .aep files without automation
- Interactive vs command-line modes
- Smart composition defaults
- Batch rendering workflows

**Quick Start:**
```bash
cd examples/render_only

# Interactive mode (prompts for file)
python render.py

# Direct mode (renders immediately)
python render.py path/to/file.aep

# Specify composition
python render.py file.aep --comp "MyComp"
```

**Perfect For:** Quick renders when you already have .aep files

**Key Features:**
- Auto-detects composition type (template vs automation output)
- Outputs to current directory by default
- Smart defaults: `ae_automation.aep` → FinalComposition, `basic_template.aep` → IntroTemplate

[📖 Full Guide →](render_only/README.md)

---

## 🎓 Learning Path

### Beginner (Start Here)
1. **basic_composition** - Learn the automation workflow
2. **text_animation** - Master text manipulation
3. **render_only** - Understand rendering workflows

### Next Steps
- Modify the examples to fit your needs
- Combine techniques from multiple examples
- Build your own automation scripts

---

## 🛠️ How Examples Work

### Automation Examples (basic_composition, text_animation)

**Folder Structure:**
```
example_name/
├── run.py                   # Main script (auto-creates template & runs automation)
├── template.py              # Template builder (auto-called by run.py if needed)
├── README.md                # Documentation
└── output/                  # Generated files (git-ignored)
    ├── basic_template.aep   # Auto-created template
    ├── ae_automation.aep    # Automation working file
    └── FinalComposition.mp4 # Rendered video
```

**Workflow (Fully Automatic):**
1. Run `python run.py`
2. Script auto-creates template if missing
3. Opens After Effects and loads template
4. Builds compositions and updates properties
5. Renders final video to `output/`

**No manual steps - just run and go!**

---

### Render-Only Example

**Folder Structure:**
```
render_only/
├── render.py                # Rendering script
├── README.md                # Documentation
└── output/                  # Rendered videos (git-ignored)
    └── *.mp4                # Output files
```

**Workflow:**
1. Run `python render.py`
2. Select .aep file (or provide path)
3. Choose composition (or use smart default)
4. Video renders to `output/`

**Use when:** You have existing .aep files and just need video output

---

## ⚙️ Configuration

Examples use Python dictionaries for configuration:

### Project Settings
```python
"project": {
    "project_file": "./template.aep",    # Template to use
    "comp_name": "FinalComposition",     # Output composition
    "comp_fps": 29.97,                   # Frame rate
    "comp_width": 1920,                  # Width
    "comp_height": 1080,                 # Height
    "comp_end_time": 10,                 # Duration (seconds)
    "renderComp": True,                  # Render video?
    "output_dir": "."                    # Output directory
}
```

### Timeline Scene
```python
{
    "name": "intro",                     # Scene name
    "duration": 5,                       # Duration
    "startTime": 0,                      # Start time
    "template_comp": "IntroTemplate",    # Source composition
    "custom_actions": [...]              # What to do
}
```

### Update Text
```python
{
    "change_type": "update_layer_property",
    "comp_name": "IntroTemplate",
    "layer_name": "MainTitle",
    "property_name": "Text.Source Text",
    "value": "My Amazing Video"
}
```

---

## 🚀 Common Customizations

### Change Video Duration
In `run.py`, modify:
```python
"comp_end_time": 20  # 20 seconds instead of 10
```

### Disable Rendering
To build compositions without rendering:
```python
"renderComp": False
```

Then use `render_only` to render later.

### Update Text Content
In the timeline config:
```python
{
    "change_type": "update_layer_property",
    "layer_name": "MainTitle",
    "value": "Your Custom Text Here"
}
```

### Change Output Location
```python
"output_dir": "C:/MyVideos"  # Custom directory
```

---

## 🔧 Prerequisites

1. **After Effects** (2024, 2025, or 2025 Beta)
2. **Python 3.7+**
3. **Package installed:**
   ```bash
   pip install after-effects-automation
   ```
4. **Startup script installed:**
   ```bash
   python install_ae_runner.py
   ```
5. **Environment configured:**
   ```bash
   cp .env.example .env
   # Edit .env with your AE path
   ```

**📖 Full Setup:** See [Installation Guide](../INSTALLATION.md)

---

## ❓ Troubleshooting

### "Template not found" then auto-creates it
**This is normal!** First run creates the template automatically.

### After Effects doesn't start
1. Check `.env` has correct `AFTER_EFFECT_FOLDER`
2. Verify AE version matches path (2024 vs 2025)
3. Install startup script: `python install_ae_runner.py`

### "Composition not found"
- For `basic_template.aep` → Use `IntroTemplate` or `OutroTemplate`
- For `ae_automation.aep` → Use `FinalComposition`
- Composition names are case-sensitive

### Scripts don't execute
1. Enable scripting in AE: Edit > Preferences > Scripting & Expressions
2. Check "Allow Scripts to Write Files and Access Network"
3. Restart After Effects
4. Verify startup script: Look for "AE Command Runner" in Window > Info

### Empty/black video
Update to latest version (bug was fixed in v0.0.4):
```bash
pip install --upgrade after-effects-automation
```

**📖 More Help:** See [Troubleshooting Guide](../TROUBLESHOOTING.md)

---

## 📝 Creating Your Own Example

### Basic Structure

```bash
# Create folder
mkdir examples/my_example
cd examples/my_example

# Create main script
touch run.py
touch template.py  # Optional: if you need custom templates
touch README.md
```

### Simple run.py Template

```python
#!/usr/bin/env python3
import os
from ae_automation import Client

# Initialize
client = Client()

# Configuration
config = {
    "project": {
        "project_file": "./my_template.aep",
        "comp_name": "FinalComposition",
        "comp_fps": 29.97,
        "comp_width": 1920,
        "comp_height": 1080,
        "comp_end_time": 10,
        "renderComp": True,
        "output_dir": ".",
        "debug": False,
        "resources": []
    },
    "timeline": [
        {
            "name": "scene1",
            "duration": 10,
            "startTime": 0,
            "template_comp": "MyTemplate",
            "custom_actions": []
        }
    ]
}

# Run
if __name__ == "__main__":
    # Save config
    import json
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Run automation
    client.startBot("config.json")
```

### Tips

- Start by copying an existing example
- Modify gradually to understand what each part does
- Use `"debug": True` to keep AE open for inspection
- Test with short durations first
- Read the generated `ae_automation.aep` file to understand structure

---

## 🔗 Related Documentation

- [Main README](../README.md) - Package overview
- [Installation Guide](../INSTALLATION.md) - Setup instructions
- [CLI Guide](../CLI_GUIDE.md) - Command-line usage
- [Troubleshooting](../TROUBLESHOOTING.md) - Problem solving
- [Process Management](../PROCESS_MANAGEMENT.md) - How it works

---

## 🤝 Contributing Examples

Have a useful example? Share it!

**What makes a good example:**
- Solves a real problem
- Well documented
- Single, clear purpose
- Works with latest version
- Includes output samples/screenshots

**How to contribute:**
1. Create example folder in `examples/`
2. Add `run.py`, `README.md`, and any other files
3. Test with AE 2024/2025
4. Include clear documentation
5. Submit pull request

---

## 📄 License

Examples are part of the After Effects Automation package - MIT License
