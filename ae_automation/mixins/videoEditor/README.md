# Video Editor UI

A modern, React-based video editor interface built with Vite and SCSS modules.

## Features

- **Undo/Redo System** - Full history management with Ctrl+Z/Ctrl+Y keyboard shortcuts
- **Advanced Timeline** - Multi-track timeline with drag-and-drop, resizing, and snap-to-grid
- **Effects & Transitions** - Built-in effects and transitions library
- **Project Settings** - Complete control over all project details
- **MP4 Rendering** - One-click rendering with custom output paths
- **Modern UI** - Clean, professional dark theme with smooth animations

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Zustand** - Lightweight state management with Immer
- **SCSS Modules** - Component-scoped styling
- **Framer Motion** - Smooth animations
- **React Icons** - Icon library
- **Axios** - HTTP client

## Installation

1. Navigate to the videoEditor directory:
   ```bash
   cd ae_automation/mixins/videoEditor
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

### Development Mode

Run the React development server:
```bash
npm run dev
```

This will start Vite dev server on `http://localhost:5173` with hot module replacement.

To run the backend in development mode:
```python
from ae_automation import AfterEffectsAutomation

ae = AfterEffectsAutomation()
ae.runVideoEditor('path/to/project.json', dev_mode=True)
```

### Production Build

Build the production-ready assets:
```bash
npm run build
```

This creates optimized files in the `dist/` directory that will be served by the Flask backend.

To run in production mode:
```python
from ae_automation import AfterEffectsAutomation

ae = AfterEffectsAutomation()
ae.runVideoEditor('path/to/project.json')
```

## Usage

### Basic Usage

```python
from ae_automation import AfterEffectsAutomation

# Create an instance
ae = AfterEffectsAutomation()

# Start the video editor
ae.runVideoEditor('path/to/your/project.json')
```

The editor will open in your default browser at `http://localhost:5000`.

### Keyboard Shortcuts

- **Ctrl+Z** - Undo
- **Ctrl+Y** or **Ctrl+Shift+Z** - Redo
- **Delete** - Delete selected scene

### Timeline Controls

- **Click** - Select scene
- **Double-click** - Edit scene details
- **Drag** - Move scene on timeline
- **Drag handles** - Resize scene duration
- **Zoom slider** - Adjust timeline zoom level

### Adding Scenes

1. Click "Add Scene" button in the toolbar
2. Double-click the new scene to edit details
3. Configure name, duration, template, and effects

### Adding Effects

1. Select a scene on the timeline
2. Browse effects in the right panel
3. Click the + button to add effect to scene

### Rendering

1. Click "Render MP4" button in the header
2. Enter output path
3. Click "Start Render"

## Project Structure

```
videoEditor/
├── src/
│   ├── components/
│   │   ├── Header/
│   │   ├── Toolbar/
│   │   ├── ProjectPanel/
│   │   ├── Timeline/
│   │   └── EffectsPanel/
│   ├── store/
│   │   └── useEditorStore.js
│   ├── styles/
│   │   ├── variables.scss
│   │   └── global.scss
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## API Endpoints

The Flask backend provides these REST API endpoints:

- `GET /api/project` - Get current project data
- `POST /api/project` - Update project data
- `POST /api/undo` - Undo last change
- `POST /api/redo` - Redo last undone change
- `GET /api/effects` - Get available effects and transitions
- `POST /api/render` - Trigger project rendering

## Customization

### Styling

Edit SCSS variables in `src/styles/variables.scss` to customize colors, spacing, etc.

### Effects

Add new effects in the backend's `/api/effects` endpoint in `VideoEditorApp.py`.

### Components

All components use CSS Modules for scoped styling. Component files follow the pattern:
- `ComponentName.jsx` - React component
- `ComponentName.module.scss` - Component styles

## Building for Production

```bash
# Install dependencies
npm install

# Build
npm run build

# The dist/ folder will contain the production build
```

## Troubleshooting

### Port already in use

If port 5000 is already in use, specify a different port:
```python
ae.runVideoEditor('project.json', port=5001)
```

### CORS errors in development

Make sure you're running both the React dev server (port 5173) and Flask backend (port 5000) with `dev_mode=True`.

### Missing flask-cors

Install the required Python package:
```bash
pip install flask-cors
```

## License

Part of the After Effects Automation project.
