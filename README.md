<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**Automate After Effects from Python. Talk to it with AI.**

JSON config in, video out. No manual AE interaction required.

English | [Español](docs/README.es.md) | [中文版](docs/README.zh-CN.md) | [Português](docs/README.pt.md)

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![Downloads](https://img.shields.io/pepy/dt/after-effects-automation?style=flat-square&color=green)](https://pepy.tech/project/after-effects-automation)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

<br>

[Quick Start](#-quick-start) · [AI Chat](#-ai-chat-panel) · [Features](#-features) · [CLI](#-cli) · [Architecture](#-architecture) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

---

## 🚀 Quick Start

```bash
pip install after-effects-automation
python install_ae_runner.py
ae-automation run config.json
```

**No config needed.** Auto-detects every AE version on your machine and picks the latest. Works from 2020 to 2026+ — no hardcoded paths, no `.env` required.

```python
from ae_automation import Client
Client().startBot("config.json")
```

---

## 🤖 AI Chat Panel

Control After Effects with natural language — right inside AE. Powered by [Prompture](https://github.com/jhd3197/prompture).

```bash
python install_extension.py        # install the AE panel
ae-automation chat                  # start backend
# In AE: Window > Extensions > AE Automation Chat
```

| You say | AE does |
|---------|---------|
| *"Create a 1080p comp called Intro, 10 seconds"* | Creates the composition |
| *"Change the title text to Product Launch 2025"* | Updates the text layer |
| *"Set the background color to #1A1A2E"* | Applies the color |
| *"List all compositions"* | Returns project structure |

Returns clickable **action buttons** that execute directly in AE. Works with any LLM — OpenAI, Claude, Ollama, Groq, and more.

---

## 🎯 Features

### Automation

**JSON-Driven** — Describe your video in a config, the platform handles everything else

**10 Action Types** — Update properties, swap layers, add resources, nest comps, apply templates, transitions, markers

**Batch Rendering** — Generate hundreds of video variations from data

**Built-in Templates** — Tutorial, social media, product showcase, slideshow, event promo

### Smart Detection

**Auto-Discovery** — Scans your system for every AE version, always picks the latest. No hardcoded years

**Version Compatibility** — Knowledge base tracks which scripts work on which AE versions. Scripts that would freeze are blocked before execution with workaround suggestions

**Cross-Platform** — Windows supported, macOS in progress. Paths, data dirs, and CEP install all adapt to your OS

### AI & Tools

**Chat Panel** — CEP extension with [Prompture](https://github.com/jhd3197/prompture) backend (any LLM provider)

**Web Editor** — Browser-based visual config editor with undo/redo

**40+ ExtendScript Files** — Direct AE manipulation via file-based command queue

---

## 🖥️ CLI

| Command | Description |
|---------|-------------|
| `ae-automation run config.json` | Run the full automation pipeline |
| `ae-automation chat` | Start the AI chat panel backend |
| `ae-automation batch *.json` | Run multiple configs sequentially |
| `ae-automation editor config.json` | Launch the visual web editor |
| `ae-automation generate --template tutorial` | Generate .aep from built-in template |
| `ae-automation export --template social-media` | Generate + render in one step |
| `ae-automation plugins list` | List, install, search, run community plugins |
| `ae-automation test` | Run compatibility tests |
| `ae-automation diagnose` | Check AE installation and scripting setup |

---

## 🏗️ Architecture

```
Python Config (JSON) → JS Bridge → ExtendScript in AE → Composition → aerender → MP4
```

The `Client` class composes seven mixins:

| Mixin | Responsibility |
|-------|---------------|
| `afterEffectMixin` | Core: launching AE, scripting, compositions, rendering |
| `botMixin` | JSON config loading and pipeline orchestration |
| `ChatPanelMixin` | AI chat backend with Prompture |
| `ProcessManagerMixin` | AE process detection, readiness, crash handling |
| `TemplateGeneratorMixin` | Programmatic .aep project creation |
| `VideoEditorAppMixin` | Flask web editor with REST API |
| `ToolsMixin` | Utilities (hex to RGBA, slug, file ops) |

| Layer | Technology |
|-------|------------|
| Backend | Python 3.7+, Flask, Flask-CORS |
| AI | Prompture (any LLM provider) |
| AE Bridge | ExtendScript (JSX), file-based command queue |
| Web Editor | React 18, Vite, Zustand |
| CEP Panel | HTML/CSS/JS, CSInterface |
| Rendering | aerender (Adobe CLI) |

<details>
<summary><strong>Compatibility</strong></summary>

| Software | Versions |
|----------|----------|
| **After Effects** | 2020 – 2026+ (auto-detected) |
| **Python** | 3.7+ |
| **OS** | Windows, macOS |

```python
from ae_automation.settings import get_discovery_report
print(get_discovery_report())  # see all detected AE installs

from ae_automation.compat import get_incompatible_scripts
print(get_incompatible_scripts(2020))  # check what won't work
```

</details>

<details>
<summary><strong>Documentation</strong></summary>

| Guide | Description |
|-------|-------------|
| [Installation](INSTALLATION.md) | Full setup: Python, CLI, AE bridge, environment |
| [Quick Start](QUICK_START.md) | End-to-end walkthrough |
| [CLI Guide](CLI_GUIDE.md) | Command reference |
| [Examples](examples/README.md) | Working automation examples |
| [Process Management](PROCESS_MANAGEMENT.md) | AE process lifecycle |
| [Troubleshooting](TROUBLESHOOTING.md) | Common issues and fixes |

</details>

<details>
<summary><strong>Troubleshooting</strong></summary>

**AE not detected?** Run `ae-automation diagnose` or set `AFTER_EFFECT_FOLDER` in `.env`

**Scripts not executing?** Enable scripting in AE: `Edit > Preferences > Scripting & Expressions`

**Chat panel not connecting?** Start the backend: `ae-automation chat`

</details>

---

## 🗺️ Roadmap

- [x] Core automation — Python to ExtendScript to AE to render
- [x] JSON config pipeline — templates, custom actions, resources
- [x] CLI — run, chat, editor, generate, export, test, diagnose
- [x] AI chat panel — CEP extension with Prompture backend
- [x] Auto-discovery — version detection and compatibility layer
- [x] Web editor — visual config editing
- [x] Built-in templates — 5 ready-to-use templates
- [x] macOS support — cross-platform abstraction layer
- [x] Real-time render progress — live progress bar in chat panel
- [x] Batch queue — sequential multi-video processing with status tracking
- [x] Plugin marketplace — community templates and actions with install/search/run

---

## 🤝 Contributing

```
fork → feature branch → commit → push → pull request
```

**Priority areas:** macOS support, new templates, batch rendering, chat panel improvements.

[Report Bug](https://github.com/jhd3197/after-effects-automation/issues) · [Request Feature](https://github.com/jhd3197/after-effects-automation/issues)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jhd3197/after-effects-automation&type=Date)](https://star-history.com/#jhd3197/after-effects-automation&Date)

> [!TIP]
> Also check out [RepoGif](https://github.com/jhd3197/RepoGif) — the tool used to generate the banner GIF!

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Adobe After Effects** is a trademark of Adobe Inc. This project is not affiliated with, endorsed by, or sponsored by Adobe Inc.

This is an automation and middleware tool that translates Python commands into Adobe-supported ExtendScript instructions. It does not modify, crack, or bypass Adobe software. It does not distribute Adobe assets or binaries. It does not enable use of After Effects without a license. A valid Adobe Creative Cloud license is required. We do not support or condone software piracy in any form.

---

<div align="center">

**After Effects Automation** — JSON in, video out.

Made with care by [Juan Denis](https://juandenis.com)

</div>
