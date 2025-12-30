# Building the Video Editor

## Quick Start

### 1. Install Node.js Dependencies

Navigate to the videoEditor directory and install dependencies:

```bash
cd ae_automation/mixins/videoEditor
npm install
```

### 2. Build for Production

Build the optimized production bundle:

```bash
npm run build
```

This will create a `dist/` folder with all the compiled assets.

### 3. Install Python Dependencies

Make sure flask-cors is installed:

```bash
pip install flask-cors
```

Or reinstall the package:

```bash
pip install -e .
```

## Development Workflow

### Option 1: Development Mode (Recommended for development)

**Terminal 1** - Start React dev server:
```bash
cd ae_automation/mixins/videoEditor
npm run dev
```

**Terminal 2** - Start Flask backend with dev mode:
```python
from ae_automation import AfterEffectsAutomation

ae = AfterEffectsAutomation()
ae.runVideoEditor('path/to/project.json', dev_mode=True)
```

This enables hot module replacement - changes to React code will update instantly without refreshing.

### Option 2: Production Mode

Build the React app first:
```bash
cd ae_automation/mixins/videoEditor
npm run build
```

Then run the Flask server:
```python
from ae_automation import AfterEffectsAutomation

ae = AfterEffectsAutomation()
ae.runVideoEditor('path/to/project.json')
```

## Troubleshooting

### "Cannot find module" errors
Run `npm install` again to ensure all dependencies are installed.

### CORS errors
Make sure `flask-cors` is installed: `pip install flask-cors`

### Build fails
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Run `npm run build`

### Port conflicts
Change the port in Python:
```python
ae.runVideoEditor('project.json', port=5001)
```

Or in Vite config for React dev server (edit `vite.config.js`):
```js
server: {
  port: 5174  // Change from 5173
}
```

## Project Structure After Build

```
videoEditor/
├── dist/               # Built production files (created by npm run build)
│   ├── index.html
│   ├── assets/
│   │   ├── *.js       # JavaScript bundles
│   │   └── *.css      # Compiled CSS
│   └── ...
├── src/                # Source files
├── node_modules/       # Dependencies (created by npm install)
├── package.json        # NPM configuration
├── vite.config.js      # Vite configuration
└── README.md          # Documentation
```

## Updating After Changes

### After React Code Changes
```bash
npm run build
```

### After Python Code Changes
```bash
pip install -e .
```

### After Dependencies Change
```bash
npm install
pip install -e .
```
