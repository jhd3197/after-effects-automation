<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**Automatiza After Effects desde Python. Habla con AE usando IA.**

JSON entra, video sale. Sin interaccion manual con AE.

[English](../README.md) | Español | [中文版](README.zh-CN.md) | [Português](README.pt.md)

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![Downloads](https://img.shields.io/pepy/dt/after-effects-automation?style=flat-square&color=green)](https://pepy.tech/project/after-effects-automation)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](../LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

<br>

[Inicio Rapido](#-inicio-rapido) · [Chat IA](#-panel-de-chat-con-ia) · [Funciones](#-funciones) · [CLI](#-cli) · [Arquitectura](#-arquitectura) · [Hoja de Ruta](#-hoja-de-ruta) · [Contribuir](#-contribuir)

</div>

---

## 🚀 Inicio Rapido

```bash
pip install after-effects-automation
python install_ae_runner.py
ae-automation run config.json
```

**Sin configuracion necesaria.** Detecta automaticamente cada version de AE en tu maquina y elige la mas reciente. Funciona desde 2020 hasta 2026+ — sin rutas fijas, sin `.env` requerido.

```python
from ae_automation import Client
Client().startBot("config.json")
```

---

## 🤖 Panel de Chat con IA

Controla After Effects con lenguaje natural — directamente dentro de AE. Impulsado por [Prompture](https://github.com/jhd3197/prompture).

```bash
python install_extension.py        # instalar el panel en AE
ae-automation chat                  # iniciar backend
# En AE: Window > Extensions > AE Automation Chat
```

| Tu dices | AE hace |
|----------|---------|
| *"Crea una composicion 1080p llamada Intro, 10 segundos"* | Crea la composicion |
| *"Cambia el texto del titulo a Lanzamiento 2025"* | Actualiza la capa de texto |
| *"Establece el color de fondo a #1A1A2E"* | Aplica el color |
| *"Lista todas las composiciones"* | Devuelve la estructura del proyecto |

Devuelve **botones de accion** clickeables que se ejecutan directamente en AE. Funciona con cualquier LLM — OpenAI, Claude, Ollama, Groq, y mas.

---

## 🎯 Funciones

### Automatizacion

**JSON-Driven** — Describe tu video en un config, la plataforma se encarga del resto

**10 Tipos de Acciones** — Actualizar propiedades, intercambiar capas, agregar recursos, anidar comps, aplicar plantillas, transiciones, marcadores

**Renderizado por Lotes** — Genera cientos de variaciones de video desde datos

**Plantillas Integradas** — Tutorial, redes sociales, showcase de producto, slideshow, promo de evento

### Deteccion Inteligente

**Auto-Descubrimiento** — Escanea tu sistema buscando cada version de AE, siempre elige la mas reciente. Sin anos hardcodeados

**Compatibilidad de Version** — Base de conocimiento que rastrea que scripts funcionan en cada version de AE. Los scripts que congelarian AE se bloquean antes de ejecutarse con sugerencias de alternativas

**Multiplataforma** — Windows soportado, macOS en progreso. Rutas, directorios de datos e instalacion de CEP se adaptan a tu SO

### IA y Herramientas

**Panel de Chat** — Extension CEP con backend [Prompture](https://github.com/jhd3197/prompture) (cualquier proveedor LLM)

**Editor Web** — Editor visual de configs basado en navegador con deshacer/rehacer

**40+ Archivos ExtendScript** — Manipulacion directa de AE via cola de comandos basada en archivos

---

## 🖥️ CLI

| Comando | Descripcion |
|---------|-------------|
| `ae-automation run config.json` | Ejecutar el pipeline completo |
| `ae-automation chat` | Iniciar backend del panel de chat IA |
| `ae-automation batch *.json` | Ejecutar multiples configs secuencialmente |
| `ae-automation editor config.json` | Abrir editor visual web |
| `ae-automation generate --template tutorial` | Generar .aep desde plantilla integrada |
| `ae-automation export --template social-media` | Generar + renderizar en un paso |
| `ae-automation plugins list` | Listar, instalar, buscar, ejecutar plugins |
| `ae-automation test` | Ejecutar pruebas de compatibilidad |
| `ae-automation diagnose` | Verificar instalacion de AE y scripting |

---

## 🏗️ Arquitectura

```
Config Python (JSON) → Puente JS → ExtendScript en AE → Composicion → aerender → MP4
```

| Capa | Tecnologia |
|------|------------|
| Backend | Python 3.9+, Flask, Flask-CORS |
| IA | Prompture (cualquier proveedor LLM) |
| Puente AE | ExtendScript (JSX), cola de comandos basada en archivos |
| Editor Web | React 18, Vite, Zustand |
| Panel CEP | HTML/CSS/JS, CSInterface |
| Renderizado | aerender (Adobe CLI) |

---

## 🗺️ Hoja de Ruta

- [x] Automatizacion core — Python a ExtendScript a AE a render
- [x] Pipeline de config JSON — plantillas, acciones custom, recursos
- [x] CLI — run, chat, editor, generate, export, test, diagnose
- [x] Panel de chat IA — extension CEP con backend Prompture
- [x] Auto-descubrimiento — deteccion de version y capa de compatibilidad
- [x] Editor web — edicion visual de configs
- [x] Plantillas integradas — 5 plantillas listas para usar
- [x] Soporte macOS — capa de abstraccion multiplataforma
- [x] Progreso de render en tiempo real — barra de progreso en el panel de chat
- [x] Cola de lotes — procesamiento secuencial multi-video con seguimiento de estado
- [x] Marketplace de plugins — plantillas y acciones comunitarias con instalar/buscar/ejecutar

---

## 🤝 Contribuir

```
fork → feature branch → commit → push → pull request
```

[Reportar Bug](https://github.com/jhd3197/after-effects-automation/issues) · [Solicitar Funcion](https://github.com/jhd3197/after-effects-automation/issues)

---

## Licencia

MIT License — ver [LICENSE](../LICENSE).

**Adobe After Effects** es una marca registrada de Adobe Inc. Este proyecto no esta afiliado, respaldado ni patrocinado por Adobe Inc.

Esta es una herramienta de automatizacion y middleware que traduce comandos Python en instrucciones ExtendScript soportadas por Adobe. No modifica, crackea ni evita el software de Adobe. No distribuye activos ni binarios de Adobe. No permite el uso de After Effects sin licencia. Se requiere una licencia valida de Adobe Creative Cloud.

---

<div align="center">

**After Effects Automation** — JSON entra, video sale.

Hecho con cuidado por [Juan Denis](https://juandenis.com)

</div>
