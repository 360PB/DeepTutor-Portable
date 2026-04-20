<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: tutoria personalizada nativa para agentes

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[Recursos](#key-features) · [Começar](#get-started) · [Explorar](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [Roteiro](#roadmap) · [Comunidade](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md) · [🇹🇭 ภาษาไทย](README_TH.md)

</div>

---
### 📦 Lançamentos

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — Aba Channels orientada por schema com mascaramento de segredos; RAG unificado em um único pipeline; reforço de consistência RAG/KB; prompts de chat externalizados; README em tailandês.

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — «Responder agora» universal em todas as capacidades; sincronização de rolagem no Co-Writer; seleção de mensagens ao salvar no caderno; painel de configurações unificado; botão Stop em streaming; gravação atômica da configuração do TutorBot.

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — Reformulação do parsing de LaTeX em bloco; sonda de diagnóstico LLM via `agents.yaml`; correção do encaminhamento de cabeçalhos extras; correção de UUID no SaveToNotebook; guia Docker + LLM local.

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — Sessões com URL marcável; tema Snow; heartbeat WebSocket e reconexão automática; desempenho do ChatComposer; reformulação do registro de provedores de embeddings; provedor de busca Serper.

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — Caderno de questões com favoritos e categorias; Mermaid no Visualize; detecção de incompatibilidade de embeddings; compatibilidade Qwen/vLLM; suporte LM Studio e llama.cpp; tema Glass.

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — Consolidação de busca com fallback SearXNG; correção da troca de provedor; vazamentos de recursos no frontend.

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Capacidade Visualize (Chart.js/SVG); prevenção de duplicatas em questionários; suporte ao modelo o4-mini.

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — Acompanhamento de embeddings com nova tentativa sob limite de taxa; dependências multiplataforma; validação MIME.

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — SDK nativo OpenAI/Anthropic (sem litellm); Math Animator no Windows; parsing JSON mais robusto; i18n chinês completo.

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — Recarga a quente de configurações; saída aninhada MinerU; correção WebSocket; mínimo Python 3.11+.

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — Reescrita nativa de agentes (~200k linhas): plugins Tools + Capabilities, CLI e SDK, TutorBot, Co-Writer, aprendizado guiado e memória persistente.

<details>
<summary><b>Lançamentos anteriores</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — Persistência de sessão, upload incremental, RAG flexível, localização em chinês.

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, logs, correções.

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — Config unificada, RAG por KB, geração de questões, barra lateral.

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — Multi-provedor LLM/embeddings, nova home, desacoplamento RAG, variáveis de ambiente.

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, imagens GHCR.

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 e React 19, WebSocket, vulnerabilidades.

</details>

### 📰 Notícias

> **[2026.4.4]** Há quanto tempo! ✨ DeepTutor v1.0.0 chegou — evolução nativa de agentes com reescrita da arquitetura do zero, TutorBot e modos flexíveis sob Apache-2.0. Um novo capítulo começa!

> **[2026.2.6]** 🚀 10k estrelas em 39 dias — obrigado à comunidade!

> **[2026.1.1]** Feliz Ano Novo! Junte-se ao [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78) ou [Discussions](https://github.com/HKUDS/DeepTutor/discussions).

> **[2025.12.29]** DeepTutor é lançado oficialmente.

<a id="key-features"></a>
## ✨ Principais recursos

- **Workspace de chat unificado** — Cinco modos, um fio: Chat, Deep Solve, quiz, Deep Research e Math Animator compartilham contexto.
- **TutorBots pessoais** — Não são chatbots: tutores autônomos com espaço de trabalho, memória, personalidade e habilidades. [nanobot](https://github.com/HKUDS/nanobot).
- **AI Co-Writer** — Markdown com IA como colaborador: reescrever, expandir ou encurtar com KB e web.
- **Aprendizado guiado** — Jornadas visuais passo a passo a partir dos seus materiais.
- **Hub de conhecimento** — PDF, Markdown e texto para bases RAG; cadernos coloridos.
- **Memória persistente** — Resumo de progresso e perfil do aprendiz; compartilhado com TutorBots.
- **CLI nativo para agentes** — Capacidades, KB, sessões e TutorBot em um comando; Rich e JSON. [`SKILL.md`](../../SKILL.md).

---

<a id="get-started"></a>
## 🚀 Começar

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

| Requisito | Versão | Verificar | Notas |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | Qualquer | `git --version` | Para clonar o repositório |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | Backend |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` | Build do frontend (não necessário só CLI ou Docker) |
| [npm](https://www.npmjs.com/) | 9+ | `npm --version` | Geralmente vem com o Node.js |

Você também precisa de uma **chave API** de pelo menos um provedor LLM (por exemplo [OpenAI](https://platform.openai.com/api-keys), [DeepSeek](https://platform.deepseek.com/), [Anthropic](https://console.anthropic.com/)). O tour guiado ajuda a inseri-la e testar a conexão.

### Opção A — Tour de configuração (recomendado)

Um **único script interativo** cobre instalação de dependências, configuração do ambiente, teste de conexão em tempo real e inicialização. Quase não é preciso editar `.env` manualmente.

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Ambiente virtual Python (escolha um):
conda create -n deeptutor python=3.11 && conda activate deeptutor   # se usar Anaconda/Miniconda
python -m venv .venv && source .venv/bin/activate                    # caso contrário (macOS/Linux)
python -m venv .venv && .venv\Scripts\activate                       # caso contrário (Windows)

python scripts/start_tour.py
```

O tour pergunta como deseja usar o DeepTutor:

- **Modo web** (recomendado) — Instala todas as dependências (pip + npm), sobe um servidor temporário e abre **Configurações** no navegador; quatro passos para LLM, embeddings e busca com teste de conexão em tempo real; ao terminar, o DeepTutor reinicia automaticamente com sua configuração.
- **Modo CLI** — Fluxo totalmente interativo no terminal: perfil, instalação, provedores, verificação e aplicação sem sair do shell.

Em ambos os casos você terá o DeepTutor em [http://localhost:3782](http://localhost:3782).

> **Início diário** — O tour só é necessário uma vez. Depois disso, inicie com:
>
> ```bash
> python scripts/start_web.py
> ```
>
> Inicia backend e frontend em um único comando e abre o navegador. Execute `start_tour.py` novamente apenas se precisar reconfigurar provedores ou reinstalar dependências.

<a id="option-b-manual"></a>
### Opção B — Instalação local manual

Se preferir controle total, instale e configure tudo manualmente.

**1. Instalar dependências**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Criar e ativar ambiente virtual (igual à opção A)
conda create -n deeptutor python=3.11 && conda activate deeptutor

# DeepTutor com dependências de backend + servidor web
pip install -e ".[server]"

# Frontend (requer Node.js 18+)
cd web && npm install && cd ..
```

**2. Configurar ambiente**

```bash
cp .env.example .env
```

Edite `.env` e preencha pelo menos os campos obrigatórios:

```dotenv
# LLM (obrigatório)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# Embeddings (obrigatório para a base de conhecimento)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
EMBEDDING_HOST=https://api.openai.com/v1
EMBEDDING_DIMENSION=3072
```

<details>
<summary><b>Provedores LLM suportados</b></summary>

| Provedor | Binding | URL base padrão |
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
<summary><b>Provedores de embedding suportados</b></summary>

| Provedor | Binding | Exemplo de modelo | Dimensão padrão |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | nome do deployment | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | Qualquer modelo de embedding | — |
| Compatível OpenAI | `custom` | — | — |

Provedores compatíveis com OpenAI (DashScope, SiliconFlow, etc.) funcionam com o binding `custom` ou `openai`.

</details>

<details>
<summary><b>Provedores de busca web suportados</b></summary>

| Provedor | Variável de ambiente | Notas |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | Recomendado, há nível gratuito |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Auto-hospedado, sem chave API |
| DuckDuckGo | — | Sem chave API |
| Perplexity | `PERPLEXITY_API_KEY` | Requer chave API |

</details>

**3. Iniciar serviços**

A forma mais rápida:

```bash
python scripts/start_web.py
```

Inicia backend e frontend e abre o navegador automaticamente.

Ou inicie cada serviço manualmente em terminais separados:

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — outro terminal
cd web && npm run dev -- -p 3782
```

| Serviço | Porta padrão |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

Abra [http://localhost:3782](http://localhost:3782).

### Opção C — Docker

O Docker empacota backend e frontend em um único contêiner; não é necessário Python ou Node.js locais. Basta [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ou Docker Engine + Compose no Linux).

**1. Variáveis de ambiente** (necessárias nas duas variantes abaixo)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

Edite `.env` e preencha pelo menos os campos obrigatórios (como na [opção B](#option-b-manual)).

**2a. Puxar imagem oficial (recomendado)**

As imagens oficiais são publicadas no [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) a cada release, para `linux/amd64` e `linux/arm64`.

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

Para fixar uma versão, edite a tag da imagem em `docker-compose.ghcr.yml`:

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # ou :latest
```

**2b. Build a partir do código-fonte**

```bash
docker compose up -d
```

Constrói a imagem localmente a partir do `Dockerfile` e inicia o contêiner.

**3. Verificar e gerenciar**

Abra [http://localhost:3782](http://localhost:3782) quando o contêiner estiver healthy.

```bash
docker compose logs -f   # acompanhar logs
docker compose down       # parar e remover o contêiner
```

<details>
<summary><b>Nuvem / servidor remoto</b></summary>

Em um servidor remoto, o navegador precisa da URL pública da API backend. Adicione em `.env`:

```dotenv
# URL pública onde o backend é acessível
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

O script de inicialização do frontend aplica esse valor em tempo de execução — não é necessário rebuild.

</details>

<details>
<summary><b>Modo desenvolvimento (hot-reload)</b></summary>

Sobreponha o override de desenvolvimento para montar o código-fonte e habilitar hot-reload em ambos os serviços:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Alterações em `deeptutor/`, `deeptutor_cli/`, `scripts/` e `web/` refletem-se imediatamente.

</details>

<details>
<summary><b>Portas personalizadas</b></summary>

Substitua as portas padrão em `.env`:

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

Depois reinicie:

```bash
docker compose up -d     # ou docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>Persistência de dados</b></summary>

Dados do usuário e bases de conhecimento persistem via volumes Docker mapeados para diretórios locais:

| Caminho no contêiner | Caminho no host | Conteúdo |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Configurações, memória, workspace, sessões, logs |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | Documentos enviados e índices vetoriais |

Esses diretórios permanecem após `docker compose down` e são reutilizados no próximo `docker compose up`.

</details>

<details>
<summary><b>Referência de variáveis de ambiente</b></summary>

| Variável | Obrigatório | Descrição |
|:---|:---:|:---|
| `LLM_BINDING` | **Sim** | Provedor LLM (`openai`, `anthropic`, etc.) |
| `LLM_MODEL` | **Sim** | Nome do modelo (ex.: `gpt-4o`) |
| `LLM_API_KEY` | **Sim** | Chave API do LLM |
| `LLM_HOST` | **Sim** | URL do endpoint |
| `EMBEDDING_BINDING` | **Sim** | Provedor de embeddings |
| `EMBEDDING_MODEL` | **Sim** | Nome do modelo de embedding |
| `EMBEDDING_API_KEY` | **Sim** | Chave API de embeddings |
| `EMBEDDING_HOST` | **Sim** | Endpoint de embeddings |
| `EMBEDDING_DIMENSION` | **Sim** | Dimensão do vetor |
| `SEARCH_PROVIDER` | Não | Busca (`tavily`, `jina`, `serper`, `perplexity`, etc.) |
| `SEARCH_API_KEY` | Não | Chave API de busca |
| `BACKEND_PORT` | Não | Porta backend (padrão `8001`) |
| `FRONTEND_PORT` | Não | Porta frontend (padrão `3782`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | Não | URL pública do backend para nuvem |
| `DISABLE_SSL_VERIFY` | Não | Desativar verificação SSL (padrão `false`) |

</details>

### Opção D — Apenas CLI

Se quiser apenas a CLI sem o frontend web:

```bash
pip install -e ".[cli]"
```

Ainda é necessário configurar o provedor LLM. O caminho mais rápido:

```bash
cp .env.example .env   # depois edite .env com suas chaves API
```

Após configurar:

```bash
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> Guia completo: [DeepTutor CLI](#deeptutor-cli-guide).

---

<a id="explore-deeptutor"></a>
## 📖 Explorar o DeepTutor

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="Arquitetura DeepTutor" width="800">
</div>

### 💬 Chat — Workspace inteligente unificado

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="Chat" width="800">
</div>

Cinco modos com **contexto unificado**.

| Modo | Função |
|:---|:---|
| **Chat** | RAG, web, código, raciocínio, brainstorming, papers. |
| **Deep Solve** | Multiagente com citações. |
| **Geração de quiz** | Avaliações na KB. |
| **Deep Research** | Subtópicos, agentes paralelos, relatório citado. |
| **Math Animator** | Manim. |

Ferramentas **desacopladas dos fluxos**.

### ✍️ Co-Writer — IA no editor

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

**Reescrever**, **Expandir**, **Encurtar**; desfazer/refazer; cadernos.

### 🎓 Aprendizado guiado

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="Guiado" width="800">
</div>

1. Plano (3–5 pontos).  
2. Páginas interativas.  
3. P&R contextuais.  
4. Resumo.

### 📚 Gestão do conhecimento

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="Conhecimento" width="800">
</div>

- **Bases de conhecimento** — PDF, TXT, MD.  
- **Cadernos** — Cores e sessões.

### 🧠 Memória

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="Memória" width="800">
</div>

- **Resumo** — Progresso.  
- **Perfil** — Preferências, nível, metas. Compartilhado com TutorBots.

---

<a id="tutorbot"></a>
### 🦞 TutorBot — Tutores de IA persistentes e autônomos

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="Arquitetura TutorBot" width="800">
</div>

Agente **multi-instância** persistente com [nanobot](https://github.com/HKUDS/nanobot).

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Modelos Soul** — Personalidade e pedagogia.  
- **Workspace independente** — Memória, sessões, habilidades; camada compartilhada.  
- **Heartbeat proativo** — Lembretes e tarefas.  
- **Ferramentas completas** — RAG, código, web, papers, raciocínio, brainstorming.  
- **Habilidades** — Arquivos skill.  
- **Multicanal** — Telegram, Discord, Slack, Feishu, WeCom, DingTalk, e-mail, etc.  
- **Equipes e subagentes**.

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI — Interface nativa para agentes

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI" width="800">
</div>

Sem navegador: capacidades, KB, sessões, memória, TutorBot. Rich + JSON. [`SKILL.md`](../../SKILL.md).

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# No REPL: /cap, /tool, /kb, /history, /notebook, /config para alternar em tempo real
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
<summary><b>Referência completa da CLI</b></summary>

**Nível superior**

| Comando | Descrição |
|:---|:---|
| `deeptutor run <capability> <message>` | Executa uma capacidade em um turno (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | REPL interativo com `--capability`, `--tool`, `--kb`, `--language`, etc. |
| `deeptutor serve` | Inicia o servidor API do DeepTutor |

**`deeptutor bot`**

| Comando | Descrição |
|:---|:---|
| `deeptutor bot list` | Lista instâncias do TutorBot |
| `deeptutor bot create <id>` | Cria e inicia um bot (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | Inicia um bot |
| `deeptutor bot stop <id>` | Para um bot |

**`deeptutor kb`**

| Comando | Descrição |
|:---|:---|
| `deeptutor kb list` | Lista bases de conhecimento |
| `deeptutor kb info <name>` | Detalhes da base |
| `deeptutor kb create <name>` | Cria a partir de documentos (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | Adiciona documentos |
| `deeptutor kb search <name> <query>` | Busca na base |
| `deeptutor kb set-default <name>` | Define KB padrão |
| `deeptutor kb delete <name>` | Remove (`--force`) |

**`deeptutor memory`**

| Comando | Descrição |
|:---|:---|
| `deeptutor memory show [file]` | Ver (`summary`, `profile`, `all`) |
| `deeptutor memory clear [file]` | Limpar (`--force`) |

**`deeptutor session`**

| Comando | Descrição |
|:---|:---|
| `deeptutor session list` | Lista sessões (`--limit`) |
| `deeptutor session show <id>` | Mensagens da sessão |
| `deeptutor session open <id>` | Retomar no REPL |
| `deeptutor session rename <id>` | Renomear (`--title`) |
| `deeptutor session delete <id>` | Excluir |

**`deeptutor notebook`**

| Comando | Descrição |
|:---|:---|
| `deeptutor notebook list` | Lista cadernos |
| `deeptutor notebook create <name>` | Criar (`--description`) |
| `deeptutor notebook show <id>` | Registros |
| `deeptutor notebook add-md <id> <path>` | Importar Markdown |
| `deeptutor notebook replace-md <id> <rec> <path>` | Substituir registro |
| `deeptutor notebook remove-record <id> <rec>` | Remover registro |

**`deeptutor config` / `plugin` / `provider`**

| Comando | Descrição |
|:---|:---|
| `deeptutor config show` | Resumo da configuração |
| `deeptutor plugin list` | Ferramentas e capacidades registradas |
| `deeptutor plugin info <name>` | Detalhe de ferramenta ou capacidade |
| `deeptutor provider login <provider>` | OAuth (`openai-codex`, `github-copilot`) |

</details>

<a id="roadmap"></a>
## 🗺️ Roteiro

| Status | Marco |
|:---:|:---|
| 🎯 | **Autenticação e login** — Página de login opcional para implantações públicas com multiusuário |
| 🎯 | **Temas e aparência** — Mais temas e personalização da interface |
| 🎯 | **Melhoria de interação** — Refinar ícones e detalhes de interação |
| 🔜 | **Memórias melhores** — Integrar gestão de memória mais robusta |
| 🔜 | **Integração LightRAG** — Integrar [LightRAG](https://github.com/HKUDS/LightRAG) como motor avançado de bases de conhecimento |
| 🔜 | **Site de documentação** — Documentação completa com guias, referência de API e tutoriais |

> Se o DeepTutor for útil para você, [dê uma estrela](https://github.com/HKUDS/DeepTutor/stargazers) — isso nos ajuda a continuar!

---

<a id="community"></a>
## 🌐 Comunidade e ecossistema

| Projeto | Papel |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | Motor do TutorBot |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| RAG rápido | Agentes sem código | Pesquisa automática | Agente ultraleve |

## 🤝 Contribuir

<div align="center">

Esperamos que o DeepTutor seja um presente para a comunidade. 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>
</div>

Veja [CONTRIBUTING.md](../../CONTRIBUTING.md).

## ⭐ Histórico de estrelas

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

[Apache License 2.0](../../LICENSE)

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.DeepTutor&style=for-the-badge&color=00d4ff" alt="Views">
</p>

</div>
