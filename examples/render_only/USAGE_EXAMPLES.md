# Render Only - Usage Examples

Quick reference for common rendering workflows.

## Basic Usage

### 1. Interactive Mode (Recommended for Beginners)

```bash
python render.py
```

Follow the prompts to:
- Enter a .aep file path
- Use the basic template (auto-generated)
- Specify composition name

### 2. Direct File Rendering

```bash
python render.py "C:\Path\To\Your\Project.aep"
```

Renders using default composition name (FinalComposition).

### 3. Specify Composition

```bash
python render.py myproject.aep --comp "MainSequence"
```

Renders a specific composition by name.

### 4. Custom Output Directory

```bash
python render.py myproject.aep --output "C:\Videos\Renders"
```

Saves the rendered video to a custom location.

## Real-World Examples

### Example 1: Batch Render Multiple Compositions

```bash
# Render intro
python render.py project.aep --comp "Intro" --output "./renders"

# Render main content
python render.py project.aep --comp "MainContent" --output "./renders"

# Render outro
python render.py project.aep --comp "Outro" --output "./renders"
```

### Example 2: Render from Automation Output

After running the basic_composition automation:

```bash
python render.py "../basic_composition/output/ae_automation.aep" --comp "FinalComposition"
```

### Example 3: Quick Template Test

```bash
# Uses basic template automatically
python render.py --comp "IntroTemplate"
```

### Example 4: Production Workflow

```bash
# Step 1: Use absolute path to avoid confusion
$PROJECT = "C:\Projects\MyVideo\final_edit.aep"

# Step 2: Render with specific settings
python render.py $PROJECT --comp "Export_4K" --output "C:\Renders\Client_Review"
```

## Command Line Options

### All Options Combined

```bash
python render.py "path/to/file.aep" --comp "MyComposition" --output "C:\Renders"
```

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `project_file` | - | Path to .aep | `myproject.aep` |
| `--comp` | `-c` | Composition name | `--comp "Intro"` |
| `--output` | `-o` | Output directory | `--output "./renders"` |

## Environment Setup

### For Windows Users

Set UTF-8 encoding (recommended):

```cmd
set PYTHONIOENCODING=utf-8
python render.py
```

Or use PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"
python render.py
```

### For Batch Scripts

Create a `batch_render.bat`:

```batch
@echo off
set PYTHONIOENCODING=utf-8

echo Rendering intro...
python render.py project.aep --comp "Intro"

echo Rendering main...
python render.py project.aep --comp "Main"

echo Done!
pause
```

## Output Files

Rendered videos are saved as:
```
{output_directory}/{composition_name}.mp4
```

Default: `{project_directory}/output/{composition_name}.mp4`

## Tips & Tricks

### 1. Check Available Compositions

Open the .aep file in After Effects to see composition names.

Composition names are **case-sensitive**:
- "MainComp" ≠ "maincomp"
- "Intro_01" ≠ "intro_01"

### 2. Relative vs Absolute Paths

**Relative paths** (from current directory):
```bash
python render.py ./projects/myfile.aep
```

**Absolute paths** (full path):
```bash
python render.py "C:\Projects\Video\myfile.aep"
```

Absolute paths are recommended to avoid confusion.

### 3. Use Quotes for Paths with Spaces

```bash
# GOOD
python render.py "C:\My Projects\Video Project\file.aep"

# BAD (will fail)
python render.py C:\My Projects\Video Project\file.aep
```

### 4. Test Render First

Render a short composition first to verify settings:

```bash
python render.py project.aep --comp "Test_5sec"
```

Then render the full project once confirmed.

### 5. Check Render Queue Settings

The script uses After Effects' default render settings.

To customize:
1. Open the .aep in After Effects
2. Set up Render Queue manually
3. Save the project
4. Use this script to batch render

## Troubleshooting

### "No comp was found with the given name"

**Solution 1:** Check composition name (case-sensitive)
```bash
# Open in AE and verify the exact name
```

**Solution 2:** Specify a different comp
```bash
python render.py project.aep --comp "ActualCompName"
```

### Empty/Black Video Output

This happens when:
- Composition is empty
- Layers are disabled
- Template hasn't been processed by automation

**Solution:** Use the automation workflow first, then render.

### "aerender not found"

**Check settings:**
```python
# In ae_automation/settings.py
AERENDER_PATH = "C:\\Program Files\\Adobe\\Adobe After Effects 2025\\Support Files\\aerender.exe"
```

### Video File is 0 KB

Render failed silently. Check:
1. Composition exists
2. After Effects is installed correctly
3. Output directory is writable
4. No licensing issues with AE

## Performance Notes

**Render Speed Factors:**
- Composition complexity
- Effects/plugins used
- Output resolution (1080p vs 4K)
- Computer hardware (GPU, RAM)
- Disk speed (SSD vs HDD)

**Example Render Times:**
- Simple text comp (5s @ 1080p): ~2-3 seconds
- Complex effects (10s @ 1080p): ~10-30 seconds
- Full production (60s @ 4K): ~2-5 minutes

Your mileage may vary based on hardware and composition complexity.
