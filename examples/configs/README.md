# Example Configurations for After Effects Automation

This directory contains ready-to-use JSON configuration files that can be edited using the web-based editor.

## Quick Start

Load any example in the web editor:

```bash
ae-editor examples/configs/01_tutorial_video.json
ae-editor examples/configs/02_social_media_post.json --host 0.0.0.0 --port 8080
```

Or use the Python command:

```bash
python app.py examples/configs/03_product_showcase.json
```

## Available Examples

### 1. Tutorial Video (`01_tutorial_video.json`)
**Duration:** 30 seconds
**Format:** 1920x1080 @ 29.97fps
**Use Case:** Educational content, how-to videos, tutorials

**Features:**
- Simple 3-scene structure (intro, content, outro)
- Text overlays for tutorial steps
- Background music integration
- Logo placement

**Perfect for:**
- YouTube tutorials
- Online courses
- Training videos
- Instructional content

---

### 2. Social Media Post (`02_social_media_post.json`)
**Duration:** 15 seconds
**Format:** 1080x1920 @ 30fps (Vertical/Stories)
**Use Case:** Instagram Stories, TikTok, Reels

**Features:**
- Vertical format optimized for mobile
- Fast-paced 3-second hook
- Template system for consistent branding
- Trending audio integration
- Call-to-action end screen

**Perfect for:**
- Instagram Stories
- TikTok videos
- Facebook Reels
- Snapchat content

---

### 3. Product Showcase (`03_product_showcase.json`)
**Duration:** 45 seconds
**Format:** 1920x1080 @ 29.97fps
**Use Case:** E-commerce, product launches, promotional videos

**Features:**
- Multiple product highlights with template system
- Professional corporate music
- Voiceover synchronization
- Timeline markers for precise timing
- Price and feature displays
- Brand logo integration

**Perfect for:**
- E-commerce product videos
- Amazon listings
- Product launches
- Sales presentations
- Marketing campaigns

---

### 4. Photo Slideshow (`04_photo_slideshow.json`)
**Duration:** 60 seconds
**Format:** 1920x1080 @ 29.97fps
**Use Case:** Memories, events, portfolios

**Features:**
- 6 photo slides with captions
- Emotional music soundtrack
- Template-based photo placement
- Title and end cards
- Automatic timing

**Perfect for:**
- Wedding slideshows
- Birthday celebrations
- Year-in-review videos
- Portfolio presentations
- Memorial tributes

---

### 5. Event Promo (`05_event_promo.json`)
**Duration:** 25 seconds
**Format:** 1920x1080 @ 30fps
**Use Case:** Event promotion, conferences, meetups

**Features:**
- Event information cards (When, Where, Who)
- Energetic music
- Multiple media types (images, video)
- Registration call-to-action
- Timeline markers for key moments
- Professional layout

**Perfect for:**
- Conference promotions
- Webinar announcements
- Meetup invitations
- Festival marketing
- Event countdowns

---

## How to Use These Examples

### Method 1: Web Editor (Recommended)

1. **Start the editor:**
   ```bash
   ae-editor examples/configs/01_tutorial_video.json
   ```

2. **Edit in browser:**
   - Opens automatically at http://127.0.0.1:5000
   - Modify text, timing, resources
   - Save changes directly to the file

3. **Run the automation:**
   ```bash
   ae-automate examples/configs/01_tutorial_video.json
   ```

### Method 2: Direct Editing

1. **Copy example to your project:**
   ```bash
   cp examples/configs/01_tutorial_video.json my_project.json
   ```

2. **Edit the JSON file:**
   - Update file paths to your assets
   - Modify text content
   - Adjust timing and durations
   - Change composition names to match your AE project

3. **Run the automation:**
   ```bash
   ae-automate my_project.json
   ```

### Method 3: Command Line

```bash
# View with default settings
ae-editor examples/configs/02_social_media_post.json

# Custom host and port
ae-editor examples/configs/03_product_showcase.json --host 0.0.0.0 --port 8080

# Using Python directly
python app.py examples/configs/04_photo_slideshow.json --port 3000
```

## Customization Guide

### 1. Update File Paths

Replace placeholder paths with your actual files:

```json
"project_file": "C:/AE_Projects/tutorial_template.aep",  // Your AE project
"resources": [
  {
    "path": "C:/AE_Projects/assets/music.mp3"  // Your audio file
  }
]
```

### 2. Modify Text Content

Update any text in the custom_actions:

```json
{
  "change_type": "update_layer_property",
  "value": "Your Custom Text Here"
}
```

### 3. Adjust Timing

Change scene durations and start times:

```json
{
  "name": "intro",
  "duration": 5,      // Length in seconds
  "startTime": 0      // When to start
}
```

### 4. Add/Remove Resources

Add new media to the resources array:

```json
{
  "type": "image",
  "name": "new_image",
  "path": "C:/path/to/image.jpg"
}
```

### 5. Customize Templates

Modify template values:

```json
{
  "change_type": "template",
  "template_name": "productCard",
  "template_values": {
    "title": "Your Product",
    "price": "$99.99"
  }
}
```

## Configuration Options Reference

### Project Settings

- `project_file` - Path to your AE project template
- `comp_name` - Main composition name
- `comp_width` / `comp_height` - Resolution (1920x1080, 1080x1920, etc.)
- `comp_fps` - Frame rate (29.97, 30, 24, 60)
- `comp_end_time` - Total duration in seconds
- `output_dir` - Where to save rendered video
- `debug` - true = preview mode, false = production
- `renderComp` - true = auto-render, false = setup only

### Resource Types

- `audio` - MP3, WAV audio files (requires duration)
- `image` - PNG, JPG, JPEG images
- `video` - MP4, MOV video files (requires duration)

### Custom Actions

- `update_layer_property` - Change text, position, scale, etc.
- `add_resource` - Add media to timeline
- `swap_items_by_index` - Replace placeholder with resource
- `add_marker` - Add sync markers
- `template` - Use predefined template

## Tips for Best Results

1. **Start with an example close to your use case**
2. **Update all file paths before running**
3. **Verify template composition names match your AE project**
4. **Test with debug=true before rendering**
5. **Use the web editor for visual editing**
6. **Check timeline duration matches comp_end_time**
7. **Use markers for audio/voiceover sync**

## Troubleshooting

**"Composition not found"**
- Ensure template_comp names exist in your AE project

**"Resource file not found"**
- Check all file paths in the resources array

**"Layer not found"**
- Verify layer names match your template compositions

**Web editor won't start**
- Check if port is already in use
- Try a different port: `--port 8080`

## Next Steps

After editing your configuration:

1. **Preview in After Effects:**
   ```bash
   ae-automate your_config.json
   ```

2. **Enable rendering:**
   Set `"renderComp": true` in the JSON

3. **Production mode:**
   Set `"debug": false` for unattended rendering

## Contributing

Have a useful example configuration? Submit a pull request!

## License

These example configurations are part of the After Effects Automation package and are licensed under the MIT License.
