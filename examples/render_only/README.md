# Render Only Example

Simple example for rendering After Effects project files without automation.

## Use Case

Use this when you:
- Already have a .aep file ready
- Just want to render the video output
- Don't need to modify layers or properties
- Want a quick way to batch render compositions

## Important: Understanding .aep Files

There are different types of .aep files in this project:

### 1. basic_template.aep (Template File)
- Contains: `IntroTemplate`, `OutroTemplate`
- Does NOT contain: `FinalComposition`
- Use this for rendering individual template compositions

### 2. ae_automation.aep (Automation Output)
- Contains: `FinalComposition` (with all scenes assembled)
- Also contains: Duplicate scene compositions
- Created by running `basic_composition/run.py`
- Use this for rendering the complete video

### Quick Reference

| File | Available Compositions | How to Render |
|------|----------------------|---------------|
| basic_template.aep | IntroTemplate, OutroTemplate | `python render.py --comp "IntroTemplate"` |
| ae_automation.aep | FinalComposition | `python render.py --comp "FinalComposition"` |
| Your custom .aep | Check in After Effects | `python render.py yourfile.aep --comp "YourComp"` |

## Usage

### Interactive Mode

Run without arguments to get an interactive prompt:

```bash
python render.py
```

You'll be asked to:
1. Provide a path to your .aep file, OR
2. Use the basic composition template (auto-generated if needed)

### Direct Mode

Provide the .aep file path directly:

```bash
python render.py path/to/your/project.aep
```

### Specify Composition

Render a specific composition by name:

```bash
python render.py myproject.aep --comp "IntroSequence"
```

### Custom Output Directory

Save the rendered video to a specific directory:

```bash
python render.py myproject.aep --output "C:\Videos\Output"
```

## Examples

### Example 1: Render existing project
```bash
python render.py "C:\Projects\MyVideo.aep"
```

### Example 2: Render with custom composition name
```bash
python render.py myproject.aep --comp "MainComposition"
```

### Example 3: Use basic template (auto-generates if needed)
```bash
python render.py
# Select option 2 when prompted
```

### Example 4: Render specific comp from basic template
```bash
python render.py --comp "FinalComposition"
# Will use basic template automatically
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `project_file` | - | Path to .aep file | Interactive prompt |
| `--comp` | `-c` | Composition name | FinalComposition or prompt |
| `--output` | `-o` | Output directory | `{project_dir}/output` |

## How It Works

1. **Find Project File**
   - Uses provided path, OR
   - Prompts user interactively, OR
   - Falls back to basic_composition template, OR
   - Generates basic template if missing

2. **Configure Render**
   - Determines composition name
   - Sets output directory
   - Prepares aerender command

3. **Render**
   - Executes Adobe aerender CLI
   - Streams progress to console
   - Reports completion status

## Output

The rendered video will be saved as:
```
{output_directory}/{composition_name}.mp4
```

**Default output directory:** `./output` (current working directory)

For example:
- If you run from `examples/render_only/`: Output goes to `examples/render_only/output/`
- If you run from `examples/basic_composition/`: Output goes to `examples/basic_composition/output/`

**Custom output directory:**
```bash
python render.py myfile.aep --output "C:\MyRenders"
```

## Requirements

- After Effects installed with aerender CLI
- Valid .aep project file
- Composition exists in the project

## Troubleshooting

### "Composition not found"
Make sure the composition name matches exactly (case-sensitive).
You can check composition names by opening the .aep file in After Effects.

### "aerender not found"
Check that `AERENDER_PATH` is correctly set in `ae_automation/settings.py`.

### "File not found"
Ensure the .aep file path is correct and accessible.
Use absolute paths to avoid confusion.

## Notes

- This example does NOT modify the .aep file
- It only renders existing compositions
- For automation (modifying layers, properties, etc.), use the `basic_composition` example instead
- aerender runs in a separate After Effects instance
