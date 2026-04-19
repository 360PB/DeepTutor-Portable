<div align="center">

<img src="../logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: ผู้ช่วยติวส่วนบุคคลแบบ Agent-Native

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[คุณสมบัติเด่น](#-คุณสมบัติเด่น) · [เริ่มต้นใช้งาน](#-เริ่มต้นใช้งาน) · [สำรวจความสามารถ](#-สำรวจ-deeptutor) · [TutorBot](#-tutorbot--ติวเตอร์-ai-แบบถาวรและอัตโนมัติ) · [CLI](#%EF%B8%8F-deeptutor-cli--อินเทอร์เฟซแบบ-agent-native) · [ชุมชน](#-ชุมชนและระบบนิเวศ)

[🇺🇸 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md)

</div>

---

### 📦 ประวัติการเผยแพร่

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — ปุ่ม "ตอบเลย" ข้ามการ reasoning ได้ทุก capability, Co-Writer ปรับขนาด split + scroll sync ตามบรรทัด, บันทึกข้อความลง Notebook แบบเลือก message, ระบบ Notebook จริงครอบคลุม Knowledge/Guide/Save, แผงตั้งค่ารวมแบบพับได้, ปุ่ม Stop รอบการ streaming, refactor TutorBot config manager แบบ atomic write, ปรับ Light/Snow theme ใหม่ และขยาย test suite

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — ปรับปรุงการ parse LaTeX block math, ตั้งค่า LLM probe ผ่าน agents.yaml, forward extra headers ใน LLM factory, แก้ UUID ของ SaveToNotebookModal, คำแนะนำ Docker + local LLM และขยาย test suite

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — URL-based chat routing พร้อม bookmark ได้, ธีม Snow, WebSocket heartbeat & auto-reconnect พร้อม resume, ปรับ ChatComposer ให้เร็วขึ้น, overhaul embedding provider registry, Serper search provider, streaming idle timeout และขยาย test suite

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — Question Notebook สำหรับทบทวนแบบทดสอบรวมศูนย์พร้อม bookmark & หมวดหมู่, รองรับ Mermaid diagram ใน Visualize, ตรวจจับ embedding model ไม่ตรง, รวม system message สำหรับ Qwen/vLLM, รองรับ LM Studio & llama.cpp และธีม Glass

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — ปรับโครงสร้าง search consolidation ให้ง่ายขึ้นพร้อม SearXNG fallback, แก้ไข provider switch fix, ตั้ง runtime config ชัดเจนใน test runner และแก้ resource leak ฝั่ง frontend

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — เพิ่ม Visualize capability ใหม่พร้อม Chart.js/SVG rendering pipeline, ป้องกัน quiz ซ้ำด้วย generation history, รองรับ o4-mini model และปรับปรุง server logging

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — แสดงความคืบหน้า Embedding พร้อม retry เมื่อเจอ HTTP 429, จัดการ dependency ข้ามแพลตฟอร์มใน start tour และแก้ MIME validation ให้ case-insensitive

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — ลบ litellm dependency ใช้ native OpenAI/Anthropic SDK providers แทน, รองรับ Math Animator บน Windows, parse JSON จาก LLM ให้ robust ขึ้น, แก้ KaTeX & navigation ใน Guided Learning และ i18n ภาษาจีนครบ

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — ล้าง runtime cache สำหรับ hot settings reload, รองรับ MinerU nested output, แก้ mimic WebSocket, กำหนดขั้นต่ำ Python 3.11+ และปรับปรุง CI

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — เขียนสถาปัตยกรรมใหม่แบบ Agent-native (~200k บรรทัด) พร้อมโมเดลปลั๊กอิน 2 ชั้น (Tools + Capabilities), CLI & SDK entry points, TutorBot มัลติแชนแนล, Co-Writer, Guided Learning และ persistent memory

<details>
<summary><b>รุ่นเก่า</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — Session persistence, อัปโหลดเอกสารเพิ่มทีละไฟล์, import RAG pipeline ที่ยืดหยุ่น และ localization ภาษาจีนครบ

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — รองรับ Docling สำหรับ RAG-Anything, ปรับ logging system และแก้บั๊ก

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — Unified service configuration, เลือก RAG pipeline ต่อ knowledge base, ปรับ question generation ใหม่ และปรับแต่ง sidebar

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — รองรับ Multi-provider LLM & embedding, หน้า home ใหม่, แยก RAG module และ refactor environment variable

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — สถาปัตยกรรม PromptManager รวม, GitHub Actions CI/CD และ Docker image สำเร็จรูปบน GHCR

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker deployment, อัปเกรด Next.js 16 & React 19, WebSocket security hardening และแก้ช่องโหว่สำคัญ

</details>

### 📰 ข่าวสาร

> **[2026.4.4]** นานมาแล้ว ✨ DeepTutor v1.0.0 มาถึงแล้ว — วิวัฒนาการแบบ agent-native ที่เขียนสถาปัตยกรรมใหม่ตั้งแต่ต้น พร้อม TutorBot และการสลับโหมดอย่างยืดหยุ่น ภายใต้สัญญาอนุญาต Apache-2.0 บทใหม่เริ่มต้นขึ้น เรื่องราวของเรายังดำเนินต่อไป!

> **[2026.2.6]** 🚀 เราไปถึง 10,000 ดาวภายในเพียง 39 วัน! ขอบคุณชุมชนที่ยอดเยี่ยมของเราสำหรับการสนับสนุน!

> **[2026.1.1]** สวัสดีปีใหม่! มาร่วม [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78) หรือ [Discussions](https://github.com/HKUDS/DeepTutor/discussions) ของเรา — มาร่วมกำหนดอนาคตของ DeepTutor กัน!

> **[2025.12.29]** DeepTutor เปิดตัวอย่างเป็นทางการ!


## ✨ คุณสมบัติเด่น

- **พื้นที่แชตแบบรวมศูนย์** — 5 โหมดอยู่ในเธรดเดียว ได้แก่ Chat, Deep Solve, Quiz Generation, Deep Research และ Math Animator โดยใช้บริบทร่วมกันทั้งหมด คุณสามารถเริ่มจากถามคำถามทั่วไป ต่อไปยังการแก้ปัญหาแบบหลายเอเจนต์ สร้างแบบทดสอบ และเจาะลึกงานวิจัยได้โดยไม่เสียประวัติการสนทนา
- **TutorBot ส่วนตัว** — ไม่ใช่แค่ chatbot แต่เป็นติวเตอร์อัตโนมัติที่มี workspace, memory, บุคลิก และทักษะของตัวเอง แต่ละบอตสามารถเตือนความจำ เรียนรู้ความสามารถใหม่ และเติบโตไปพร้อมกับผู้ใช้ ขับเคลื่อนโดย [nanobot](https://github.com/HKUDS/nanobot)
- **AI Co-Writer** — ตัวแก้ไข Markdown ที่ให้ AI เป็นผู้ร่วมเขียนอย่างแท้จริง เลือกข้อความเพื่อ Rewrite, Expand หรือ Shorten ได้ พร้อมดึงบริบทจาก knowledge base และเว็บ ทุกชิ้นงานสามารถป้อนกลับเข้าระบบการเรียนของคุณ
- **Guided Learning** — เปลี่ยนเอกสารหรือโน้ตของคุณให้เป็นเส้นทางการเรียนรู้แบบเป็นขั้นตอน พร้อมหน้าเนื้อหาเชิงโต้ตอบ ภาพประกอบ และการถามตอบตามบริบท
- **Knowledge Hub** — อัปโหลด PDF, Markdown และไฟล์ข้อความเพื่อสร้าง knowledge base แบบ RAG-ready จัดระเบียบข้อมูลเชิงลึกข้ามเซสชันด้วยสมุดบันทึกที่ใส่สีได้ เอกสารของคุณไม่ได้แค่วางอยู่ — มันขับเคลื่อนทุกการสนทนา
- **Persistent Memory** — DeepTutor สร้างโปรไฟล์ผู้เรียนที่เติบโตอยู่ตลอดเวลา จากสิ่งที่คุณเรียน วิธีที่คุณเรียน และเป้าหมายของคุณ ใช้ร่วมกันข้ามทุกฟีเจอร์และทุก TutorBot ยิ่งใช้ยิ่งแม่นยำ
- **Agent-Native CLI** — ทุกความสามารถ, knowledge base, session และ TutorBot สามารถเรียกใช้ได้ผ่านคำสั่งเดียวในเทอร์มินัล พร้อมทั้งรองรับผลลัพธ์แบบสวยงามสำหรับมนุษย์และ JSON สำหรับ AI agent และ pipeline มอบ [`SKILL.md`](../../SKILL.md) ให้ agent ใดก็ได้ แล้วมันจะจัดการ DeepTutor ได้เอง

---

## 🚀 เริ่มต้นใช้งาน

### ตัวเลือก A — Setup Tour (แนะนำ)

**สคริปต์แบบโต้ตอบเพียงชุดเดียว** ที่จะพาคุณผ่านทุกขั้นตอน: ติดตั้ง dependency, ตั้งค่า environment, ทดสอบการเชื่อมต่อแบบเรียลไทม์ และเปิดระบบใช้งาน โดยแทบไม่ต้องแก้ `.env` ด้วยตนเอง

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# สร้าง Python environment
conda create -n deeptutor python=3.11 && conda activate deeptutor
# หรือ: python -m venv .venv && source .venv/bin/activate

# เริ่ม guided tour
python scripts/start_tour.py
```

Setup Tour จะถามว่าคุณต้องการใช้งาน DeepTutor แบบใด:

- **Web mode** (แนะนำ) — ช่วยเลือก dependency profile, ติดตั้งทั้งฝั่ง pip + npm, จากนั้นเปิดเซิร์ฟเวอร์ชั่วคราวและนำไปยังหน้า **Settings** ในเบราว์เซอร์ พร้อมทัวร์ 4 ขั้นตอนสำหรับตั้งค่า LLM, Embedding และ Search provider พร้อมทดสอบการเชื่อมต่อแบบเรียลไทม์ เมื่อเสร็จแล้ว DeepTutor จะรีสตาร์ทอัตโนมัติพร้อม config ของคุณ
- **CLI mode** — ตั้งค่าทุกอย่างในเทอร์มินัล ตั้งแต่เลือก dependency profile ไปจนถึงตรวจสอบการเชื่อมต่อและบันทึกการตั้งค่า

ไม่ว่าจะเลือกแบบไหน คุณจะเข้าใช้งานได้ที่ [http://localhost:3782](http://localhost:3782)

### ตัวเลือก B — ติดตั้งเองแบบ Local

หากคุณต้องการควบคุมทุกขั้นตอนด้วยตัวเอง ให้ติดตั้งและตั้งค่าตามนี้

**1. ติดตั้ง dependency**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

conda create -n deeptutor python=3.11 && conda activate deeptutor
pip install -e ".[server]"

# Frontend
cd web && npm install && cd ..
```

**2. ตั้งค่า environment**

```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env` และกรอกค่าที่จำเป็นอย่างน้อยดังนี้:

```dotenv
# LLM (จำเป็น)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# Embedding (จำเป็นสำหรับ Knowledge Base)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_API_KEY=sk-xxx
EMBEDDING_HOST=https://api.openai.com/v1
EMBEDDING_DIMENSION=3072
```

<details>
<summary><b>ผู้ให้บริการ LLM ที่รองรับ</b></summary>

| ผู้ให้บริการ | Binding | Base URL เริ่มต้น |
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
<summary><b>ผู้ให้บริการ Embedding ที่รองรับ</b></summary>

| ผู้ให้บริการ | Binding | ตัวอย่างโมเดล | Dimension เริ่มต้น |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | deployment name | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | โมเดล embedding ใดก็ได้ | — |
| OpenAI-compatible | `custom` | — | — |

ผู้ให้บริการที่เข้ากันได้กับ OpenAI (DashScope, SiliconFlow ฯลฯ) ใช้ผ่าน binding `custom` หรือ `openai` ได้

</details>

<details>
<summary><b>ผู้ให้บริการ Web Search ที่รองรับ</b></summary>

| ผู้ให้บริการ | Env Key | หมายเหตุ |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | แนะนำ, มี free tier |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | Self-hosted, ไม่ต้องใช้ API key |
| DuckDuckGo | — | ไม่ต้องใช้ API key |
| Perplexity | `PERPLEXITY_API_KEY` | ต้องใช้ API key |

</details>

**3. เริ่มบริการ**

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — เปิดอีกเทอร์มินัลหนึ่ง
cd web && npm run dev -- -p 3782
```

| Service | Port เริ่มต้น |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

เปิด [http://localhost:3782](http://localhost:3782) แล้วพร้อมใช้งาน

### ตัวเลือก C — ติดตั้งด้วย Docker

Docker ช่วยรวม backend และ frontend ไว้ในคอนเทนเนอร์เดียว จึงไม่จำเป็นต้องติดตั้ง Python หรือ Node.js บนเครื่องโดยตรง

**1. ตั้งค่า environment variable** (จำเป็นสำหรับทุกตัวเลือก)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

แก้ไข `.env` และกรอกค่าที่จำเป็น (เหมือน [ตัวเลือก B](#ตัวเลือก-b--ติดตั้งเองแบบ-local) ด้านบน)

**2a. ดึง image ทางการ (แนะนำ)**

Image ทางการเผยแพร่ที่ [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) ทุกครั้งที่ release สำหรับ `linux/amd64` และ `linux/arm64`

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

หากต้องการ pin เวอร์ชันเฉพาะ ให้แก้ image tag ใน `docker-compose.ghcr.yml`:

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # หรือ :latest
```

**2b. Build จาก source**

```bash
docker compose up -d
```

คำสั่งนี้จะ build image จาก `Dockerfile` และเริ่มคอนเทนเนอร์

**3. ตรวจสอบและจัดการ**

เปิด [http://localhost:3782](http://localhost:3782) เมื่อคอนเทนเนอร์พร้อมแล้ว

```bash
docker compose logs -f   # ดู log
docker compose down       # หยุดและลบคอนเทนเนอร์
```

<details>
<summary><b>Deploy บน Cloud / เซิร์ฟเวอร์ระยะไกล</b></summary>

เมื่อ deploy บนเซิร์ฟเวอร์ระยะไกล เบราว์เซอร์ต้องรู้ URL สาธารณะของ backend API เพิ่มตัวแปรอีกหนึ่งตัวใน `.env`:

```dotenv
# ตั้งเป็น URL สาธารณะที่สามารถเข้าถึง backend ได้
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

Frontend startup script จะใช้ค่านี้ตอน runtime — ไม่ต้อง rebuild

</details>

<details>
<summary><b>Development mode (hot-reload)</b></summary>

เพิ่ม dev override เพื่อ mount source code และเปิด hot-reload สำหรับทั้งสองบริการ:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

การเปลี่ยนแปลงใน `deeptutor/`, `deeptutor_cli/`, `scripts/` และ `web/` จะมีผลทันที

</details>

<details>
<summary><b>กำหนด Port เอง</b></summary>

แก้ไข port เริ่มต้นใน `.env`:

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

จากนั้นรีสตาร์ท:

```bash
docker compose up -d     # หรือ docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>การเก็บข้อมูลถาวร (Data persistence)</b></summary>

ข้อมูลผู้ใช้และ knowledge base เก็บผ่าน Docker volume ที่ map กับ directory ในเครื่อง:

| Container path | Host path | เนื้อหา |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | Settings, memory, workspace, sessions, logs |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | เอกสารที่อัปโหลด & vector indices |

Directory เหล่านี้จะอยู่หลังจาก `docker compose down` และถูกนำมาใช้ใหม่เมื่อ `docker compose up` ครั้งต่อไป

</details>

<details>
<summary><b>ตารางอ้างอิง Environment Variables</b></summary>

| ตัวแปร | จำเป็น | คำอธิบาย |
|:---|:---:|:---|
| `LLM_BINDING` | **ใช่** | ผู้ให้บริการ LLM (`openai`, `anthropic` ฯลฯ) |
| `LLM_MODEL` | **ใช่** | ชื่อโมเดล (เช่น `gpt-4o`) |
| `LLM_API_KEY` | **ใช่** | API key สำหรับ LLM |
| `LLM_HOST` | **ใช่** | URL endpoint ของ API |
| `EMBEDDING_BINDING` | **ใช่** | ผู้ให้บริการ Embedding |
| `EMBEDDING_MODEL` | **ใช่** | ชื่อ Embedding model |
| `EMBEDDING_API_KEY` | **ใช่** | API key สำหรับ Embedding |
| `EMBEDDING_HOST` | **ใช่** | Endpoint สำหรับ Embedding |
| `EMBEDDING_DIMENSION` | **ใช่** | มิติของ vector |
| `SEARCH_PROVIDER` | ไม่ | ผู้ให้บริการ Search (`tavily`, `jina`, `serper`, `perplexity` ฯลฯ) |
| `SEARCH_API_KEY` | ไม่ | API key สำหรับ Search |
| `BACKEND_PORT` | ไม่ | Port ฝั่ง backend (ค่าเริ่มต้น `8001`) |
| `FRONTEND_PORT` | ไม่ | Port ฝั่ง frontend (ค่าเริ่มต้น `3782`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | ไม่ | URL สาธารณะของ backend สำหรับ cloud deployment |
| `DISABLE_SSL_VERIFY` | ไม่ | ปิดการตรวจสอบ SSL (ค่าเริ่มต้น `false`) |

</details>

### ตัวเลือก D — ใช้เฉพาะ CLI

หากคุณต้องการเฉพาะ command-line interface โดยไม่ใช้เว็บ frontend:

```bash
pip install -e ".[cli]"
deeptutor chat                                   # Interactive REPL
deeptutor run chat "Explain Fourier transform"   # เรียกใช้ capability แบบ one-shot
deeptutor run deep_solve "Solve x^2 = 4"         # แก้ปัญหาแบบหลายเอเจนต์
deeptutor kb create my-kb --doc textbook.pdf     # สร้าง knowledge base
```

> ดูรายละเอียดเพิ่มเติมที่ [DeepTutor CLI](#%EF%B8%8F-deeptutor-cli--อินเทอร์เฟซแบบ-agent-native)

---

## 📖 สำรวจ DeepTutor

<div align="center">
<img src="../figs/deeptutor-architecture.png" alt="สถาปัตยกรรม DeepTutor" width="800">
</div>

### 💬 Chat — พื้นที่ทำงานอัจฉริยะแบบรวม

<div align="center">
<img src="../figs/dt-chat.png" alt="พื้นที่ Chat" width="800">
</div>

DeepTutor รวม 5 โหมดหลักไว้ใน workspace เดียว โดยใช้ **ระบบจัดการบริบทร่วมกัน** ทำให้ประวัติการสนทนา knowledge base และแหล่งอ้างอิงต่อเนื่องข้ามโหมดได้ — สลับไปมาได้อิสระในหัวข้อเดียวกัน

| โหมด | หน้าที่ |
|:---|:---|
| **Chat** | สนทนาแบบยืดหยุ่น พร้อมเปิดใช้ RAG, web search, code execution, deep reasoning, brainstorming และ paper search ได้ตามต้องการ |
| **Deep Solve** | แก้ปัญหาแบบหลายเอเจนต์ โดยวางแผน สืบค้น แก้โจทย์ และตรวจสอบ พร้อม citation อย่างเป็นระบบ |
| **Quiz Generation** | สร้างแบบทดสอบจาก knowledge base พร้อมตรวจสอบคุณภาพของคำถาม |
| **Deep Research** | แยกหัวข้อออกเป็นประเด็นย่อย ส่งเอเจนต์ค้นคว้าแบบขนานจาก RAG, เว็บ และงานวิชาการ แล้วสรุปเป็นรายงานที่มีอ้างอิง |
| **Math Animator** | เปลี่ยนแนวคิดคณิตศาสตร์ให้เป็นภาพเคลื่อนไหวและ storyboard ด้วย Manim |

เครื่องมือ **แยกอิสระจาก workflow** — ในทุกโหมด คุณเลือกได้ว่าจะเปิดเครื่องมือตัวไหน ใช้กี่ตัว หรือจะไม่ใช้เลย Workflow จัดการเรื่องการให้เหตุผล ส่วนเครื่องมือเป็นของคุณที่จะประกอบเข้าด้วยกัน

> เริ่มจากถามคำถามง่าย ๆ ยกระดับเป็น Deep Solve เมื่อยากขึ้น สร้างแบบทดสอบเพื่อตรวจสอบตัวเอง จากนั้นเปิด Deep Research เพื่อลงลึก — ทั้งหมดในเธรดเดียว

### ✍️ Co-Writer — ให้ AI อยู่ในตัวแก้ไขของคุณ

<div align="center">
<img src="../figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

Co-Writer นำความชาญฉลาดของ Chat มาใส่ในพื้นผิวการเขียนโดยตรง เป็น Markdown editor ที่ฝัง AI เป็นผู้ช่วยร่วมเขียน ไม่ใช่แค่แถบด้านข้าง

เลือกข้อความแล้วสั่ง **Rewrite**, **Expand** หรือ **Shorten** — สามารถดึงบริบทจาก knowledge base หรือเว็บมาช่วยได้ ระบบแก้ไขแบบไม่ทำลายของเดิมพร้อม undo/redo เต็มรูปแบบ และทุกชิ้นงานสามารถบันทึกลง notebook ได้

### 🎓 Guided Learning — เรียนรู้ทีละขั้นแบบมีภาพประกอบ

<div align="center">
<img src="../figs/dt-guide.png" alt="Guided Learning" width="800">
</div>

Guided Learning เปลี่ยนสื่อการเรียนของคุณให้กลายเป็นเส้นทางการเรียนรู้แบบหลายขั้นตอน ระบุหัวข้อ เชื่อมโยง notebook records แล้ว DeepTutor จะ:

1. **ออกแบบแผนการเรียนรู้** — ระบุ 3–5 ประเด็นความรู้แบบก้าวหน้าจากเอกสารของคุณ
2. **สร้างหน้าเชิงโต้ตอบ** — แต่ละประเด็นจะกลายเป็นหน้า HTML เชิงภาพพร้อมคำอธิบาย แผนภาพ และตัวอย่าง
3. **เปิดให้ถามตอบตามบริบท** — แชตคู่กับแต่ละขั้นเพื่อสำรวจเพิ่ม
4. **สรุปความก้าวหน้า** — เมื่อจบ จะได้รับสรุปการเรียนรู้ทั้งหมดของคุณ

เซสชันเป็นแบบ persistent — หยุด กลับมาทำต่อ หรือเข้าดูขั้นตอนใดก็ได้ทุกเมื่อ

### 📚 การจัดการความรู้ — โครงสร้างพื้นฐานการเรียนของคุณ

<div align="center">
<img src="../figs/dt-knowledge.png" alt="การจัดการความรู้" width="800">
</div>

ส่วน Knowledge ใช้สำหรับสร้างและจัดการคลังเอกสารที่ขับเคลื่อนทุกฟีเจอร์ใน DeepTutor

- **Knowledge Bases** — อัปโหลดไฟล์ PDF, TXT หรือ Markdown เพื่อสร้างคลังข้อมูลที่ค้นหาได้และพร้อมสำหรับ RAG เพิ่มเอกสารได้ทีละไฟล์ตามที่ห้องสมุดของคุณเติบโต
- **Notebooks** — จัดระเบียบบันทึกการเรียนรู้จาก Chat, Guided Learning, Co-Writer หรือ Deep Research ลงในสมุดบันทึกที่แบ่งหมวดหมู่และใส่สีได้

Knowledge base ของคุณไม่ใช่แค่ที่เก็บ — มันมีส่วนร่วมอย่างแข็งขันในทุกการสนทนา ทุกเซสชันวิจัย และทุกเส้นทางการเรียนรู้

### 🧠 Memory — DeepTutor เรียนรู้ไปพร้อมกับคุณ

<div align="center">
<img src="../figs/dt-memory.png" alt="Memory" width="800">
</div>

DeepTutor มี memory แบบถาวรที่เติบโตอยู่ตลอดเวลาผ่าน 2 มิติ:

- **Summary** — สรุปว่าคุณเรียนอะไรไปแล้ว สำรวจประเด็นใดบ้าง และความเข้าใจพัฒนาอย่างไร
- **Profile** — โปรไฟล์ผู้เรียน เช่น ระดับความรู้ เป้าหมาย สไตล์การสื่อสาร และความชอบ — ปรับปรุงอัตโนมัติผ่านทุกการโต้ตอบ

Memory นี้ถูกใช้ร่วมกันข้ามทุกฟีเจอร์และทุก TutorBot ยิ่งคุณใช้ DeepTutor มากเท่าไร มันก็ยิ่งตอบได้เฉพาะตัวและมีประสิทธิภาพมากขึ้น

---

### 🦞 TutorBot — ติวเตอร์ AI แบบถาวรและอัตโนมัติ

<div align="center">
<img src="../figs/tutorbot-architecture.png" alt="สถาปัตยกรรม TutorBot" width="800">
</div>

TutorBot ไม่ใช่ chatbot ธรรมดา แต่เป็น **เอเจนต์แบบถาวร หลายอินสแตนซ์** ที่ทำงานบน [nanobot](https://github.com/HKUDS/nanobot) โดยแต่ละ TutorBot รัน agent loop เป็นของตัวเองพร้อม workspace, memory และบุคลิกแยกจากกัน คุณสามารถสร้างติวเตอร์คณิตศาสตร์แบบโสเครติส, โค้ชการเขียนที่ใจเย็น หรือผู้ช่วยวิจัยที่เข้มงวดได้พร้อมกันหลายตัว แต่ละตัวเติบโตไปพร้อมกับคุณ

<div align="center">
<img src="../figs/tb.png" alt="TutorBot" width="800">
</div>

- **Soul Templates** — กำหนดบุคลิก โทนการสอน และปรัชญาการสอนผ่านไฟล์ Soul ที่แก้ไขได้ เลือกจาก archetype ในตัว (โสเครติส, ให้กำลังใจ, เข้มงวด) หรือออกแบบเอง — soul กำหนดทุกการตอบ
- **Independent Workspace** — แต่ละบอตมี directory ของตัวเองพร้อม memory, sessions, skills และ config แยกจากกัน — แยกตัวเต็มที่แต่ยังเข้าถึงชั้นความรู้ร่วมของ DeepTutor ได้
- **Proactive Heartbeat** — บอตไม่ใช่แค่ตอบ — มันริเริ่มเอง ระบบ Heartbeat ในตัวเปิดให้เช็กอินการเรียนซ้ำ เตือนทบทวน และจัดตารางงาน ติวเตอร์ของคุณมาหาแม้คุณไม่เริ่ม
- **Full Tool Access** — ทุกบอตเข้าถึงเครื่องมือครบชุดของ DeepTutor: RAG retrieval, code execution, web search, academic paper search, deep reasoning และ brainstorming
- **Skill Learning** — สอนบอตความสามารถใหม่โดยเพิ่มไฟล์ skill ลงใน workspace ของมัน เมื่อความต้องการของคุณเปลี่ยน ความสามารถของติวเตอร์ก็เปลี่ยนตาม
- **Multi-Channel Presence** — เชื่อมต่อกับ Telegram, Discord, Slack, Feishu, WeChat Work, DingTalk, Email และช่องทางอื่น ๆ ติวเตอร์ไปหาคุณไม่ว่าคุณจะอยู่ที่ไหน
- **Team & Sub-Agents** — สร้าง sub-agent ทำงานเบื้องหลังหรือจัด multi-agent team ภายในบอตเดียวสำหรับงานซับซ้อนและใช้เวลานาน

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list                  # ดูติวเตอร์ทั้งหมดที่กำลังทำงาน
```

---

### ⌨️ DeepTutor CLI — อินเทอร์เฟซแบบ Agent-Native

<div align="center">
<img src="../figs/cli-architecture.png" alt="สถาปัตยกรรม DeepTutor CLI" width="800">
</div>

DeepTutor รองรับ CLI อย่างเต็มรูปแบบ ทุก capability, knowledge base, session, memory และ TutorBot อยู่ห่างแค่คำสั่งเดียว — ไม่ต้องเปิดเบราว์เซอร์ CLI ให้บริการทั้งมนุษย์ (แสดงผลสวยงามในเทอร์มินัล) และ AI agent (ส่งออกเป็น JSON ที่มีโครงสร้าง)

มอบ [`SKILL.md`](../../SKILL.md) ที่ root ของโปรเจกต์ให้ agent ที่ใช้เครื่องมือ ([nanobot](https://github.com/HKUDS/nanobot) หรือ LLM ใดก็ตามที่มี tool access) แล้วมันจะตั้งค่าและใช้งาน DeepTutor ได้เอง

**One-shot execution** — เรียกใช้ capability ใดก็ได้จากเทอร์มินัล:

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

**Interactive REPL** — เซสชันแชตแบบถาวรพร้อมสลับโหมดขณะใช้งาน:

```bash
deeptutor chat --capability deep_solve --kb my-kb
# ภายใน REPL: /cap, /tool, /kb, /history, /notebook, /config เพื่อสลับขณะใช้งาน
```

**Knowledge base lifecycle** — สร้าง ค้นหา และจัดการคลัง RAG-ready ทั้งหมดจากเทอร์มินัล:

```bash
deeptutor kb create my-kb --doc textbook.pdf       # สร้างจากเอกสาร
deeptutor kb add my-kb --docs-dir ./papers/         # เพิ่มโฟลเดอร์เอกสาร
deeptutor kb search my-kb "gradient descent"        # ค้นหาโดยตรง
deeptutor kb set-default my-kb                      # ตั้งเป็น KB เริ่มต้น
```

**Dual output mode** — แสดงผลสวยงามสำหรับมนุษย์, JSON สำหรับ pipeline:

```bash
deeptutor run chat "Summarize chapter 3" -f rich    # แสดงผลสี สวยงาม
deeptutor run chat "Summarize chapter 3" -f json    # JSON events แบบ line-delimited
```

**Session continuity** — กลับมาทำต่อจากจุดที่ค้างไว้:

```bash
deeptutor session list                              # แสดงรายการเซสชัน
deeptutor session open <id>                         # กลับมาทำต่อใน REPL
```

<details>
<summary><b>ตารางอ้างอิงคำสั่ง CLI ทั้งหมด</b></summary>

**คำสั่งหลัก**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor run <capability> <message>` | เรียกใช้ capability แบบ single turn (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | Interactive REPL พร้อมตัวเลือก `--capability`, `--tool`, `--kb`, `--language` |
| `deeptutor serve` | เริ่ม DeepTutor API server |

**`deeptutor bot`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor bot list` | แสดงรายการ TutorBot ทั้งหมด |
| `deeptutor bot create <id>` | สร้างและเริ่มบอตใหม่ (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | เริ่มบอต |
| `deeptutor bot stop <id>` | หยุดบอต |

**`deeptutor kb`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor kb list` | แสดงรายการ knowledge base ทั้งหมด |
| `deeptutor kb info <name>` | แสดงรายละเอียด knowledge base |
| `deeptutor kb create <name>` | สร้างจากเอกสาร (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | เพิ่มเอกสารทีละไฟล์ |
| `deeptutor kb search <name> <query>` | ค้นหา knowledge base |
| `deeptutor kb set-default <name>` | ตั้งเป็น KB เริ่มต้น |
| `deeptutor kb delete <name>` | ลบ knowledge base (`--force`) |

**`deeptutor memory`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor memory show [file]` | ดู memory (`summary`, `profile` หรือ `all`) |
| `deeptutor memory clear [file]` | ล้าง memory (`--force`) |

**`deeptutor session`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor session list` | แสดงรายการเซสชัน (`--limit`) |
| `deeptutor session show <id>` | ดูข้อความในเซสชัน |
| `deeptutor session open <id>` | กลับมาทำต่อใน REPL |
| `deeptutor session rename <id>` | เปลี่ยนชื่อเซสชัน (`--title`) |
| `deeptutor session delete <id>` | ลบเซสชัน |

**`deeptutor notebook`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor notebook list` | แสดงรายการ notebook |
| `deeptutor notebook create <name>` | สร้าง notebook (`--description`) |
| `deeptutor notebook show <id>` | ดูบันทึกใน notebook |
| `deeptutor notebook add-md <id> <path>` | นำเข้า markdown เป็นบันทึก |
| `deeptutor notebook replace-md <id> <rec> <path>` | เปลี่ยนบันทึก markdown |
| `deeptutor notebook remove-record <id> <rec>` | ลบบันทึก |

**`deeptutor config` / `plugin` / `provider`**

| คำสั่ง | คำอธิบาย |
|:---|:---|
| `deeptutor config show` | แสดงสรุป configuration ปัจจุบัน |
| `deeptutor plugin list` | แสดงรายการ tools และ capabilities ที่ลงทะเบียน |
| `deeptutor plugin info <name>` | แสดงรายละเอียด tool หรือ capability |
| `deeptutor provider login <provider>` | ยืนยันตัวตน (`openai-codex` OAuth; `github-copilot` ตรวจสอบ Copilot auth ที่มีอยู่) |

</details>

## 🗺️ แผนงานในอนาคต

| สถานะ | หมุดหมาย |
|:---:|:---|
| 🎯 | **Authentication & Login** — รองรับหน้าเข้าสู่ระบบแบบเลือกใช้สำหรับการ deploy สาธารณะและผู้ใช้หลายคน |
| 🎯 | **Themes & Appearance** — ธีมและการปรับแต่งหน้าตา UI ที่หลากหลายขึ้น |
| 🎯 | **Interaction Improvement** — ปรับปรุง icon และรายละเอียดการโต้ตอบ |
| 🔜 | **Better Memories** — ยกระดับระบบจัดการ memory |
| 🔜 | **LightRAG Integration** — รวม [LightRAG](https://github.com/HKUDS/LightRAG) เป็น knowledge base engine ขั้นสูง |
| 🔜 | **Documentation Site** — เว็บไซต์เอกสารที่ครบถ้วนขึ้น ทั้งคู่มือ, API reference และ tutorial |

> หาก DeepTutor มีประโยชน์สำหรับคุณ [ฝากกดดาว](https://github.com/HKUDS/DeepTutor/stargazers) — มันช่วยให้เราพัฒนาต่อไปได้!

---

## 🌐 ชุมชนและระบบนิเวศ

DeepTutor สร้างขึ้นบนโครงการโอเพนซอร์สคุณภาพหลายตัว:

| โครงการ | บทบาทใน DeepTutor |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | เอนจินเอเจนต์น้ำหนักเบาที่ขับเคลื่อน TutorBot |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | แกนหลักสำหรับ RAG pipeline และการทำดัชนีเอกสาร |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | ระบบสร้างแอนิเมชันคณิตศาสตร์สำหรับ Math Animator |

**จาก ecosystem ของ HKUDS:**

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| Simple & Fast RAG | Zero-Code Agent Framework | Automated Research | Ultra-Lightweight AI Agent |


## 🤝 การมีส่วนร่วม

<div align="center">

เราหวังว่า DeepTutor จะเป็นของขวัญแก่ชุมชน 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>

</div>

อ่าน [CONTRIBUTING.md](../../CONTRIBUTING.md) สำหรับคำแนะนำเกี่ยวกับการตั้งค่าสภาพแวดล้อมสำหรับนักพัฒนา มาตรฐานโค้ด และขั้นตอนการส่ง pull request

## ⭐ ประวัติดาว

<div align="center">

<a href="https://www.star-history.com/#HKUDS/DeepTutor&type=timeline&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/DeepTutor&type=timeline&legend=top-left" />
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

[⭐ กดดาว](https://github.com/HKUDS/DeepTutor/stargazers) · [🐛 รายงานบั๊ก](https://github.com/HKUDS/DeepTutor/issues) · [💬 Discussions](https://github.com/HKUDS/DeepTutor/discussions)

---

เผยแพร่ภายใต้สัญญาอนุญาต [Apache License 2.0](../../LICENSE)

<p>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.DeepTutor&style=for-the-badge&color=00d4ff" alt="Views">
</p>

</div>
