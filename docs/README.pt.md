<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**Automatize o After Effects com Python. Converse com AE usando IA.**

Defina composicoes em JSON, controle com Python ou CLI,
converse com AE em linguagem natural e renderize em escala.

[English](../README.md) | [Español](README.es.md) | [中文版](README.zh-CN.md) | Português

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](../LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

</div>

---

## Inicio Rapido

```bash
# 1. Instalar
pip install after-effects-automation

# 2. Configurar a ponte com AE
python install_ae_runner.py

# 3. Executar
ae-automation run config.json
```

Ou com Python:

```python
from ae_automation import Client

client = Client()
client.startBot("config.json")
```

---

## Painel de Chat com IA

Controle o After Effects com linguagem natural — direto dentro do AE.

```bash
# 1. Instalar a extensao
python install_extension.py

# 2. Iniciar o backend
ae-automation chat

# 3. No AE: Window > Extensions > AE Automation Chat
```

Digite o que voce quer:
- *"Crie uma composicao 1080p chamada Intro de 10 segundos"*
- *"Mude o texto do titulo para Lancamento 2025"*
- *"Liste todas as composicoes"*
- *"Salve o projeto"*

Funciona com qualquer provedor de IA via [Prompture](https://github.com/jhd3197/prompture) — OpenAI, Claude, Ollama e mais.

---

## CLI

| Comando | Descricao |
|---------|-----------|
| `ae-automation run config.json` | Executar pipeline completo |
| `ae-automation chat` | Iniciar backend do chat IA (porta 5001) |
| `ae-automation editor config.json` | Abrir editor visual web (porta 5000) |
| `ae-automation generate --template tutorial` | Gerar .aep a partir de template |
| `ae-automation export --template social-media` | Gerar + renderizar em um passo |
| `ae-automation test` | Executar testes de compatibilidade |
| `ae-automation diagnose` | Verificar instalacao do AE |

---

## Licenca

MIT License — veja [LICENSE](../LICENSE).

---

<div align="center">

**After Effects Automation** — JSON entra, video sai.

Feito com cuidado por [Juan Denis](https://juandenis.com)

</div>
