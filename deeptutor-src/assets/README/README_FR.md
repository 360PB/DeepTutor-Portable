<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor : tutorat personnalisé natif pour agents

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[Fonctionnalités](#key-features) · [Démarrage](#get-started) · [Explorer](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [Feuille de route](#roadmap) · [Communauté](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md) · [🇹🇭 ภาษาไทย](README_TH.md)

</div>

---
### 📦 Versions

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — Onglet Channels piloté par schéma et masquage des secrets ; RAG fusionné en un seul pipeline ; renforcement de la cohérence RAG/KB ; prompts de chat externalisés ; README en thaï.

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — « Répondre maintenant » universel sur toutes les capacités ; synchronisation du défilement Co-Writer ; sélection des messages pour l’enregistrement dans le carnet ; panneau de paramètres unifié ; bouton Stop en streaming ; écriture atomique de la configuration TutorBot.

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — Refonte du parsing LaTeX en blocs ; sonde de diagnostic LLM via `agents.yaml` ; correctif de transfert d’en-têtes supplémentaires ; correctif UUID SaveToNotebook ; guide Docker + LLM local.

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — Sessions signets par URL ; thème Snow ; battement WebSocket et reconnexion auto ; perf ChatComposer ; refonte du registre des fournisseurs d’embeddings ; fournisseur de recherche Serper.

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — Carnet de questions avec favoris et catégories ; Mermaid dans Visualize ; détection d’incohérence d’embeddings ; compatibilité Qwen/vLLM ; prise en charge LM Studio et llama.cpp ; thème Glass.

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — Consolidation de la recherche avec repli SearXNG ; correctif de changement de fournisseur ; fuites de ressources côté frontend.

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Capacité Visualize (Chart.js/SVG) ; prévention des doublons de quiz ; prise en charge du modèle o4-mini.

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — Suivi de progression des embeddings avec nouvelles tentatives sous limitation de débit ; dépendances multiplateforme ; validation MIME.

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — SDK natifs OpenAI/Anthropic (sans litellm) ; Math Animator sous Windows ; analyse JSON plus robuste ; i18n chinois complet.

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — Rechargement à chaud des réglages ; sortie imbriquée MinerU ; correctif WebSocket ; Python 3.11+ minimum.

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — Réécriture native agents (~200k lignes) : modèle de plugins Tools + Capabilities, CLI et SDK, TutorBot, Co-Writer, apprentissage guidé et mémoire persistante.

<details>
<summary><b>Versions précédentes</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — Persistance de session, import incrémental, RAG flexible, localisation chinoise complète.

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, journaux, correctifs.

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — Config unifiée, RAG par KB, génération de questions, barre latérale.

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — Multi-fournisseurs LLM/embeddings, nouvelle page d’accueil, découplage RAG, variables d’environnement.

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, images GHCR.

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 et React 19, WebSocket, vulnérabilités.

</details>

### 📰 Actualités

> **[2026.4.4]** Ça faisait longtemps ! ✨ DeepTutor v1.0.0 est enfin là — évolution native agents : refonte complète de l’architecture, TutorBot et modes flexibles sous Apache-2.0. Un nouveau chapitre commence !

> **[2026.2.6]** 🚀 10k étoiles en 39 jours — merci à la communauté !

> **[2026.1.1]** Bonne année ! Rejoignez [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78) ou [Discussions](https://github.com/HKUDS/DeepTutor/discussions).

> **[2025.12.29]** DeepTutor est officiellement publié.

<a id="key-features"></a>
## ✨ Points clés

- **Espace de chat unifié** — Cinq modes, un fil : Chat, Deep Solve, quiz, Deep Research, Math Animator partagent le contexte.
- **TutorBots personnels** — Pas des chatbots : tuteurs autonomes, espace de travail, mémoire, personnalité, compétences. [nanobot](https://github.com/HKUDS/nanobot).
- **AI Co-Writer** — Markdown : réécrire, développer, raccourcir avec KB et web.
- **Apprentissage guidé** — Parcours visuels par étapes à partir de vos documents.
- **Hub de connaissances** — PDF, Markdown, texte pour des bases RAG ; carnets colorés.
- **Mémoire persistante** — Synthèse de progression et profil d’apprenant ; partagé avec les TutorBots.
- **CLI natif agents** — Capacités, KB, sessions, TutorBot en une commande ; Rich et JSON. [`SKILL.md`](../../SKILL.md) pour les agents.

---

<a id="get-started"></a>
## 🚀 Démarrage

### Prérequis

Avant de commencer, installez les éléments suivants :

| Prérequis | Version | Vérifier | Notes |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | Toute | `git --version` | Pour cloner le dépôt |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | Backend |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` | Build frontend (inutile en CLI seul ou Docker) |
| [npm](https://www.npmjs.com/) | 9+ | `npm --version` | Souvent fourni avec Node.js |

Vous avez aussi besoin d’une **clé API** d’au moins un fournisseur LLM (ex. [OpenAI](https://platform.openai.com/api-keys), [DeepSeek](https://platform.deepseek.com/), [Anthropic](https://console.anthropic.com/)). La visite guidée vous aide à la saisir et à tester la connexion.

### Option A — Visite guidée (recommandé)

Un **script interactif unique** couvre l’installation des dépendances, la configuration, les tests de connexion en direct et le lancement. Peu ou pas d’édition manuelle du `.env`.

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Environnement virtuel Python (au choix) :
conda create -n deeptutor python=3.11 && conda activate deeptutor   # Anaconda / Miniconda
python -m venv .venv && source .venv/bin/activate                    # sinon (macOS / Linux)
python -m venv .venv && .venv\Scripts\activate                       # sinon (Windows)

python scripts/start_tour.py
```

La visite demande comment vous souhaitez utiliser DeepTutor :

- **Mode web** (recommandé) — Installe toutes les dépendances (pip + npm), démarre un serveur temporaire et ouvre la page **Paramètres** dans le navigateur. Un parcours en quatre étapes configure LLM, embeddings et recherche avec test de connexion en direct. À la fin, DeepTutor redémarre automatiquement avec votre configuration.
- **Mode CLI** — Flux entièrement interactif dans le terminal : profil, installation, fournisseurs, vérification et application sans quitter le shell.

Dans les deux cas, vous aboutissez à [http://localhost:3782](http://localhost:3782).

> **Lancement quotidien** — La visite n’est nécessaire qu’une fois. Ensuite, démarrez avec :
>
> ```bash
> python scripts/start_web.py
> ```
>
> Lance backend et frontend en une commande et ouvre le navigateur. Relancez `start_tour.py` seulement pour reconfigurer les fournisseurs ou réinstaller les dépendances.

<a id="option-b-manual"></a>
### Option B — Installation locale manuelle

Si vous préférez tout contrôler vous-même, installez et configurez manuellement.

**1. Installer les dépendances**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Créer et activer l’environnement virtuel (comme l’option A)
conda create -n deeptutor python=3.11 && conda activate deeptutor

# DeepTutor avec dépendances backend + serveur web
pip install -e ".[server]"

# Frontend (Node.js 18+ requis)
cd web && npm install && cd ..
```

**2. Configurer l’environnement**

```bash
cp .env.example .env
```

Modifiez `.env` et renseignez au minimum les champs obligatoires :

```dotenv
# LLM (obligatoire)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# Embeddings (obligatoire pour la base de connaissances)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
EMBEDDING_HOST=https://api.openai.com/v1
EMBEDDING_DIMENSION=3072
```

<details>
<summary><b>Fournisseurs LLM pris en charge</b></summary>

| Fournisseur | Binding | URL de base par défaut |
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
<summary><b>Fournisseurs d’embeddings pris en charge</b></summary>

| Fournisseur | Binding | Exemple de modèle | Dimension par défaut |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | nom du déploiement | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | Tout modèle d’embedding | — |
| Compatible OpenAI | `custom` | — | — |

Les fournisseurs compatibles OpenAI (DashScope, SiliconFlow, etc.) fonctionnent via le binding `custom` ou `openai`.

</details>

<details>
<summary><b>Fournisseurs de recherche web pris en charge</b></summary>

| Fournisseur | Clé d’environnement | Notes |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | Recommandé, palier gratuit disponible |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Auto-hébergé, pas de clé API |
| DuckDuckGo | — | Pas de clé API |
| Perplexity | `PERPLEXITY_API_KEY` | Nécessite une clé API |

</details>

**3. Démarrer les services**

Le moyen le plus rapide :

```bash
python scripts/start_web.py
```

Démarre backend et frontend et ouvre le navigateur automatiquement.

Vous pouvez aussi lancer chaque service manuellement dans des terminaux séparés :

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — autre terminal
cd web && npm run dev -- -p 3782
```

| Service | Port par défaut |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

Ouvrez [http://localhost:3782](http://localhost:3782).

### Option C — Docker

Docker regroupe backend et frontend dans un seul conteneur ; Python et Node.js locaux ne sont pas requis. Il suffit de [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ou Docker Engine + Compose sous Linux).

**1. Variables d’environnement** (requis pour les deux variantes ci-dessous)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

Modifiez `.env` et renseignez au minimum les champs obligatoires (comme pour l’[option B](#option-b-manual)).

**2a. Tirer l’image officielle (recommandé)**

Les images officielles sont publiées sur [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) à chaque release, pour `linux/amd64` et `linux/arm64`.

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

Pour épingler une version, modifiez la balise d’image dans `docker-compose.ghcr.yml` :

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # ou :latest
```

**2b. Build depuis les sources**

```bash
docker compose up -d
```

Construit l’image localement depuis le `Dockerfile` et démarre le conteneur.

**3. Vérifier et gérer**

Ouvrez [http://localhost:3782](http://localhost:3782) lorsque le conteneur est healthy.

```bash
docker compose logs -f   # suivre les logs
docker compose down       # arrêter et supprimer le conteneur
```

<details>
<summary><b>Déploiement cloud / serveur distant</b></summary>

Sur un serveur distant, le navigateur doit connaître l’URL publique de l’API backend. Ajoutez dans `.env` :

```dotenv
# URL publique où le backend est joignable
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

Le script de démarrage du frontend applique cette valeur à l’exécution — pas besoin de rebuild.

</details>

<details>
<summary><b>Mode développement (rechargement à chaud)</b></summary>

Superposez l’override de développement pour monter le code source et activer le rechargement à chaud des deux services :

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Les modifications dans `deeptutor/`, `deeptutor_cli/`, `scripts/` et `web/` sont reflétées immédiatement.

</details>

<details>
<summary><b>Ports personnalisés</b></summary>

Surchargez les ports par défaut dans `.env` :

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

Puis redémarrez :

```bash
docker compose up -d     # ou docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>Persistance des données</b></summary>

Les données utilisateur et les bases de connaissances persistent via des volumes Docker mappés sur des répertoires locaux :

| Chemin conteneur | Chemin hôte | Contenu |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Réglages, mémoire, espace de travail, sessions, journaux |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | Documents téléchargés et index vectoriels |

Ces répertoires survivent à `docker compose down` et sont réutilisés au prochain `docker compose up`.

</details>

<details>
<summary><b>Référence des variables d’environnement</b></summary>

| Variable | Obligatoire | Description |
|:---|:---:|:---|
| `LLM_BINDING` | **Oui** | Fournisseur LLM (`openai`, `anthropic`, etc.) |
| `LLM_MODEL` | **Oui** | Nom du modèle (ex. `gpt-4o`) |
| `LLM_API_KEY` | **Oui** | Clé API LLM |
| `LLM_HOST` | **Oui** | URL de l’endpoint |
| `EMBEDDING_BINDING` | **Oui** | Fournisseur d’embeddings |
| `EMBEDDING_MODEL` | **Oui** | Nom du modèle d’embedding |
| `EMBEDDING_API_KEY` | **Oui** | Clé API embeddings |
| `EMBEDDING_HOST` | **Oui** | Endpoint embeddings |
| `EMBEDDING_DIMENSION` | **Oui** | Dimension du vecteur |
| `SEARCH_PROVIDER` | Non | Recherche (`tavily`, `jina`, `serper`, `perplexity`, etc.) |
| `SEARCH_API_KEY` | Non | Clé API de recherche |
| `BACKEND_PORT` | Non | Port backend (défaut `8001`) |
| `FRONTEND_PORT` | Non | Port frontend (défaut `3782`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | Non | URL publique du backend pour le cloud |
| `DISABLE_SSL_VERIFY` | Non | Désactiver la vérification SSL (défaut `false`) |

</details>

### Option D — CLI uniquement

Si vous voulez uniquement la CLI sans le frontend web :

```bash
pip install -e ".[cli]"
```

Vous devez toujours configurer le fournisseur LLM. Le plus rapide :

```bash
cp .env.example .env   # puis éditez .env avec vos clés API
```

Une fois configuré :

```bash
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> Guide complet : [DeepTutor CLI](#deeptutor-cli-guide).

---

<a id="explore-deeptutor"></a>
## 📖 Explorer DeepTutor

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="Architecture DeepTutor" width="800">
</div>

### 💬 Chat — Espace intelligent unifié

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="Chat" width="800">
</div>

Cinq modes, **contexte unifié**.

| Mode | Rôle |
|:---|:---|
| **Chat** | RAG, web, code, raisonnement, brainstorming, articles. |
| **Deep Solve** | Multi-agents avec citations. |
| **Génération de quiz** | Évaluations ancrées à la KB. |
| **Deep Research** | Sous-sujets, agents parallèles, rapport cité. |
| **Math Animator** | Manim. |

Les outils sont **découplés des flux** — vous choisissez ce qui est actif.

### ✍️ Co-Writer — IA dans l’éditeur

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

**Réécrire**, **Développer**, **Raccourcir** ; annuler/refaire ; carnets.

### 🎓 Apprentissage guidé

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="Guidé" width="800">
</div>

1. Plan (3–5 points).  
2. Pages interactives.  
3. Q&R contextuelles.  
4. Synthèse.

### 📚 Gestion des connaissances

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="Connaissances" width="800">
</div>

- **Bases de connaissances** — PDF, TXT, MD.  
- **Carnets** — Couleurs et sessions.

### 🧠 Mémoire

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="Mémoire" width="800">
</div>

- **Synthèse** — Progression.  
- **Profil** — Préférences, niveau, objectifs. Partagé avec TutorBots.

---

<a id="tutorbot"></a>
### 🦞 TutorBot — Tuteurs IA persistants et autonomes

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="Architecture TutorBot" width="800">
</div>

Agent **multi-instance** persistant sur [nanobot](https://github.com/HKUDS/nanobot) : boucle, espace, mémoire, personnalité propres.

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Modèles Soul** — Personnalité et pédagogie.  
- **Espace indépendant** — Mémoire, sessions, compétences ; couche partagée DeepTutor.  
- **Heartbeat proactif** — Rappels et tâches.  
- **Outils complets** — RAG, code, web, papers, raisonnement, brainstorming.  
- **Compétences** — Fichiers skill.  
- **Multicanal** — Telegram, Discord, Slack, Feishu, WeCom, DingTalk, e-mail, etc.  
- **Équipes et sous-agents**.

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI — Interface native pour agents

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI" width="800">
</div>

Sans navigateur : capacités, KB, sessions, mémoire, TutorBot. Rich + JSON. [`SKILL.md`](../../SKILL.md).

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# Dans le REPL : /cap, /tool, /kb, /history, /notebook, /config pour changer à la volée
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
<summary><b>Référence complète de la CLI</b></summary>

**Niveau racine**

| Commande | Description |
|:---|:---|
| `deeptutor run <capability> <message>` | Exécute une capacité en un tour (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | REPL interactif avec `--capability`, `--tool`, `--kb`, `--language`, etc. |
| `deeptutor serve` | Démarre le serveur API DeepTutor |

**`deeptutor bot`**

| Commande | Description |
|:---|:---|
| `deeptutor bot list` | Liste les instances TutorBot |
| `deeptutor bot create <id>` | Crée et démarre un bot (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | Démarre un bot |
| `deeptutor bot stop <id>` | Arrête un bot |

**`deeptutor kb`**

| Commande | Description |
|:---|:---|
| `deeptutor kb list` | Liste les bases de connaissances |
| `deeptutor kb info <name>` | Détails d’une base |
| `deeptutor kb create <name>` | Crée à partir de documents (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | Ajoute des documents |
| `deeptutor kb search <name> <query>` | Recherche dans la base |
| `deeptutor kb set-default <name>` | Définit la KB par défaut |
| `deeptutor kb delete <name>` | Supprime (`--force`) |

**`deeptutor memory`**

| Commande | Description |
|:---|:---|
| `deeptutor memory show [file]` | Afficher (`summary`, `profile`, `all`) |
| `deeptutor memory clear [file]` | Effacer (`--force`) |

**`deeptutor session`**

| Commande | Description |
|:---|:---|
| `deeptutor session list` | Liste des sessions (`--limit`) |
| `deeptutor session show <id>` | Messages de la session |
| `deeptutor session open <id>` | Reprendre dans le REPL |
| `deeptutor session rename <id>` | Renommer (`--title`) |
| `deeptutor session delete <id>` | Supprimer |

**`deeptutor notebook`**

| Commande | Description |
|:---|:---|
| `deeptutor notebook list` | Liste des carnets |
| `deeptutor notebook create <name>` | Créer (`--description`) |
| `deeptutor notebook show <id>` | Voir les enregistrements |
| `deeptutor notebook add-md <id> <path>` | Importer du Markdown |
| `deeptutor notebook replace-md <id> <rec> <path>` | Remplacer un enregistrement |
| `deeptutor notebook remove-record <id> <rec>` | Supprimer un enregistrement |

**`deeptutor config` / `plugin` / `provider`**

| Commande | Description |
|:---|:---|
| `deeptutor config show` | Résumé de la configuration |
| `deeptutor plugin list` | Outils et capacités enregistrés |
| `deeptutor plugin info <name>` | Détail d’un outil ou d’une capacité |
| `deeptutor provider login <provider>` | Connexion OAuth (`openai-codex`, `github-copilot`) |

</details>

<a id="roadmap"></a>
## 🗺️ Feuille de route

| Statut | Jalons |
|:---:|:---|
| 🎯 | **Authentification et connexion** — Page de login optionnelle pour déploiements publics et multi-utilisateurs |
| 🎯 | **Thèmes et apparence** — Thèmes variés et personnalisation de l’interface |
| 🎯 | **Amélioration de l’interaction** — Optimiser les icônes et les détails d’interaction |
| 🔜 | **Mémoires améliorées** — Intégrer une meilleure gestion de la mémoire |
| 🔜 | **Intégration LightRAG** — Intégrer [LightRAG](https://github.com/HKUDS/LightRAG) comme moteur avancé de bases de connaissances |
| 🔜 | **Site de documentation** — Documentation complète : guides, référence API et tutoriels |

> Si DeepTutor vous est utile, [donnez-nous une étoile](https://github.com/HKUDS/DeepTutor/stargazers) — cela nous aide à continuer !

---

<a id="community"></a>
## 🌐 Communauté et écosystème

| Projet | Rôle |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | Moteur TutorBot |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| RAG rapide | Agents sans code | Recherche auto | Agent léger |

## 🤝 Contribuer

<div align="center">

Nous espérons que DeepTutor sera un cadeau pour la communauté. 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>
</div>

Voir [CONTRIBUTING.md](../../CONTRIBUTING.md).

## ⭐ Historique des étoiles

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

[Licence Apache 2.0](../../LICENSE)

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.DeepTutor&style=for-the-badge&color=00d4ff" alt="Views">
</p>

</div>
