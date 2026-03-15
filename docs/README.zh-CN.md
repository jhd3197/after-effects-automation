<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**从 Python 自动化 After Effects，用 AI 与 AE 对话。**

JSON 输入，视频输出。无需手动操作 AE。

[English](../README.md) | [Español](README.es.md) | 中文版 | [Português](README.pt.md)

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![Downloads](https://img.shields.io/pepy/dt/after-effects-automation?style=flat-square&color=green)](https://pepy.tech/project/after-effects-automation)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](../LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

<br>

[快速开始](#-快速开始) · [AI 聊天](#-ai-聊天面板) · [功能](#-功能) · [命令行](#-命令行) · [架构](#-架构) · [路线图](#-路线图) · [贡献](#-贡献)

</div>

---

## 🚀 快速开始

```bash
pip install after-effects-automation
python install_ae_runner.py
ae-automation run config.json
```

**无需配置。** 自动检测机器上所有 AE 版本并选择最新版。支持 2020 到 2026+ — 无硬编码路径，无需 `.env` 文件。

```python
from ae_automation import Client
Client().startBot("config.json")
```

---

## 🤖 AI 聊天面板

用自然语言控制 After Effects — 直接在 AE 内操作。由 [Prompture](https://github.com/jhd3197/prompture) 驱动。

```bash
python install_extension.py        # 安装 AE 面板
ae-automation chat                  # 启动后端
# 在 AE 中：Window > Extensions > AE Automation Chat
```

| 你说 | AE 执行 |
|------|---------|
| *"创建一个 1080p 的合成叫 Intro，10 秒"* | 创建合成 |
| *"将标题文字改为产品发布 2025"* | 更新文字图层 |
| *"设置背景颜色为 #1A1A2E"* | 应用颜色 |
| *"列出所有合成"* | 返回项目结构 |

返回可点击的**操作按钮**，直接在 AE 中执行。支持任何 LLM — OpenAI、Claude、Ollama、Groq 等。

---

## 🎯 功能

### 自动化

**JSON 驱动** — 在配置中描述你的视频，平台处理其余一切

**10 种操作类型** — 更新属性、替换图层、添加资源、嵌套合成、应用模板、转场、标记

**批量渲染** — 从数据源生成数百个视频变体

**内置模板** — 教程、社交媒体、产品展示、幻灯片、活动推广

### 智能检测

**自动发现** — 扫描系统中所有 AE 版本，始终选择最新版。无硬编码年份

**版本兼容性** — 知识库跟踪哪些脚本在哪些 AE 版本上可用。会导致冻结的脚本在执行前被阻止，并提供替代方案

**跨平台** — 支持 Windows，macOS 进行中。路径、数据目录和 CEP 安装均适配你的操作系统

### AI 和工具

**聊天面板** — CEP 扩展配合 [Prompture](https://github.com/jhd3197/prompture) 后端（任何 LLM 提供商）

**Web 编辑器** — 基于浏览器的可视化配置编辑器，支持撤销/重做

**40+ ExtendScript 文件** — 通过基于文件的命令队列直接操作 AE

---

## 🖥️ 命令行

| 命令 | 说明 |
|------|------|
| `ae-automation run config.json` | 运行完整自动化流程 |
| `ae-automation chat` | 启动 AI 聊天面板后端 |
| `ae-automation batch *.json` | 按顺序运行多个配置 |
| `ae-automation editor config.json` | 打开可视化 Web 编辑器 |
| `ae-automation generate --template tutorial` | 从内置模板生成 .aep |
| `ae-automation export --template social-media` | 一步生成 + 渲染 |
| `ae-automation plugins list` | 列出、安装、搜索、运行社区插件 |
| `ae-automation test` | 运行兼容性测试 |
| `ae-automation diagnose` | 检查 AE 安装和脚本设置 |

---

## 🏗️ 架构

```
Python 配置 (JSON) → JS 桥接 → AE 中的 ExtendScript → 合成 → aerender → MP4
```

| 层 | 技术 |
|----|------|
| 后端 | Python 3.9+、Flask、Flask-CORS |
| AI | Prompture（任何 LLM 提供商） |
| AE 桥接 | ExtendScript (JSX)、基于文件的命令队列 |
| Web 编辑器 | React 18、Vite、Zustand |
| CEP 面板 | HTML/CSS/JS、CSInterface |
| 渲染 | aerender（Adobe CLI） |

---

## 🗺️ 路线图

- [x] 核心自动化 — Python 到 ExtendScript 到 AE 到渲染
- [x] JSON 配置流程 — 模板、自定义操作、资源
- [x] CLI — run、chat、editor、generate、export、test、diagnose
- [x] AI 聊天面板 — CEP 扩展配合 Prompture 后端
- [x] 自动发现 — 版本检测和兼容性层
- [x] Web 编辑器 — 可视化配置编辑
- [x] 内置模板 — 5 个即用模板
- [x] macOS 支持 — 跨平台抽象层
- [x] 实时渲染进度 — 聊天面板中的实时进度条
- [x] 批量队列 — 顺序多视频处理及状态跟踪
- [x] 插件市场 — 社区模板和操作，支持安装/搜索/运行

---

## 🤝 贡献

```
fork → feature branch → commit → push → pull request
```

[报告 Bug](https://github.com/jhd3197/after-effects-automation/issues) · [请求功能](https://github.com/jhd3197/after-effects-automation/issues)

---

## 许可证

MIT License — 详见 [LICENSE](../LICENSE)。

**Adobe After Effects** 是 Adobe Inc. 的商标。本项目不隶属于 Adobe Inc.，未经其认可或赞助。

本工具是一个自动化中间件，将 Python 命令转换为 Adobe 支持的 ExtendScript 指令。不修改、破解或绕过 Adobe 软件。不分发 Adobe 资产或二进制文件。不允许在无许可证的情况下使用 After Effects。需要有效的 Adobe Creative Cloud 许可证。

---

<div align="center">

**After Effects Automation** — JSON 输入，视频输出。

由 [Juan Denis](https://juandenis.com) 用心制作

</div>
