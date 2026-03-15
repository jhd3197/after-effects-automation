<div align="center">

# After Effects Automation

<img width="700" alt="ae_automation" src="https://user-images.githubusercontent.com/13461850/204080205-624daba4-9883-429b-aa16-e4bb0b3221d7.png" />

**Automatize o After Effects com Python. Converse com AE usando IA.**

JSON entra, video sai. Sem interacao manual com o AE.

[English](../README.md) | [Español](README.es.md) | [中文版](README.zh-CN.md) | Português

<br>

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![After Effects](https://img.shields.io/badge/After_Effects-9999FF?style=for-the-badge&logo=adobeaftereffects&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI](https://img.shields.io/pypi/v/after-effects-automation?style=flat-square&color=blue)](https://pypi.org/project/after-effects-automation/)
[![Downloads](https://img.shields.io/pepy/dt/after-effects-automation?style=flat-square&color=green)](https://pepy.tech/project/after-effects-automation)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](../LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/after-effects-automation?style=flat-square&color=f5c542)](https://github.com/jhd3197/after-effects-automation/stargazers)

<br>

[Inicio Rapido](#-inicio-rapido) · [Chat IA](#-painel-de-chat-com-ia) · [Funcionalidades](#-funcionalidades) · [CLI](#-cli) · [Arquitetura](#-arquitetura) · [Roteiro](#-roteiro) · [Contribuir](#-contribuir)

</div>

---

## 🚀 Inicio Rapido

```bash
pip install after-effects-automation
python install_ae_runner.py
ae-automation run config.json
```

**Sem configuracao necessaria.** Detecta automaticamente cada versao do AE na sua maquina e escolhe a mais recente. Funciona de 2020 a 2026+ — sem caminhos fixos, sem `.env` necessario.

```python
from ae_automation import Client
Client().startBot("config.json")
```

---

## 🤖 Painel de Chat com IA

Controle o After Effects com linguagem natural — direto dentro do AE. Alimentado por [Prompture](https://github.com/jhd3197/prompture).

```bash
python install_extension.py        # instalar o painel no AE
ae-automation chat                  # iniciar backend
# No AE: Window > Extensions > AE Automation Chat
```

| Voce diz | AE faz |
|----------|--------|
| *"Crie uma composicao 1080p chamada Intro, 10 segundos"* | Cria a composicao |
| *"Mude o texto do titulo para Lancamento 2025"* | Atualiza a camada de texto |
| *"Defina a cor de fundo para #1A1A2E"* | Aplica a cor |
| *"Liste todas as composicoes"* | Retorna a estrutura do projeto |

Retorna **botoes de acao** clicaveis que executam diretamente no AE. Funciona com qualquer LLM — OpenAI, Claude, Ollama, Groq e mais.

---

## 🎯 Funcionalidades

### Automacao

**JSON-Driven** — Descreva seu video em um config, a plataforma cuida do resto

**10 Tipos de Acao** — Atualizar propriedades, trocar camadas, adicionar recursos, aninhar comps, aplicar templates, transicoes, marcadores

**Renderizacao em Lote** — Gere centenas de variacoes de video a partir de dados

**Templates Integrados** — Tutorial, redes sociais, showcase de produto, slideshow, promo de evento

### Deteccao Inteligente

**Auto-Descoberta** — Escaneia seu sistema procurando cada versao do AE, sempre escolhe a mais recente. Sem anos fixos no codigo

**Compatibilidade de Versao** — Base de conhecimento rastreia quais scripts funcionam em cada versao do AE. Scripts que congelariam sao bloqueados antes da execucao com sugestoes de alternativas

**Multiplataforma** — Windows suportado, macOS em progresso. Caminhos, diretorios de dados e instalacao CEP se adaptam ao seu SO

### IA e Ferramentas

**Painel de Chat** — Extensao CEP com backend [Prompture](https://github.com/jhd3197/prompture) (qualquer provedor LLM)

**Editor Web** — Editor visual de configs baseado em navegador com desfazer/refazer

**40+ Arquivos ExtendScript** — Manipulacao direta do AE via fila de comandos baseada em arquivos

---

## 🖥️ CLI

| Comando | Descricao |
|---------|-----------|
| `ae-automation run config.json` | Executar o pipeline completo |
| `ae-automation chat` | Iniciar backend do painel de chat IA |
| `ae-automation batch *.json` | Executar multiplos configs sequencialmente |
| `ae-automation editor config.json` | Abrir editor visual web |
| `ae-automation generate --template tutorial` | Gerar .aep a partir de template integrado |
| `ae-automation export --template social-media` | Gerar + renderizar em um passo |
| `ae-automation plugins list` | Listar, instalar, buscar, executar plugins da comunidade |
| `ae-automation test` | Executar testes de compatibilidade |
| `ae-automation diagnose` | Verificar instalacao do AE e scripting |

---

## 🏗️ Arquitetura

```
Config Python (JSON) → Ponte JS → ExtendScript no AE → Composicao → aerender → MP4
```

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.9+, Flask, Flask-CORS |
| IA | Prompture (qualquer provedor LLM) |
| Ponte AE | ExtendScript (JSX), fila de comandos baseada em arquivos |
| Editor Web | React 18, Vite, Zustand |
| Painel CEP | HTML/CSS/JS, CSInterface |
| Renderizacao | aerender (Adobe CLI) |

---

## 🗺️ Roteiro

- [x] Automacao core — Python para ExtendScript para AE para render
- [x] Pipeline de config JSON — templates, acoes customizadas, recursos
- [x] CLI — run, chat, editor, generate, export, test, diagnose
- [x] Painel de chat IA — extensao CEP com backend Prompture
- [x] Auto-descoberta — deteccao de versao e camada de compatibilidade
- [x] Editor web — edicao visual de configs
- [x] Templates integrados — 5 templates prontos para uso
- [x] Suporte macOS — camada de abstracao multiplataforma
- [x] Progresso de render em tempo real — barra de progresso no painel de chat
- [x] Fila de lotes — processamento sequencial multi-video com rastreamento de status
- [x] Marketplace de plugins — templates e acoes da comunidade com instalar/buscar/executar

---

## 🤝 Contribuir

```
fork → feature branch → commit → push → pull request
```

[Reportar Bug](https://github.com/jhd3197/after-effects-automation/issues) · [Solicitar Funcionalidade](https://github.com/jhd3197/after-effects-automation/issues)

---

## Licenca

MIT License — veja [LICENSE](../LICENSE).

**Adobe After Effects** e uma marca registrada da Adobe Inc. Este projeto nao e afiliado, endossado ou patrocinado pela Adobe Inc.

Esta e uma ferramenta de automacao e middleware que traduz comandos Python em instrucoes ExtendScript suportadas pela Adobe. Nao modifica, crackeia ou contorna o software da Adobe. Nao distribui ativos ou binarios da Adobe. Nao permite o uso do After Effects sem licenca. Uma licenca valida do Adobe Creative Cloud e necessaria.

---

<div align="center">

**After Effects Automation** — JSON entra, video sai.

Feito com cuidado por [Juan Denis](https://juandenis.com)

</div>
