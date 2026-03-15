<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**Automatiza After Effects desde Python. Habla con AE usando IA.**

Define composiciones en JSON, controla desde Python o la CLI,
chatea con AE en lenguaje natural y renderiza a escala.

[English](../README.md) | Español | [中文版](README.zh-CN.md) | [Português](README.pt.md)

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

# 2. Configurar el puente con AE
python install_ae_runner.py

# 3. Ejecutar
ae-automation run config.json
```

O desde Python:

```python
from ae_automation import Client

client = Client()
client.startBot("config.json")
```

---

## Panel de Chat con IA

Controla After Effects con lenguaje natural — directamente dentro de AE.

```bash
# 1. Instalar la extension
python install_extension.py

# 2. Iniciar el backend
ae-automation chat

# 3. En AE: Window > Extensions > AE Automation Chat
```

Escribe lo que quieras:
- *"Crea una composicion 1080p llamada Intro de 10 segundos"*
- *"Cambia el texto del titulo a Lanzamiento 2025"*
- *"Lista todas las composiciones"*
- *"Guarda el proyecto"*

Funciona con cualquier proveedor de IA mediante [Prompture](https://github.com/jhd3197/prompture) — OpenAI, Claude, Ollama, y mas.

---

## CLI

| Comando | Descripcion |
|---------|-------------|
| `ae-automation run config.json` | Ejecutar pipeline completo |
| `ae-automation chat` | Iniciar backend del chat IA (puerto 5001) |
| `ae-automation editor config.json` | Abrir editor visual web (puerto 5000) |
| `ae-automation generate --template tutorial` | Generar .aep desde plantilla |
| `ae-automation export --template social-media` | Generar + renderizar en un paso |
| `ae-automation test` | Ejecutar pruebas de compatibilidad |
| `ae-automation diagnose` | Verificar instalacion de AE |

---

## Licencia

MIT License — ver [LICENSE](../LICENSE).

---

<div align="center">

**After Effects Automation** — JSON entra, video sale.

Hecho con cuidado por [Juan Denis](https://juandenis.com)

</div>
