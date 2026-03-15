<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**从 Python 自动化 After Effects，用 AI 与 AE 对话。**

用 JSON 定义合成，通过 Python 或命令行驱动，
用自然语言与 AE 聊天，批量渲染视频。

[English](../README.md) | [Español](README.es.md) | 中文版 | [Português](README.pt.md)

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](../LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

</div>

---

## 快速开始

```bash
# 1. 安装
pip install after-effects-automation

# 2. 配置 AE 桥接
python install_ae_runner.py

# 3. 运行
ae-automation run config.json
```

或通过 Python：

```python
from ae_automation import Client

client = Client()
client.startBot("config.json")
```

---

## AI 聊天面板

用自然语言控制 After Effects — 直接在 AE 内操作。

```bash
# 1. 安装扩展
python install_extension.py

# 2. 启动聊天后端
ae-automation chat

# 3. 在 AE 中：Window > Extensions > AE Automation Chat
```

直接输入你想做的：
- *"创建一个 1080p 的合成叫 Intro，10 秒"*
- *"将标题文字改为产品发布 2025"*
- *"列出所有合成"*
- *"保存项目"*

通过 [Prompture](https://github.com/jhd3197/prompture) 支持任何 AI 提供商 — OpenAI、Claude、Ollama 等。

---

## 命令行

| 命令 | 说明 |
|------|------|
| `ae-automation run config.json` | 运行完整自动化流程 |
| `ae-automation chat` | 启动 AI 聊天后端（端口 5001） |
| `ae-automation editor config.json` | 打开可视化编辑器（端口 5000） |
| `ae-automation generate --template tutorial` | 从模板生成 .aep |
| `ae-automation export --template social-media` | 一步生成 + 渲染 |
| `ae-automation test` | 运行兼容性测试 |
| `ae-automation diagnose` | 检查 AE 安装 |

---

## 许可证

MIT License — 详见 [LICENSE](../LICENSE)。

---

<div align="center">

**After Effects Automation** — JSON 输入，视频输出。

由 [Juan Denis](https://juandenis.com) 用心制作

</div>
