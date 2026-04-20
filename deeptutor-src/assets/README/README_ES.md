<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: tutoría personalizada nativa para agentes

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[Funciones](#key-features) · [Primeros pasos](#get-started) · [Explorar](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [Hoja de ruta](#roadmap) · [Comunidad](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md) · [🇹🇭 ภาษาไทย](README_TH.md)

</div>

---
### 📦 Lanzamientos

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — Pestaña Channels basada en esquema con enmascaramiento de secretos; RAG unificado en un solo pipeline; refuerzo de coherencia RAG/KB; prompts de chat externalizados; README en tailandés.

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — «Responder ya» universal en todas las capacidades; sincronización de desplazamiento en Co-Writer; selección de mensajes al guardar en el cuaderno; panel de ajustes unificado; botón Stop en streaming; escritura atómica de la configuración de TutorBot.

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — Renovación del análisis de matemáticas LaTeX en bloque; sonda de diagnóstico LLM vía `agents.yaml`; corrección del reenvío de cabeceras extra; arreglo de UUID en SaveToNotebook; guía Docker + LLM local.

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — Sesiones marcables por URL; tema Snow; latido WebSocket y reconexión automática; mejora de rendimiento de ChatComposer; renovación del registro de proveedores de embeddings; proveedor de búsqueda Serper.

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — Cuaderno de preguntas con marcadores y categorías; Mermaid en Visualize; detección de desajuste de embeddings; compatibilidad Qwen/vLLM; soporte LM Studio y llama.cpp; tema Glass.

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — Consolidación de búsqueda con respaldo SearXNG; corrección del cambio de proveedor; fugas de recursos en el frontend.

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Capacidad Visualize (Chart.js/SVG); prevención de duplicados en cuestionarios; soporte del modelo o4-mini.

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — Seguimiento del progreso de embeddings con reintentos por límite de tasa; dependencias multiplataforma; validación MIME.

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — SDK nativo OpenAI/Anthropic (sin litellm); Math Animator en Windows; análisis JSON más robusto; i18n chino completo.

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — Recarga en caliente de ajustes; salida anidada de MinerU; corrección WebSocket; mínimo Python 3.11+.

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — Reescritura nativa de agentes (~200k líneas): modelo de plugins Tools + Capabilities, CLI y SDK, TutorBot, Co-Writer, aprendizaje guiado y memoria persistente.

<details>
<summary><b>Lanzamientos anteriores</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — Persistencia de sesión, carga incremental, importación flexible de RAG, localización completa al chino.

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, logs y correcciones.

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — Configuración unificada, RAG por KB, generación de preguntas, barra lateral.

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — Multi-proveedor LLM/embeddings, nueva home, desacoplamiento RAG, variables de entorno.

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, imágenes GHCR.

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 y React 19, WebSocket, vulnerabilidades.

</details>

### 📰 Noticias

> **[2026.4.4]** ¡Cuánto tiempo! ✨ DeepTutor v1.0.0 ya está aquí: evolución nativa de agentes con reescritura de arquitectura desde cero, TutorBot y modos flexibles bajo Apache-2.0. ¡Un nuevo capítulo comienza!

> **[2026.2.6]** 🚀 ¡10k estrellas en solo 39 días! Gracias a la comunidad.

> **[2026.1.1]** Feliz año nuevo. Únete a [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78) o [Discussions](https://github.com/HKUDS/DeepTutor/discussions).

> **[2025.12.29]** DeepTutor se publica oficialmente.

<a id="key-features"></a>
## ✨ Funciones principales

- **Espacio de chat unificado** — Cinco modos, un hilo: Chat, Deep Solve, generación de cuestionarios, Deep Research y Math Animator comparten contexto.
- **TutorBots personales** — No son chatbots: tutores autónomos con espacio de trabajo, memoria, personalidad y habilidades. Impulsados por [nanobot](https://github.com/HKUDS/nanobot).
- **AI Co-Writer** — Markdown con la IA como colaborador de primer nivel: reescribir, ampliar o acortar con KB y web.
- **Aprendizaje guiado** — Convierte tus materiales en recorridos visuales por pasos.
- **Centro de conocimiento** — PDF, Markdown y texto para bases RAG; cuadernos por color.
- **Memoria persistente** — Resumen de progreso y perfil del aprendiz; compartido con TutorBots.
- **CLI nativo para agentes** — Capacidades, KB, sesiones y TutorBot en un comando; Rich y JSON. Entrega [`SKILL.md`](../../SKILL.md) a tu agente.

---

<a id="get-started"></a>
## 🚀 Primeros pasos

### Requisitos previos

Antes de empezar, asegúrate de tener instalado lo siguiente:

| Requisito | Versión | Comprobar | Notas |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | Cualquiera | `git --version` | Para clonar el repositorio |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | Backend |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` | Build del frontend (no necesario solo CLI o Docker) |
| [npm](https://www.npmjs.com/) | 9+ | `npm --version` | Suele venir con Node.js |

También necesitas una **clave API** de al menos un proveedor LLM (p. ej. [OpenAI](https://platform.openai.com/api-keys), [DeepSeek](https://platform.deepseek.com/), [Anthropic](https://console.anthropic.com/)). El tour de configuración te guiará para introducirla y probar la conexión.

### Opción A — Tour de configuración (recomendado)

Un **único script interactivo** cubre instalación de dependencias, configuración del entorno, prueba de conexión en vivo y arranque. Casi no tendrás que editar `.env` a mano.

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Entorno virtual de Python (elige uno):
conda create -n deeptutor python=3.11 && conda activate deeptutor   # si usas Anaconda/Miniconda
python -m venv .venv && source .venv/bin/activate                    # si no (macOS/Linux)
python -m venv .venv && .venv\Scripts\activate                       # si no (Windows)

python scripts/start_tour.py
```

El tour pregunta cómo quieres usar DeepTutor:

- **Modo web** (recomendado) — Instala todas las dependencias (pip + npm), levanta un servidor temporal y abre la página de **Ajustes** en el navegador. Un tour en cuatro pasos configura LLM, embeddings y búsqueda con prueba de conexión en vivo. Al terminar, DeepTutor se reinicia automáticamente con tu configuración.
- **Modo CLI** — Flujo totalmente interactivo en terminal: perfil de dependencias, instalación, proveedores, verificación y aplicación sin salir del shell.

En ambos casos terminarás con DeepTutor en [http://localhost:3782](http://localhost:3782).

> **Arranque diario** — El tour solo hace falta la primera vez. A partir de entonces inicia con:
>
> ```bash
> python scripts/start_web.py
> ```
>
> Arranca backend y frontend en un solo comando y abre el navegador. Vuelve a ejecutar `start_tour.py` solo si necesitas reconfigurar proveedores o reinstalar dependencias.

<a id="option-b-manual"></a>
### Opción B — Instalación local manual

Si prefieres control total, instala y configura todo tú mismo.

**1. Instalar dependencias**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Crear y activar entorno virtual (igual que en la opción A)
conda create -n deeptutor python=3.11 && conda activate deeptutor

# DeepTutor con dependencias de backend + servidor web
pip install -e ".[server]"

# Frontend (requiere Node.js 18+)
cd web && npm install && cd ..
```

**2. Configurar entorno**

```bash
cp .env.example .env
```

Edita `.env` y rellena al menos los campos obligatorios:

```dotenv
# LLM (obligatorio)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# Embeddings (obligatorio para la base de conocimiento)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
EMBEDDING_HOST=https://api.openai.com/v1
EMBEDDING_DIMENSION=3072
```

<details>
<summary><b>Proveedores LLM admitidos</b></summary>

| Proveedor | Binding | URL base predeterminada |
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
| llama.cpp | `llama_cpp` | `http://localhost:8080/v1` |
| LM Studio | `lm_studio` | `http://localhost:1234/v1` |
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
<summary><b>Proveedores de embeddings admitidos</b></summary>

| Proveedor | Binding | Ejemplo de modelo | Dim. predeterminada |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | nombre del despliegue | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | Cualquier modelo de embedding | — |
| OpenAI-compatible | `custom` | — | — |

Los proveedores compatibles con OpenAI (DashScope, SiliconFlow, etc.) funcionan con el binding `custom` u `openai`.

</details>

<details>
<summary><b>Proveedores de búsqueda web admitidos</b></summary>

| Proveedor | Variable de entorno | Notas |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | Recomendado, hay nivel gratuito |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Autohospedado, sin clave API |
| DuckDuckGo | — | Sin clave API |
| Perplexity | `PERPLEXITY_API_KEY` | Requiere clave API |

</details>

**3. Iniciar servicios**

La forma más rápida de levantar todo:

```bash
python scripts/start_web.py
```

Inicia backend y frontend y abre el navegador automáticamente.

También puedes arrancar cada servicio manualmente en terminales separadas:

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — en otra terminal
cd web && npm run dev -- -p 3782
```

| Servicio | Puerto predeterminado |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

Abre [http://localhost:3782](http://localhost:3782).

### Opción C — Docker

Docker empaqueta backend y frontend en un solo contenedor; no necesitas Python ni Node.js en local. Solo hace falta [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker Engine + Compose en Linux).

**1. Variables de entorno** (necesarias en ambas variantes siguientes)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

Edita `.env` y rellena al menos los campos obligatorios (igual que en la [opción B](#option-b-manual)).

**2a. Descargar imagen oficial (recomendado)**

Las imágenes oficiales se publican en [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) en cada release, para `linux/amd64` y `linux/arm64`.

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

Para fijar una versión, edita la etiqueta de imagen en `docker-compose.ghcr.yml`:

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # o :latest
```

**2b. Compilar desde el código fuente**

```bash
docker compose up -d
```

Construye la imagen localmente desde el `Dockerfile` y arranca el contenedor.

**3. Verificar y administrar**

Abre [http://localhost:3782](http://localhost:3782) cuando el contenedor esté healthy.

```bash
docker compose logs -f   # seguir logs
docker compose down       # detener y eliminar el contenedor
```

<details>
<summary><b>Despliegue en la nube / servidor remoto</b></summary>

En un servidor remoto el navegador debe conocer la URL pública del API backend. Añade en `.env`:

```dotenv
# URL pública donde se alcanza el backend
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

El script de arranque del frontend aplica este valor en tiempo de ejecución; no hace falta reconstruir.

</details>

<details>
<summary><b>Modo desarrollo (recarga en caliente)</b></summary>

Superpone el override de desarrollo para montar el código y activar recarga en caliente en ambos servicios:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Los cambios en `deeptutor/`, `deeptutor_cli/`, `scripts/` y `web/` se reflejan al instante.

</details>

<details>
<summary><b>Puertos personalizados</b></summary>

Sobrescribe los puertos predeterminados en `.env`:

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

Luego reinicia:

```bash
docker compose up -d     # o docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>Persistencia de datos</b></summary>

Los datos de usuario y las bases de conocimiento persisten mediante volúmenes Docker mapeados a carpetas locales:

| Ruta en el contenedor | Ruta en el host | Contenido |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Ajustes, memoria, espacio de trabajo, sesiones, logs |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | Documentos subidos e índices vectoriales |

Estas carpetas sobreviven a `docker compose down` y se reutilizan en el próximo `docker compose up`.

</details>

<details>
<summary><b>Referencia de variables de entorno</b></summary>

| Variable | Obligatorio | Descripción |
|:---|:---:|:---|
| `LLM_BINDING` | **Sí** | Proveedor LLM (`openai`, `anthropic`, etc.) |
| `LLM_MODEL` | **Sí** | Nombre del modelo (p. ej. `gpt-4o`) |
| `LLM_API_KEY` | **Sí** | Clave API del LLM |
| `LLM_HOST` | **Sí** | URL del endpoint |
| `EMBEDDING_BINDING` | **Sí** | Proveedor de embeddings |
| `EMBEDDING_MODEL` | **Sí** | Nombre del modelo de embedding |
| `EMBEDDING_API_KEY` | **Sí** | Clave API de embeddings |
| `EMBEDDING_HOST` | **Sí** | Endpoint de embeddings |
| `EMBEDDING_DIMENSION` | **Sí** | Dimensión del vector |
| `SEARCH_PROVIDER` | No | Proveedor de búsqueda (`tavily`, `jina`, `serper`, `perplexity`, etc.) |
| `SEARCH_API_KEY` | No | Clave de búsqueda |
| `BACKEND_PORT` | No | Puerto backend (predeterminado `8001`) |
| `FRONTEND_PORT` | No | Puerto frontend (predeterminado `3782`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | No | URL pública del backend para despliegue en la nube |
| `DISABLE_SSL_VERIFY` | No | Desactivar verificación SSL (predeterminado `false`) |

</details>

### Opción D — Solo CLI

Si solo quieres la CLI sin el frontend web:

```bash
pip install -e ".[cli]"
```

Sigue siendo necesario configurar el proveedor LLM. Lo más rápido:

```bash
cp .env.example .env   # luego edita .env con tus claves API
```

Una vez configurado:

```bash
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> Guía completa: [DeepTutor CLI](#deeptutor-cli-guide).

---

<a id="explore-deeptutor"></a>
## 📖 Explorar DeepTutor

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="Arquitectura DeepTutor" width="800">
</div>

### 💬 Chat — Espacio inteligente unificado

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="Chat" width="800">
</div>

Cinco modos en un solo espacio con **gestión unificada del contexto**.

| Modo | Qué hace |
|:---|:---|
| **Chat** | RAG, búsqueda web, ejecución de código, razonamiento, lluvia de ideas, papers. |
| **Deep Solve** | Resolución multiagente con citas. |
| **Generación de cuestionarios** | Evaluaciones ancladas a la KB. |
| **Deep Research** | Subtemas, agentes paralelos, informe citado. |
| **Math Animator** | Animaciones con Manim. |

Las herramientas están **desacopladas de los flujos** — eliges qué activar.

### ✍️ Co-Writer — IA en el editor

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

Editor Markdown completo: **Reescribir**, **Ampliar**, **Acortar** con KB o web; deshacer/rehacer; guardar en cuadernos.

### 🎓 Aprendizaje guiado

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="Aprendizaje guiado" width="800">
</div>

1. Plan de aprendizaje (3–5 puntos).  
2. Páginas interactivas HTML.  
3. Preguntas en contexto por paso.  
4. Resumen al terminar.

### 📚 Gestión del conocimiento

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="Conocimiento" width="800">
</div>

- **Bases de conocimiento** — PDF, TXT, Markdown; añadir de forma incremental.  
- **Cuadernos** — Registros por sesiones y colores.

### 🧠 Memoria

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="Memoria" width="800">
</div>

- **Resumen** — Progreso de estudio.  
- **Perfil** — Preferencias, nivel, objetivos, estilo. Compartido con TutorBots.

---

<a id="tutorbot"></a>
### 🦞 TutorBot — Tutores de IA persistentes y autónomos

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="Arquitectura TutorBot" width="800">
</div>

No es un chatbot: es un **agente multiinstancia** persistente basado en [nanobot](https://github.com/HKUDS/nanobot). Cada instancia tiene su bucle, espacio de trabajo, memoria y personalidad.

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Plantillas Soul** — Personalidad y filosofía docente.  
- **Espacio independiente** — Memoria, sesiones, habilidades; acceso a la capa compartida de DeepTutor.  
- **Heartbeat proactivo** — Recordatorios y tareas programadas.  
- **Acceso completo a herramientas** — RAG, código, web, papers, razonamiento, lluvia de ideas.  
- **Aprendizaje de habilidades** — Archivos de skill en el espacio de trabajo.  
- **Multicanal** — Telegram, Discord, Slack, Feishu, WeCom, DingTalk, correo, etc.  
- **Equipos y subagentes** — Tareas largas y complejas.

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI — Interfaz nativa para agentes

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI" width="800">
</div>

CLI completo: capacidades, KB, sesiones, memoria y TutorBot sin navegador. Salida Rich para humanos y JSON para agentes. [`SKILL.md`](../../SKILL.md) para agentes con herramientas.

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# En el REPL: /cap, /tool, /kb, /history, /notebook, /config para cambiar al vuelo
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
<summary><b>Referencia completa de la CLI</b></summary>

**Nivel superior**

| Comando | Descripción |
|:---|:---|
| `deeptutor run <capability> <message>` | Ejecuta una capacidad en un solo turno (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | REPL interactivo con `--capability`, `--tool`, `--kb`, `--language`, etc. |
| `deeptutor serve` | Inicia el servidor API de DeepTutor |

**`deeptutor bot`**

| Comando | Descripción |
|:---|:---|
| `deeptutor bot list` | Lista instancias de TutorBot |
| `deeptutor bot create <id>` | Crea e inicia un bot (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | Inicia un bot |
| `deeptutor bot stop <id>` | Detiene un bot |

**`deeptutor kb`**

| Comando | Descripción |
|:---|:---|
| `deeptutor kb list` | Lista bases de conocimiento |
| `deeptutor kb info <name>` | Detalles de la base |
| `deeptutor kb create <name>` | Crea desde documentos (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | Añade documentos |
| `deeptutor kb search <name> <query>` | Busca en la base |
| `deeptutor kb set-default <name>` | Define la KB por defecto |
| `deeptutor kb delete <name>` | Elimina (`--force`) |

**`deeptutor memory`**

| Comando | Descripción |
|:---|:---|
| `deeptutor memory show [file]` | Ver (`summary`, `profile`, `all`) |
| `deeptutor memory clear [file]` | Borrar (`--force`) |

**`deeptutor session`**

| Comando | Descripción |
|:---|:---|
| `deeptutor session list` | Lista sesiones (`--limit`) |
| `deeptutor session show <id>` | Mensajes de la sesión |
| `deeptutor session open <id>` | Reanudar en el REPL |
| `deeptutor session rename <id>` | Renombrar (`--title`) |
| `deeptutor session delete <id>` | Eliminar |

**`deeptutor notebook`**

| Comando | Descripción |
|:---|:---|
| `deeptutor notebook list` | Lista cuadernos |
| `deeptutor notebook create <name>` | Crear (`--description`) |
| `deeptutor notebook show <id>` | Ver registros |
| `deeptutor notebook add-md <id> <path>` | Importar Markdown |
| `deeptutor notebook replace-md <id> <rec> <path>` | Sustituir registro |
| `deeptutor notebook remove-record <id> <rec>` | Quitar registro |

**`deeptutor config` / `plugin` / `provider`**

| Comando | Descripción |
|:---|:---|
| `deeptutor config show` | Resumen de configuración |
| `deeptutor plugin list` | Herramientas y capacidades registradas |
| `deeptutor plugin info <name>` | Detalle de herramienta o capacidad |
| `deeptutor provider login <provider>` | OAuth (`openai-codex`, `github-copilot`) |

</details>

<a id="roadmap"></a>
## 🗺️ Hoja de ruta

| Estado | Hito |
|:---:|:---|
| 🎯 | **Autenticación e inicio de sesión** — Página de login opcional para despliegues públicos con multiusuario |
| 🎯 | **Temas y apariencia** — Más temas y personalización de la interfaz |
| 🎯 | **Mejora de la interacción** — Optimizar iconos y detalles de interacción |
| 🔜 | **Mejores memorias** — Integrar una gestión de memoria más potente |
| 🔜 | **Integración LightRAG** — Integrar [LightRAG](https://github.com/HKUDS/LightRAG) como motor avanzado de bases de conocimiento |
| 🔜 | **Sitio de documentación** — Documentación completa con guías, referencia de API y tutoriales |

> Si DeepTutor te resulta útil, [danos una estrella](https://github.com/HKUDS/DeepTutor/stargazers): ¡nos ayuda a seguir!

---

<a id="community"></a>
## 🌐 Comunidad y ecosistema

| Proyecto | Papel |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | Motor ligero de TutorBot |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG e indexación |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| RAG rápido | Agentes sin código | Investigación automática | Agente ultraligero |

## 🤝 Contribuir

<div align="center">

Esperamos que DeepTutor sea un regalo para la comunidad. 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>
</div>

Consulta [CONTRIBUTING.md](../../CONTRIBUTING.md).

## ⭐ Historial de estrellas

<div align="center">
<a href="https://www.star-history.com/#HKUDS/DeepTutor&type=timeline&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
    <img alt="Star History" src="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
  </picture>
</a>
</div>

<p align="center">
 <a href="https://www.star-history.com/hkuds/deeptutor">
  <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/badge?repo=HKUDS/DeepTutor&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/badge?repo=HKUDS/DeepTutor" />
   <img alt="Star History Rank" src="https://api.star-history.com/badge?repo=HKUDS/DeepTutor" />
  </picture>
 </a>
</p>

<div align="center">

**[Data Intelligence Lab @ HKU](https://github.com/HKUDS)**

[⭐ Star](https://github.com/HKUDS/DeepTutor/stargazers) · [🐛 Issues](https://github.com/HKUDS/DeepTutor/issues) · [💬 Discussions](https://github.com/HKUDS/DeepTutor/discussions)

---

[Licencia Apache 2.0](../../LICENSE)

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.DeepTutor&style=for-the-badge&color=00d4ff" alt="Views">
</p>

</div>
