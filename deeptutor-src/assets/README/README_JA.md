<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: エージェントネイティブなパーソナライズドチュータリング

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[主な機能](#key-features) · [はじめる](#get-started) · [DeepTutor を探る](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [ロードマップ](#roadmap) · [コミュニティ](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md) · [🇹🇭 ภาษาไทย](README_TH.md)

</div>

---
### 📦 リリース

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — Schema 駆動の Channels タブとシークレットマスク、RAG を単一パイプラインへ集約、RAG/KB の整合性強化、チャットプロンプトの外部化、タイ語 README。

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — 全ケイパビリティ対応のユニバーサル「今すぐ回答」、Co-Writer のスクロール同期、ノートブック保存時のメッセージ選択、統一設定パネル、ストリーミング Stop ボタン、TutorBot 設定の原子的書き込み。

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — LaTeX ブロック数式パースの刷新、`agents.yaml` 経由の LLM 診断プローブ、追加ヘッダ転送の修正、SaveToNotebook の UUID 修正、Docker とローカル LLM のガイダンス。

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — URL ベースのブックマーク可能セッション、Snow テーマ、WebSocket ハートビートと自動再接続、ChatComposer の性能改善、埋め込みプロバイダレジストリの刷新、Serper 検索プロバイダ。

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — ブックマークとカテゴリ付きクイズノートブック、Visualize での Mermaid、埋め込み不一致検出、Qwen/vLLM 互換、LM Studio と llama.cpp 対応、Glass テーマ。

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — 検索の整理と SearXNG フォールバック、プロバイダ切替の修正、フロントエンドのリソースリーク修正。

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Visualize ケイパビリティ（Chart.js/SVG）、クイズ重複防止、o4-mini モデル対応。

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — 埋め込み進捗とレート制限時のリトライ、クロスプラットフォーム依存関係の修正、MIME 検証の修正。

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — ネイティブ OpenAI/Anthropic SDK（litellm 廃止）、Windows での Math Animator、堅牢な JSON パース、中国語 i18n の完備。

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — ホットリロード可能な設定、MinerU のネスト出力、WebSocket 修正、最低 Python 3.11+。

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — エージェントネイティブ架構の全面書き換え（約 20 万行）：Tools + Capabilities プラグインモデル、CLI と SDK、TutorBot、Co-Writer、ガイド付き学習、永続メモリ。

<details>
<summary><b>過去のリリース</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — セッション永続化、増分アップロード、柔軟な RAG パイプライン、中国語ローカライズ。

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling 対応、ログ改善、バグ修正。

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — 統一サービス設定、KB ごとの RAG 選択、問題生成刷新、サイドバー。

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — マルチプロバイダ LLM/埋め込み、新ホーム、RAG 分離、環境変数整理。

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager、CI/CD、GHCR イメージ。

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker、Next.js 16 / React 19、WebSocket 強化、脆弱性修正。

</details>

### 📰 ニュース

> **[2026.4.4]** お久しぶりです！✨ DeepTutor v1.0.0 がついに登場 — Apache-2.0 のもと、ゼロからの架構書き直し、TutorBot、柔軟なモード切替を備えたエージェントネイティブな進化です。新章の始まりです！

> **[2026.2.6]** 🚀 わずか 39 日で 10k スターに到達。コミュニティに感謝します！

> **[2026.1.1]** 新年あけましておめでとうございます。[Discord](https://discord.gg/eRsjPgMU4t)、[WeChat](https://github.com/HKUDS/DeepTutor/issues/78)、[Discussions](https://github.com/HKUDS/DeepTutor/discussions) で一緒に未来を作りましょう。

> **[2025.12.29]** DeepTutor を正式リリースしました。

<a id="key-features"></a>
## ✨ 主な機能

- **統一チャットワークスペース** — 5 モードを 1 スレッドで。チャット、Deep Solve、クイズ、Deep Research、Math Animator が同じ文脈を共有。
- **パーソナル TutorBot** — チャットボットではなく自律チューター。独立ワークスペース、記憶、人格、スキル。[nanobot](https://github.com/HKUDS/nanobot) 搭載。
- **AI Co-Writer** — Markdown で AI が第一級の共同編集者。書き換え・拡張・短縮、KB と Web を参照。
- **ガイド付き学習** — 資料を段階的・視覚的な学習ジャーニーへ。
- **ナレッジハブ** — PDF / MD / テキストで RAG 対応 KB、カラー付きノートブックで整理。
- **永続メモリ** — 学習の要約と学習者プロファイル。全機能と TutorBot で共有。
- **エージェントネイティブ CLI** — 能力・KB・セッション・TutorBot をコマンド一つで。Rich と JSON。ルートの [`SKILL.md`](../../SKILL.md) をエージェントに渡せば自律操作。

---

<a id="get-started"></a>
## 🚀 はじめる

### 前提条件

次のツールが入っていることを確認してください。

| 要件 | バージョン | 確認 | メモ |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | 任意 | `git --version` | クローン用 |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | バックエンド |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` | フロント構築（CLI のみ / Docker の場合は不要） |
| [npm](https://www.npmjs.com/) | 9+ | `npm --version` | Node に同梱されることが多い |

少なくとも 1 つの LLM プロバイダの **API キー**（例：[OpenAI](https://platform.openai.com/api-keys)、[DeepSeek](https://platform.deepseek.com/)、[Anthropic](https://console.anthropic.com/)）が必要です。セットアップツアーで入力と接続テストを案内します。

### オプション A — セットアップツアー（推奨）

**1 本の対話スクリプト**で依存関係のインストール、環境設定、接続テスト、起動まで案内します。手動で `.env` を編集する必要はほぼありません。

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Python 仮想環境（いずれか）：
conda create -n deeptutor python=3.11 && conda activate deeptutor   # Anaconda / Miniconda 利用時
python -m venv .venv && source .venv/bin/activate                    # それ以外（macOS / Linux）
python -m venv .venv && .venv\Scripts\activate                       # それ以外（Windows）

python scripts/start_tour.py
```

ツアーでは利用方法を尋ねます。

- **Web モード**（推奨）— すべての依存（pip + npm）をインストールし、一時サーバを立ち上げてブラウザの **設定** を開きます。LLM・Embedding・検索プロバイダを 4 ステップで設定し、ライブ接続テストが可能です。完了後、設定に応じて DeepTutor が自動再起動します。
- **CLI モード** — シェル内だけで、プロファイル選択から依存インストール、プロバイダ設定、検証、適用まで完結します。

いずれも [http://localhost:3782](http://localhost:3782) で利用できます。

> **日次の起動** — ツアーは初回だけで構いません。以降は次で起動してください。
>
> ```bash
> python scripts/start_web.py
> ```
>
> バックエンドとフロントエンドをまとめて起動し、ブラウザを自動で開きます。プロバイダの再設定や依存の再インストールが必要なときだけ `start_tour.py` を再実行してください。

<a id="option-b-manual"></a>
### オプション B — 手動ローカルインストール

細部まで自分で制御したい場合は、次の手順でインストール・設定します。

**1. 依存関係**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# 仮想環境の作成・有効化（オプション A と同じ）
conda create -n deeptutor python=3.11 && conda activate deeptutor

# DeepTutor（バックエンド + Web サーバー用依存）
pip install -e ".[server]"

# フロントエンド（Node.js 18+ が必要）
cd web && npm install && cd ..
```

**2. 環境**

```bash
cp .env.example .env
```

`.env` に最低限を記入：

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
<summary><b>対応 LLM プロバイダ</b></summary>

| プロバイダ | Binding | 既定 Base URL |
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
<summary><b>対応 Embedding プロバイダ</b></summary>

| プロバイダ | Binding | モデル例 | 既定次元 |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | デプロイ名 | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | 任意の埋め込みモデル | — |
| OpenAI 互換 | `custom` | — | — |

OpenAI 互換プロバイダ（DashScope、SiliconFlow など）は `custom` または `openai` binding で利用できます。

</details>

<details>
<summary><b>対応 Web 検索プロバイダ</b></summary>

| プロバイダ | 環境変数 | メモ |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | 推奨、無料枠あり |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | 自ホスト、API キー不要 |
| DuckDuckGo | — | API キー不要 |
| Perplexity | `PERPLEXITY_API_KEY` | API キー必須 |

</details>

**3. サービス起動**

最短で起動するには：

```bash
python scripts/start_web.py
```

バックエンドとフロントエンドをまとめて起動し、ブラウザを自動で開きます。

別ターミナルで手動起動する場合：

```bash
# バックエンド（FastAPI）
python -m deeptutor.api.run_server

# フロントエンド（Next.js）— 別ターミナル
cd web && npm run dev -- -p 3782
```

| サービス | 既定ポート |
|:---:|:---:|
| バックエンド | `8001` |
| フロントエンド | `3782` |

[http://localhost:3782](http://localhost:3782) を開きます。

### オプション C — Docker

Docker でバックエンドとフロントエンドを 1 つのコンテナにまとめられます。ローカルに Python や Node.js は不要です。[Docker Desktop](https://www.docker.com/products/docker-desktop/)（Linux では Docker Engine + Compose）があれば十分です。

**1. 環境変数**（下記 2a / 2b のどちらでも必要）

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

`.env` に少なくとも必須項目を記入します（[オプション B](#option-b-manual)と同じ）。

**2a. 公式イメージの取得（推奨）**

リリースごとに [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) へ `linux/amd64` と `linux/arm64` 向けイメージが公開されます。

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

バージョンを固定するには `docker-compose.ghcr.yml` のイメージタグを編集します。

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # または :latest
```

**2b. ソースからビルド**

```bash
docker compose up -d
```

`Dockerfile` からローカルビルドしてコンテナを起動します。

**3. 確認と運用**

コンテナが healthy になったら [http://localhost:3782](http://localhost:3782) を開きます。

```bash
docker compose logs -f   # ログを tail
docker compose down       # 停止してコンテナを削除
```

<details>
<summary><b>クラウド / リモートサーバー</b></summary>

リモートにデプロイする場合、ブラウザがバックエンド API の公開 URL を知る必要があります。`.env` に次を追加します。

```dotenv
# バックエンドに到達できる公開 URL
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

フロントエンド起動スクリプトが実行時にこの値を適用します。再ビルドは不要です。

</details>

<details>
<summary><b>開発モード（ホットリロード）</b></summary>

開発用オーバーレイでソースをマウントし、両サービスのホットリロードを有効にします。

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

`deeptutor/`、`deeptutor_cli/`、`scripts/`、`web/` の変更がすぐ反映されます。

</details>

<details>
<summary><b>カスタムポート</b></summary>

`.env` で既定ポートを上書きします。

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

その後再起動します。

```bash
docker compose up -d     # または docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>データ永続化</b></summary>

ユーザーデータとナレッジベースは Docker ボリュームでローカルディレクトリにマップされます。

| コンテナ内パス | ホストパス | 内容 |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | 設定、メモリ、ワークスペース、セッション、ログ |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | アップロード済みドキュメントとベクトルインデックス |

`docker compose down` 後もこれらのディレクトリは残り、次回 `up` で再利用されます。

</details>

<details>
<summary><b>環境変数リファレンス</b></summary>

| 変数 | 必須 | 説明 |
|:---|:---:|:---|
| `LLM_BINDING` | **はい** | LLM プロバイダ（`openai`、`anthropic` など） |
| `LLM_MODEL` | **はい** | モデル名（例：`gpt-4o`） |
| `LLM_API_KEY` | **はい** | LLM の API キー |
| `LLM_HOST` | **はい** | API の URL |
| `EMBEDDING_BINDING` | **はい** | 埋め込みプロバイダ |
| `EMBEDDING_MODEL` | **はい** | 埋め込みモデル名 |
| `EMBEDDING_API_KEY` | **はい** | 埋め込み API キー |
| `EMBEDDING_HOST` | **はい** | 埋め込みエンドポイント |
| `EMBEDDING_DIMENSION` | **はい** | ベクトル次元 |
| `SEARCH_PROVIDER` | いいえ | 検索（`tavily`、`jina`、`serper`、`perplexity` など） |
| `SEARCH_API_KEY` | いいえ | 検索 API キー |
| `BACKEND_PORT` | いいえ | バックエンドポート（既定 `8001`） |
| `FRONTEND_PORT` | いいえ | フロントエンドポート（既定 `3782`） |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | いいえ | クラウド向け公開バックエンド URL |
| `DISABLE_SSL_VERIFY` | いいえ | SSL 検証を無効化（既定 `false`） |

</details>

### オプション D — CLI のみ

Web フロントエンドなしで CLI だけ使う場合：

```bash
pip install -e ".[cli]"
```

LLM プロバイダの設定は依然として必要です。最短手順：

```bash
cp .env.example .env   # 編集して API キーなどを記入
```

設定後：

```bash
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> 詳細は [DeepTutor CLI](#deeptutor-cli-guide)。

---

<a id="explore-deeptutor"></a>
## 📖 DeepTutor を探る

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="DeepTutor アーキテクチャ" width="800">
</div>

### 💬 チャット — 統一インテリジェントワークスペース

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="チャット" width="800">
</div>

**統一コンテキスト**で 5 モードが共存。履歴・KB・参照はモード間で保持。

| モード | 役割 |
|:---|:---|
| **チャット** | RAG、検索、コード実行、深い推論、ブレスト、論文検索を組み合わせ。 |
| **Deep Solve** | 計画・調査・解答・検証と引用。 |
| **クイズ生成** | KB に根ざした評価と検証。 |
| **Deep Research** | サブトピック分解と並列調査、引用付きレポート。 |
| **Math Animator** | Manim による可視化。 |

ツールは**ワークフローから分離** — モードごとに有効化を選択。

### ✍️ Co-Writer — エディタ内の AI

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

フル Markdown エディタで AI が共同編集。**書き換え / 拡張 / 短縮**、KB や Web を参照。ノートブックへ保存可能。

### 🎓 ガイド付き学習

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="ガイド付き学習" width="800">
</div>

1. **学習計画** — 3〜5 の段階的知識点。  
2. **インタラクティブページ** — HTML で図解と例。  
3. **文脈 QA** — 各ステップでチャット。  
4. **まとめ** — 完了時にサマリ。

### 📚 ナレッジ管理

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="ナレッジ" width="800">
</div>

- **ナレッジベース** — PDF / TXT / MD、増分追加。  
- **ノートブック** — セッション横断で色分け整理。

### 🧠 メモリ

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="メモリ" width="800">
</div>

- **サマリ** — 学習の流れ。  
- **プロファイル** — 嗜好・レベル・目標・文体。TutorBot と共有。

---

<a id="tutorbot"></a>
### 🦞 TutorBot — 永続的で自律的な AI チューター

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="TutorBot アーキテクチャ" width="800">
</div>

[nanobot](https://github.com/HKUDS/nanobot) ベースの**マルチインスタンス**自律エージェント。各インスタンスは独立ループ・ワークスペース・記憶・人格。

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Soul テンプレート** — 人格と教育哲学。  
- **独立ワークスペース** — メモリ・セッション・スキル。共有 KB 層にもアクセス。  
- **プロアクティブ Heartbeat** — 定期リマインダとタスク。  
- **フルツール** — RAG、コード、Web、論文、推論、ブレスト。  
- **スキル学習** — ワークスペースにスキルファイルを追加。  
- **マルチチャネル** — Telegram、Discord、Slack、Feishu、企業微信、DingTalk、メール 等。  
- **チーム / サブエージェント** — 長時間タスク向け。

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI アーキテクチャ" width="800">
</div>

ブラウザ不要で能力・KB・セッション・メモリ・TutorBot を操作。Rich と JSON。[`SKILL.md`](../../SKILL.md) をツール利用エージェントに渡すと自律設定・操作。

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# REPL 内: /cap、/tool、/kb、/history、/notebook、/config などで切替
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
<summary><b>CLI コマンドリファレンス（全コマンド）</b></summary>

**トップレベル**

| コマンド | 説明 |
|:---|:---|
| `deeptutor run <capability> <message>` | 単発で能力を実行（`chat`、`deep_solve`、`deep_question`、`deep_research`、`math_animator`） |
| `deeptutor chat` | 対話 REPL（`--capability`、`--tool`、`--kb`、`--language` など） |
| `deeptutor serve` | DeepTutor API サーバを起動 |

**`deeptutor bot`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor bot list` | TutorBot 一覧 |
| `deeptutor bot create <id>` | 新規作成・起動（`--name`、`--persona`、`--model`） |
| `deeptutor bot start <id>` | 起動 |
| `deeptutor bot stop <id>` | 停止 |

**`deeptutor kb`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor kb list` | ナレッジベース一覧 |
| `deeptutor kb info <name>` | 詳細 |
| `deeptutor kb create <name>` | ドキュメントから作成（`--doc`、`--docs-dir`） |
| `deeptutor kb add <name>` | ドキュメントを追加 |
| `deeptutor kb search <name> <query>` | 検索 |
| `deeptutor kb set-default <name>` | デフォルト KB に設定 |
| `deeptutor kb delete <name>` | 削除（`--force`） |

**`deeptutor memory`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor memory show [file]` | 表示（`summary`、`profile`、`all`） |
| `deeptutor memory clear [file]` | クリア（`--force`） |

**`deeptutor session`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor session list` | 一覧（`--limit`） |
| `deeptutor session show <id>` | メッセージ表示 |
| `deeptutor session open <id>` | REPL で再開 |
| `deeptutor session rename <id>` | 名前変更（`--title`） |
| `deeptutor session delete <id>` | 削除 |

**`deeptutor notebook`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor notebook list` | 一覧 |
| `deeptutor notebook create <name>` | 作成（`--description`） |
| `deeptutor notebook show <id>` | レコード表示 |
| `deeptutor notebook add-md <id> <path>` | Markdown をインポート |
| `deeptutor notebook replace-md <id> <rec> <path>` | レコードを置換 |
| `deeptutor notebook remove-record <id> <rec>` | レコード削除 |

**`deeptutor config` / `plugin` / `provider`**

| コマンド | 説明 |
|:---|:---|
| `deeptutor config show` | 設定サマリを表示 |
| `deeptutor plugin list` | 登録済みツールと能力 |
| `deeptutor plugin info <name>` | ツールまたは能力の詳細 |
| `deeptutor provider login <provider>` | OAuth ログイン（`openai-codex`、`github-copilot`） |

</details>

<a id="roadmap"></a>
## 🗺️ ロードマップ

| 状態 | マイルストーン |
|:---:|:---|
| 🎯 | **認証とログイン** — 公開向けデプロイ用の任意ログインとマルチユーザー |
| 🎯 | **テーマと外観** — 多彩なテーマと UI のカスタマイズ |
| 🎯 | **インタラクション改善** — アイコン設計と操作感の磨き込み |
| 🔜 | **より良いメモリ** — メモリ管理の強化 |
| 🔜 | **LightRAG 統合** — [LightRAG](https://github.com/HKUDS/LightRAG) を高度な KB エンジンとして統合 |
| 🔜 | **ドキュメントサイト** — ガイド、API リファレンス、チュートリアルを含む公式ドキュメント |

> DeepTutor が役に立ったら [Star を付ける](https://github.com/HKUDS/DeepTutor/stargazers) と開発の励みになります！

---

<a id="community"></a>
## 🌐 コミュニティとエコシステム

| プロジェクト | 役割 |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | TutorBot の軽量エンジン |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG とインデックス |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| 高速 RAG | ノーコードエージェント | 自動研究 | 超軽量エージェント |

## 🤝 コントリビューション

<div align="center">

DeepTutor がコミュニティへの贈り物になれば幸いです。🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>

</div>

[CONTRIBUTING.md](../../CONTRIBUTING.md) を参照。

## ⭐ Star 履歴

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
