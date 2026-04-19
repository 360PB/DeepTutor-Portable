<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: агентно-нативное персонализированное обучение

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[Возможности](#key-features) · [Быстрый старт](#get-started) · [Обзор](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [Дорожная карта](#roadmap) · [Сообщество](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md)

</div>

---
### 📰 Новости

> **[2026.4.4]** Давно не виделись! ✨ Вышел DeepTutor v1.0.0 — агентно-нативная эволюция: архитектура переписана с нуля, TutorBot и гибкие режимы под Apache-2.0. Начинается новая глава!

> **[2026.2.6]** 🚀 10k звёзд за 39 дней — спасибо сообществу!

> **[2026.1.1]** С Новым годом! [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78), [Discussions](https://github.com/HKUDS/DeepTutor/discussions).

> **[2025.12.29]** Официальный релиз DeepTutor.

### 📦 Релизы

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — инвалидация кэша во время выполнения для горячей перезагрузки настроек, вложенный вывод MinerU, исправление mimic WebSocket, минимум Python 3.11+ и улучшения CI.

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — агентно-нативная переработка архитектуры (DeepTutor 2.0): двухуровневая модель плагинов (Tools + Capabilities), входы CLI и SDK, многоканальный TutorBot, Co-Writer, Guided Learning и постоянная память.

<details>
<summary><b>Прошлые релизы</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — сессии, инкрементальная загрузка, гибкий RAG, полная китайская локализация.

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, логи, исправления.

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — единая конфигурация, RAG по KB, генерация вопросов, боковая панель.

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — мульти-провайдеры LLM/эмбеддинги, новая главная, разделение RAG, переменные окружения.

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, образы GHCR.

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 и React 19, WebSocket, уязвимости.

</details>

<a id="key-features"></a>
## ✨ Ключевые возможности

- **Единое чат-пространство** — пять режимов в одной ветке: Chat, Deep Solve, квизы, Deep Research, Math Animator с общим контекстом.
- **Персональные TutorBot** — не чат-боты: автономные репетиторы со своей памятью, личностью и навыками. [nanobot](https://github.com/HKUDS/nanobot).
- **AI Co-Writer** — Markdown: переписать, расширить, сократить с KB и вебом.
- **Guided Learning** — визуальные пошаговые маршруты по вашим материалам.
- **Центр знаний** — PDF, Markdown, текст для RAG; цветные блокноты.
- **Постоянная память** — сводка прогресса и профиль ученика; общая с TutorBot.
- **Агентно-нативный CLI** — возможности, KB, сессии, TutorBot одной командой; Rich и JSON. [`SKILL.md`](../../SKILL.md).

---

<a id="get-started"></a>
## 🚀 Быстрый старт

### Вариант A — интерактивный тур (рекомендуется)

**Один скрипт** — зависимости, окружение, проверка связи, запуск.

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

conda create -n deeptutor python=3.11 && conda activate deeptutor
# или: python -m venv .venv && source .venv/bin/activate

python scripts/start_tour.py
```

- **Web** — профиль, pip + npm, временный сервер, **Настройки**, 4 шага (LLM, эмбеддинги, поиск).
- **CLI** — всё в терминале.

[http://localhost:3782](http://localhost:3782)

<a id="option-b-manual"></a>
### Вариант B — ручная локальная установка

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

conda create -n deeptutor python=3.11 && conda activate deeptutor
pip install -e ".[server]"

cd web && npm install && cd ..
```

```bash
cp .env.example .env
```

```dotenv
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
EMBEDDING_HOST=https://api.openai.com/v1
EMBEDDING_DIMENSION=3072
```

<details>
<summary><b>Поддерживаемые провайдеры LLM</b></summary>

| Провайдер | Binding | Базовый URL по умолчанию |
|:--|:--|:--|
| AiHubMix | `aihubmix` | `https://aihubmix.com/v1` |
| Anthropic | `anthropic` | `https://api.anthropic.com/v1` |
| Azure OpenAI | `azure_openai` | — |
| BytePlus | `byteplus` | `https://ark.ap-southeast.bytepluses.com/api/v3` |
| BytePlus Coding Plan | `byteplus_coding_plan` | `https://ark.ap-southeast.bytepluses.com/api/coding/v3` |
| Custom (OpenAI-compat) | `custom` | — |
| DashScope (Qwen) | `dashscope` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| DeepSeek | `deepseek` | `https://api.deepseek.com` |
| Gemini | `gemini` | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| GitHub Copilot | `github_copilot` | `https://api.githubcopilot.com` |
| Groq | `groq` | `https://api.groq.com/openai/v1` |
| MiniMax | `minimax` | `https://api.minimax.io/v1` |
| Mistral | `mistral` | `https://api.mistral.ai/v1` |
| Moonshot (Kimi) | `moonshot` | `https://api.moonshot.ai/v1` |
| Ollama | `ollama` | `http://localhost:11434/v1` |
| OpenAI | `openai` | `https://api.openai.com/v1` |
| OpenAI Codex | `openai_codex` | `https://chatgpt.com/backend-api` |
| OpenRouter | `openrouter` | `https://openrouter.ai/api/v1` |
| OpenVINO Model Server | `ovms` | `http://localhost:8000/v3` |
| Qianfan (Ernie) | `qianfan` | `https://qianfan.baidubce.com/v2` |
| SiliconFlow | `siliconflow` | `https://api.siliconflow.cn/v1` |
| Step Fun | `stepfun` | `https://api.stepfun.com/v1` |
| vLLM | `vllm` | `http://localhost:8000/v1` |
| VolcEngine | `volcengine` | `https://ark.cn-beijing.volces.com/api/v3` |
| VolcEngine Coding Plan | `volcengine_coding_plan` | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Xiaomi MIMO | `xiaomi_mimo` | `https://api.xiaomimimo.com/v1` |
| Zhipu AI (GLM) | `zhipu` | `https://open.bigmodel.cn/api/paas/v4` |

</details>

<details>
<summary><b>Поддерживаемые провайдеры эмбеддингов</b></summary>

Эмбеддинги используют тот же список, что и LLM. Частые примеры:

| Провайдер | Binding | Пример модели |
|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` |
| DashScope | `dashscope` | `text-embedding-v3` |
| Ollama | `ollama` | `nomic-embed-text` |
| SiliconFlow | `siliconflow` | `BAAI/bge-m3` |
| vLLM | `vllm` | Любая embedding-модель |
| OpenAI-совместимый | `custom` | — |

</details>

<details>
<summary><b>Поддерживаемые веб-поисковые провайдеры</b></summary>

| Провайдер | Переменная окружения | Примечания |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | Рекомендуется, есть бесплатный уровень |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Самохостинг, без API-ключа |
| DuckDuckGo | — | Без API-ключа |
| Perplexity | `PERPLEXITY_API_KEY` | Нужен API-ключ |

</details>

```bash
python -m deeptutor.api.run_server
cd web && npm run dev -- -p 3782
```

| Сервис | Порт |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

### Вариант C — Docker

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

Как в [варианте B](#option-b-manual).

**2a. Официальный образ** — [GHCR](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor)

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

**2b. Сборка** — `docker compose up -d`

**3.** [http://localhost:3782](http://localhost:3782)

```bash
docker compose logs -f
docker compose down
```

<details>
<summary><b>Облако / удалённый сервер</b></summary>

```dotenv
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

</details>

<details>
<summary><b>Режим разработки (hot-reload)</b></summary>

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

</details>

<details>
<summary><b>Свои порты</b></summary>

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

</details>

<details>
<summary><b>Персистентность данных</b></summary>

| Контейнер | Хост | Содержимое |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Настройки, память, workspace, сессии, логи |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | Документы и векторы |

</details>

<details>
<summary><b>Переменные окружения</b></summary>

| Переменная | Обяз. | Описание |
|:---|:---:|:---|
| `LLM_BINDING` | **Да** | Провайдер LLM |
| `LLM_MODEL` | **Да** | Модель |
| `LLM_API_KEY` | **Да** | Ключ |
| `LLM_HOST` | **Да** | URL |
| `EMBEDDING_BINDING` | **Да** | Эмбеддинги |
| `EMBEDDING_MODEL` | **Да** | Модель |
| `EMBEDDING_API_KEY` | **Да** | Ключ |
| `EMBEDDING_HOST` | **Да** | URL |
| `EMBEDDING_DIMENSION` | **Да** | Размерность |
| `SEARCH_PROVIDER` | Нет | Поиск |
| `SEARCH_API_KEY` | Нет | Ключ |
| `BACKEND_PORT` | Нет | по умолч. `8001` |
| `FRONTEND_PORT` | Нет | по умолч. `3782` |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | Нет | Публичный URL |
| `DISABLE_SSL_VERIFY` | Нет | по умолч. `false` |

</details>

### Вариант D — только CLI

```bash
pip install -e ".[cli]"
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> Полное руководство: [DeepTutor CLI](#deeptutor-cli-guide).

---

<a id="explore-deeptutor"></a>
## 📖 Обзор DeepTutor

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="Архитектура DeepTutor" width="800">
</div>

### 💬 Чат — единое интеллектуальное пространство

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="Чат" width="800">
</div>

Пять режимов, **единый контекст**.

| Режим | Назначение |
|:---|:---|
| **Chat** | RAG, веб, код, рассуждения, мозговой штурм, статьи. |
| **Deep Solve** | Мультиагенты с цитатами. |
| **Генерация квизов** | Оценки по KB. |
| **Deep Research** | Подтемы, параллельные агенты, отчёт с ссылками. |
| **Math Animator** | Manim. |

Инструменты **отделены от сценариев**.

### ✍️ Co-Writer — ИИ в редакторе

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

**Переписать**, **Расширить**, **Сократить**; отмена/повтор; блокноты.

### 🎓 Guided Learning

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="Guided Learning" width="800">
</div>

1. План (3–5 пунктов).  
2. Интерактивные страницы.  
3. Контекстные вопросы.  
4. Итог.

### 📚 Управление знаниями

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="Знания" width="800">
</div>

- **Базы знаний** — PDF, TXT, MD.  
- **Блокноты** — по сессиям и цветам.

### 🧠 Память

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="Память" width="800">
</div>

- **Сводка** — прогресс.  
- **Профиль** — предпочтения, уровень, цели. Общая с TutorBot.

---

<a id="tutorbot"></a>
### 🦞 TutorBot — постоянные автономные ИИ-репетиторы

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="Архитектура TutorBot" width="800">
</div>

**Мультиинстансный** агент на [nanobot](https://github.com/HKUDS/nanobot): свой цикл, workspace, память, личность.

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Шаблоны Soul** — личность и педагогика.  
- **Отдельный workspace** — память, сессии, навыки; общий слой DeepTutor.  
- **Проактивный Heartbeat** — напоминания и задачи.  
- **Полный набор инструментов** — RAG, код, веб, статьи, рассуждения, мозговой штурм.  
- **Навыки** — файлы skill.  
- **Мультиканал** — Telegram, Discord, Slack, Feishu, WeCom, DingTalk, почта и др.  
- **Команды и субагенты**.

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI — интерфейс для агентов

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI" width="800">
</div>

Без браузера: возможности, KB, сессии, память, TutorBot. Rich + JSON. [`SKILL.md`](../../SKILL.md).

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# В REPL: /cap, /tool, /kb, /history, /notebook, /config для переключения на лету
```

```bash
deeptutor kb create my-kb --doc textbook.pdf
deeptutor kb add my-kb --docs-dir ./papers/
deeptutor kb search my-kb "gradient descent"
deeptutor kb set-default my-kb
```

```bash
deeptutor run chat "Summarize chapter 3" -f rich
deeptutor run chat "Summarize chapter 3" -f json
```

```bash
deeptutor session list
deeptutor session open <id>
```

<details>
<summary><b>Полная справка по CLI</b></summary>

**Верхний уровень**

| Команда | Описание |
|:---|:---|
| `deeptutor run <capability> <message>` | Запуск возможности за один ход (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | Интерактивный REPL с `--capability`, `--tool`, `--kb`, `--language` и др. |
| `deeptutor serve` | Запуск сервера API DeepTutor |

**`deeptutor bot`**

| Команда | Описание |
|:---|:---|
| `deeptutor bot list` | Список экземпляров TutorBot |
| `deeptutor bot create <id>` | Создать и запустить бота (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | Запустить бота |
| `deeptutor bot stop <id>` | Остановить бота |

**`deeptutor kb`**

| Команда | Описание |
|:---|:---|
| `deeptutor kb list` | Список баз знаний |
| `deeptutor kb info <name>` | Детали базы |
| `deeptutor kb create <name>` | Создать из документов (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | Добавить документы |
| `deeptutor kb search <name> <query>` | Поиск по базе |
| `deeptutor kb set-default <name>` | База по умолчанию |
| `deeptutor kb delete <name>` | Удалить (`--force`) |

**`deeptutor memory`**

| Команда | Описание |
|:---|:---|
| `deeptutor memory show [file]` | Просмотр (`summary`, `profile`, `all`) |
| `deeptutor memory clear [file]` | Очистить (`--force`) |

**`deeptutor session`**

| Команда | Описание |
|:---|:---|
| `deeptutor session list` | Список сессий (`--limit`) |
| `deeptutor session show <id>` | Сообщения сессии |
| `deeptutor session open <id>` | Продолжить в REPL |
| `deeptutor session rename <id>` | Переименовать (`--title`) |
| `deeptutor session delete <id>` | Удалить |

**`deeptutor notebook`**

| Команда | Описание |
|:---|:---|
| `deeptutor notebook list` | Список блокнотов |
| `deeptutor notebook create <name>` | Создать (`--description`) |
| `deeptutor notebook show <id>` | Записи |
| `deeptutor notebook add-md <id> <path>` | Импорт Markdown |
| `deeptutor notebook replace-md <id> <rec> <path>` | Заменить запись |
| `deeptutor notebook remove-record <id> <rec>` | Удалить запись |

**`deeptutor config` / `plugin` / `provider`**

| Команда | Описание |
|:---|:---|
| `deeptutor config show` | Сводка конфигурации |
| `deeptutor plugin list` | Зарегистрированные инструменты и возможности |
| `deeptutor plugin info <name>` | Детали инструмента или возможности |
| `deeptutor provider login <provider>` | OAuth (`openai-codex`, `github-copilot`) |

</details>

<a id="roadmap"></a>
## 🗺️ Дорожная карта

| Статус | Этап |
|:---:|:---|
| 🔜 | **Аутентификация и вход** — опциональная страница входа для публичных развёртываний и мультипользовательский режим |
| 🔜 | **Темы и оформление** — разнообразные темы и настройка интерфейса |
| 🔜 | **Интеграция LightRAG** — подключение [LightRAG](https://github.com/HKUDS/LightRAG) как продвинутого движка баз знаний |
| 🔜 | **Сайт документации** — полная документация: руководства, справочник API и учебные материалы |

> Если DeepTutor вам полезен, [поставьте звезду](https://github.com/HKUDS/DeepTutor/stargazers) — это помогает проекту!

---

<a id="community"></a>
## 🌐 Сообщество и экосистема

| Проект | Роль |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | Движок TutorBot |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| Быстрый RAG | Агенты без кода | Автоисследования | Лёгкий агент |

## 🤝 Участие

<div align="center">

Надеемся, что DeepTutor станет подарком сообществу. 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>
</div>

См. [CONTRIBUTING.md](../../CONTRIBUTING.md).

## ⭐ История звёзд

<div align="center">
<a href="https://www.star-history.com/#HKUDS/DeepTutor&type=timeline&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
    <img alt="Star History" src="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
  </picture>
</a>
</div>

<div align="center">

**[Data Intelligence Lab @ HKU](https://github.com/HKUDS)**

[⭐ Star](https://github.com/HKUDS/DeepTutor/stargazers) · [🐛 Issues](https://github.com/HKUDS/DeepTutor/issues) · [💬 Discussions](https://github.com/HKUDS/DeepTutor/discussions)

---

[Apache License 2.0](../../LICENSE)

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.DeepTutor&style=for-the-badge&color=00d4ff" alt="Views">
</p>

</div>
