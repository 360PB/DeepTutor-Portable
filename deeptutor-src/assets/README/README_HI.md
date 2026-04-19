<div align="center">

<img src="../../assets/logo-ver2.png" alt="DeepTutor" width="140" style="border-radius: 15px;">

# DeepTutor: एजेंट-नेटिव व्यक्तिगत शिक्षण

<a href="https://trendshift.io/repositories/17099" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17099" alt="HKUDS%2FDeepTutor | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](../../LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/HKUDS/DeepTutor?style=flat-square&color=brightgreen)](https://github.com/HKUDS/DeepTutor/releases)
[![arXiv](https://img.shields.io/badge/arXiv-Coming_Soon-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](#)

[![Discord](https://img.shields.io/badge/Discord-Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/eRsjPgMU4t)
[![Feishu](https://img.shields.io/badge/Feishu-Group-00D4AA?style=flat-square&logo=feishu&logoColor=white)](../../Communication.md)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?style=flat-square&logo=wechat&logoColor=white)](https://github.com/HKUDS/DeepTutor/issues/78)

[मुख्य विशेषताएँ](#key-features) · [शुरू करें](#get-started) · [अन्वेषण](#explore-deeptutor) · [TutorBot](#tutorbot) · [CLI](#deeptutor-cli-guide) · [रोडमैप](#roadmap) · [समुदाय](#community)

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇵🇹 Português](README_PT.md)

</div>

---
### 📰 समाचार

> **[2026.4.4]** बहुत दिन बाद! ✨ DeepTutor v1.0.0 आ गया — Apache-2.0 के तहत एजेंट-नेटिव विकास: ज़मीन से आर्किटेक्चर रिराइट, TutorBot, लचीले मोड। नया अध्याय शुरू!

> **[2026.2.6]** 🚀 39 दिनों में 10k सितारे — समुदाय का धन्यवाद!

> **[2026.1.1]** नया साल मुबारक! [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78), [Discussions](https://github.com/HKUDS/DeepTutor/discussions) से जुड़ें।

> **[2025.12.29]** DeepTutor आधिकारिक रूप से जारी।

### 📦 रिलीज़

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — गर्म सेटिंग रीलोड के लिए रनटाइम कैश इनवैलिडेशन, MinerU नेस्टेड आउटपुट, mimic WebSocket फिक्स, न्यूनतम Python 3.11+, CI सुधार।

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — एजेंट-नेटिव आर्किटेक्चर रिराइट (DeepTutor 2.0): दो-स्तरीय प्लगइन मॉडल (Tools + Capabilities), CLI व SDK प्रवेश, मल्टी-चैनल TutorBot, Co-Writer, Guided Learning, स्थायी मेमोरी।

<details>
<summary><b>पिछले रिलीज़</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — सत्र स्थिरता, इंक्रीमेंटल अपलोड, लचीला RAG, पूर्ण चीनी स्थानीयकरण।

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, लॉग, बग फिक्स।

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — एकीकृत कॉन्फ़िग, KB प्रति RAG, प्रश्न जनरेशन, साइडबार।

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — मल्टी-प्रोवाइडर LLM/एम्बेडिंग, नया होम, RAG डिकप्लिंग, env वेरिएबल।

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, GHCR इमेज।

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 व React 19, WebSocket, कमज़ोरियाँ।

</details>

<a id="key-features"></a>
## ✨ मुख्य विशेषताएँ

- **एकीकृत चैट वर्कस्पेस** — पाँच मोड, एक थ्रेड: Chat, Deep Solve, क्विज़, Deep Research, Math Animator एक संदर्भ साझा करते हैं।
- **व्यक्तिगत TutorBot** — चैटबॉट नहीं: स्वायत्त ट्यूटर, अपना वर्कस्पेस, मेमोरी, व्यक्तित्व, कौशल। [nanobot](https://github.com/HKUDS/nanobot)।
- **AI Co-Writer** — Markdown में AI सह-लेखक: फिर से लिखें, विस्तार, संक्षेप; KB व वेब।
- **Guided Learning** — आपकी सामग्री से संरचित दृश्य यात्राएँ।
- **नॉलेज हब** — PDF, Markdown, टेक्स्ट से RAG-तैयार KB; रंगीन नोटबुक।
- **स्थायी मेमोरी** — प्रगति सारांश व शिक्षार्थी प्रोफ़ाइल; TutorBot के साथ साझा।
- **एजेंट-नेटिव CLI** — क्षमता, KB, सत्र, TutorBot एक कमांड में; Rich व JSON। [`SKILL.md`](../../SKILL.md)।

---

<a id="get-started"></a>
## 🚀 शुरू करें

### विकल्प A — सेटअप टूर (अनुशंसित)

**एक इंटरैक्टिव स्क्रिप्ट** — निर्भरता, वातावरण, कनेक्शन टेस्ट, लॉन्च।

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

conda create -n deeptutor python=3.11 && conda activate deeptutor
# या: python -m venv .venv && source .venv/bin/activate

python scripts/start_tour.py
```

- **वेब मोड** — प्रोफ़ाइल, pip + npm, अस्थायी सर्वर, **सेटिंग्स**, 4 चरण।
- **CLI मोड** — पूरा टर्मिनल।

[http://localhost:3782](http://localhost:3782)

<a id="option-b-manual"></a>
### विकल्प B — मैन्युअल स्थानीय इंस्टॉल

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
<summary><b>समर्थित LLM प्रदाता</b></summary>

| प्रदाता | Binding | डिफ़ॉल्ट Base URL |
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
<summary><b>समर्थित एम्बेडिंग प्रदाता</b></summary>

एम्बेडिंग के लिए LLM जैसी ही सूची। सामान्य उदाहरण:

| प्रदाता | Binding | मॉडल उदाहरण |
|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` |
| DashScope | `dashscope` | `text-embedding-v3` |
| Ollama | `ollama` | `nomic-embed-text` |
| SiliconFlow | `siliconflow` | `BAAI/bge-m3` |
| vLLM | `vllm` | कोई भी एम्बेडिंग मॉडल |
| OpenAI-संगत | `custom` | — |

</details>

<details>
<summary><b>समर्थित वेब खोज प्रदाता</b></summary>

| प्रदाता | एन्व कुंजी | नोट |
|:--|:--|:--|
| Brave | `BRAVE_API_KEY` | अनुशंसित, मुफ़्त स्तर |
| Tavily | `TAVILY_API_KEY` | |
| Jina | `JINA_API_KEY` | |
| SearXNG | — | सेल्फ-होस्ट, API कुंजी नहीं |
| DuckDuckGo | — | API कुंजी नहीं |
| Perplexity | `PERPLEXITY_API_KEY` | API कुंजी आवश्यक |

</details>

```bash
python -m deeptutor.api.run_server
cd web && npm run dev -- -p 3782
```

| सेवा | पोर्ट |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

### विकल्प C — Docker

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

[विकल्प B](#option-b-manual) जैसा।

**2a. आधिकारिक इमेज** — [GHCR](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor)

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

**2b. स्रोत से बिल्ड** — `docker compose up -d`

**3.** [http://localhost:3782](http://localhost:3782)

```bash
docker compose logs -f
docker compose down
```

<details>
<summary><b>क्लाउड / रिमोट</b></summary>

```dotenv
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

</details>

<details>
<summary><b>डेव मोड (हॉट-रिलोड)</b></summary>

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

</details>

<details>
<summary><b>कस्टम पोर्ट</b></summary>

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

</details>

<details>
<summary><b>डेटा स्थिरता</b></summary>

| कंटेनर पथ | होस्ट | सामग्री |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | सेटिंग्स, मेमोरी, वर्कस्पेस, सत्र, लॉग |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | दस्तावेज़ व वेक्टर |

</details>

<details>
<summary><b>पर्यावरण चर</b></summary>

| चर | आवश्यक | विवरण |
|:---|:---:|:---|
| `LLM_BINDING` | **हाँ** | LLM प्रदाता |
| `LLM_MODEL` | **हाँ** | मॉडल |
| `LLM_API_KEY` | **हाँ** | कुंजी |
| `LLM_HOST` | **हाँ** | URL |
| `EMBEDDING_BINDING` | **हाँ** | एम्बेडिंग |
| `EMBEDDING_MODEL` | **हाँ** | मॉडल |
| `EMBEDDING_API_KEY` | **हाँ** | कुंजी |
| `EMBEDDING_HOST` | **हाँ** | URL |
| `EMBEDDING_DIMENSION` | **हाँ** | आयाम |
| `SEARCH_PROVIDER` | नहीं | खोज |
| `SEARCH_API_KEY` | नहीं | कुंजी |
| `BACKEND_PORT` | नहीं | डिफ़ॉल्ट `8001` |
| `FRONTEND_PORT` | नहीं | डिफ़ॉल्ट `3782` |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | नहीं | सार्वजनिक URL |
| `DISABLE_SSL_VERIFY` | नहीं | डिफ़ॉल्ट `false` |

</details>

### विकल्प D — केवल CLI

```bash
pip install -e ".[cli]"
deeptutor chat
deeptutor run chat "Explain Fourier transform"
deeptutor run deep_solve "Solve x^2 = 4"
deeptutor kb create my-kb --doc textbook.pdf
```

> पूर्ण गाइड: [DeepTutor CLI](#deeptutor-cli-guide)।

---

<a id="explore-deeptutor"></a>
## 📖 DeepTutor का अन्वेषण

<div align="center">
<img src="../../assets/figs/deeptutor-architecture.png" alt="DeepTutor आर्किटेक्चर" width="800">
</div>

### 💬 चैट — एकीकृत बुद्धिमान वर्कस्पेस

<div align="center">
<img src="../../assets/figs/dt-chat.png" alt="चैट" width="800">
</div>

पाँच मोड, **एकीकृत संदर्भ प्रबंधन**।

| मोड | कार्य |
|:---|:---|
| **Chat** | RAG, वेब, कोड, तर्क, ब्रेनस्टॉर्म, पेपर। |
| **Deep Solve** | मल्टी-एजेंट, उद्धरण। |
| **क्विज़ जनरेशन** | KB आधारित मूल्यांकन। |
| **Deep Research** | उप-विषय, समानांतर एजेंट, उद्धृत रिपोर्ट। |
| **Math Animator** | Manim। |

टूल **वर्कफ़्लो से अलग** — आप चुनते हैं क्या सक्रिय करना है।

### ✍️ Co-Writer — संपादक में AI

<div align="center">
<img src="../../assets/figs/dt-cowriter.png" alt="Co-Writer" width="800">
</div>

**फिर से लिखें**, **विस्तार**, **संक्षेप**; अनडू/रीडू; नोटबुक।

### 🎓 Guided Learning

<div align="center">
<img src="../../assets/figs/dt-guide.png" alt="Guided Learning" width="800">
</div>

1. योजना (3–5 बिंदु)।  
2. इंटरैक्टिव पृष्ठ।  
3. संदर्भ Q&A।  
4. सारांश।

### 📚 ज्ञान प्रबंधन

<div align="center">
<img src="../../assets/figs/dt-knowledge.png" alt="ज्ञान" width="800">
</div>

- **नॉलेज बेस** — PDF, TXT, MD।  
- **नोटबुक** — सत्र व रंग।

### 🧠 मेमोरी

<div align="center">
<img src="../../assets/figs/dt-memory.png" alt="मेमोरी" width="800">
</div>

- **सारांश** — प्रगति।  
- **प्रोफ़ाइल** — पसंद, स्तर, लक्ष्य। TutorBot साझा।

---

<a id="tutorbot"></a>
### 🦞 TutorBot — स्थायी स्वायत्त AI ट्यूटर

<div align="center">
<img src="../../assets/figs/tutorbot-architecture.png" alt="TutorBot आर्किटेक्चर" width="800">
</div>

[nanobot](https://github.com/HKUDS/nanobot) पर **बहु-इंस्टेंस** स्थायी एजेंट।

<div align="center">
<img src="../../assets/figs/tb.png" alt="TutorBot" width="800">
</div>

- **Soul टेम्पलेट** — व्यक्तित्व व शिक्षण दर्शन।  
- **स्वतंत्र वर्कस्पेस** — मेमोरी, सत्र, कौशल; साझा ज्ञान परत।  
- **प्रोएक्टिव Heartbeat** — अनुस्मारक व कार्य।  
- **पूर्ण टूल** — RAG, कोड, वेब, पेपर, तर्क, ब्रेनस्टॉर्म।  
- **कौशल सीखना** — skill फ़ाइलें।  
- **मल्टी-चैनल** — Telegram, Discord, Slack, Feishu, WeCom, DingTalk, ईमेल आदि।  
- **टीम व उप-एजेंट**।

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
deeptutor bot list
```

---

<a id="deeptutor-cli-guide"></a>
### ⌨️ DeepTutor CLI — एजेंट-नेटिव इंटरफ़ेस

<div align="center">
<img src="../../assets/figs/cli-architecture.png" alt="CLI" width="800">
</div>

बिना ब्राउज़र: क्षमता, KB, सत्र, मेमोरी, TutorBot। Rich + JSON। [`SKILL.md`](../../SKILL.md)।

```bash
deeptutor run chat "Explain the Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_question "Linear algebra" --config num_questions=5
deeptutor run deep_research "Attention mechanisms in transformers"
```

```bash
deeptutor chat --capability deep_solve --kb my-kb
# REPL में: /cap, /tool, /kb, /history, /notebook, /config से तुरंत बदलाव
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
<summary><b>पूर्ण CLI संदर्भ</b></summary>

**शीर्ष स्तर**

| कमांड | विवरण |
|:---|:---|
| `deeptutor run <capability> <message>` | एक बार में क्षमता चलाएँ (`chat`, `deep_solve`, `deep_question`, `deep_research`, `math_animator`) |
| `deeptutor chat` | इंटरैक्टिव REPL (`--capability`, `--tool`, `--kb`, `--language` आदि) |
| `deeptutor serve` | DeepTutor API सर्वर शुरू करें |

**`deeptutor bot`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor bot list` | सभी TutorBot इंस्टेंस |
| `deeptutor bot create <id>` | नया बॉट बनाएँ और चलाएँ (`--name`, `--persona`, `--model`) |
| `deeptutor bot start <id>` | बॉट शुरू |
| `deeptutor bot stop <id>` | बॉट रोकें |

**`deeptutor kb`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor kb list` | नॉलेज बेस सूची |
| `deeptutor kb info <name>` | विवरण |
| `deeptutor kb create <name>` | दस्तावेज़ों से बनाएँ (`--doc`, `--docs-dir`) |
| `deeptutor kb add <name>` | दस्तावेज़ जोड़ें |
| `deeptutor kb search <name> <query>` | खोज |
| `deeptutor kb set-default <name>` | डिफ़ॉल्ट KB |
| `deeptutor kb delete <name>` | हटाएँ (`--force`) |

**`deeptutor memory`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor memory show [file]` | देखें (`summary`, `profile`, `all`) |
| `deeptutor memory clear [file]` | साफ़ करें (`--force`) |

**`deeptutor session`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor session list` | सत्र सूची (`--limit`) |
| `deeptutor session show <id>` | संदेश |
| `deeptutor session open <id>` | REPL में जारी रखें |
| `deeptutor session rename <id>` | नाम बदलें (`--title`) |
| `deeptutor session delete <id>` | हटाएँ |

**`deeptutor notebook`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor notebook list` | नोटबुक सूची |
| `deeptutor notebook create <name>` | बनाएँ (`--description`) |
| `deeptutor notebook show <id>` | रिकॉर्ड |
| `deeptutor notebook add-md <id> <path>` | Markdown आयात |
| `deeptutor notebook replace-md <id> <rec> <path>` | रिकॉर्ड बदलें |
| `deeptutor notebook remove-record <id> <rec>` | रिकॉर्ड हटाएँ |

**`deeptutor config` / `plugin` / `provider`**

| कमांड | विवरण |
|:---|:---|
| `deeptutor config show` | कॉन्फ़िग सारांश |
| `deeptutor plugin list` | पंजीकृत टूल और क्षमताएँ |
| `deeptutor plugin info <name>` | टूल या क्षमता विवरण |
| `deeptutor provider login <provider>` | OAuth (`openai-codex`, `github-copilot`) |

</details>

<a id="roadmap"></a>
## 🗺️ रोडमैप

| स्थिति | माइलस्टोन |
|:---:|:---|
| 🔜 | **प्रमाणीकरण व लॉगिन** — सार्वजनिक डिप्लॉय के लिए वैकल्पिक लॉगिन व बहु-उपयोगकर्ता |
| 🔜 | **थीम व रूप** — विविध थीम व अनुकूलित UI |
| 🔜 | **LightRAG एकीकरण** — [LightRAG](https://github.com/HKUDS/LightRAG) को उन्नत नॉलेज बेस इंजन के रूप में |
| 🔜 | **दस्तावेज़ साइट** — गाइड, API संदर्भ व ट्यूटोरियल सहित पूर्ण दस्तावेज़ीकरण |

> यदि DeepTutor उपयोगी लगे तो [स्टार दें](https://github.com/HKUDS/DeepTutor/stargazers) — हमें प्रोत्साहन मिलता है!

---

<a id="community"></a>
## 🌐 समुदाय व पारिस्थितिकी तंत्र

| परियोजना | भूमिका |
|:---|:---|
| [**nanobot**](https://github.com/HKUDS/nanobot) | TutorBot इंजन |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | RAG |
| [**ManimCat**](https://github.com/Wing900/ManimCat) | Math Animator |

| [⚡ LightRAG](https://github.com/HKUDS/LightRAG) | [🤖 AutoAgent](https://github.com/HKUDS/AutoAgent) | [🔬 AI-Researcher](https://github.com/HKUDS/AI-Researcher) | [🧬 nanobot](https://github.com/HKUDS/nanobot) |
|:---:|:---:|:---:|:---:|
| तेज़ RAG | बिना-कोड एजेंट | स्वचालित अनुसंधान | अल्ट्रा-लाइट एजेंट |

## 🤝 योगदान

<div align="center">

हम चाहते हैं कि DeepTutor समुदाय के लिए उपहार बने। 🎁

<a href="https://github.com/HKUDS/DeepTutor/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/DeepTutor&max=999" alt="Contributors" />
</a>
</div>

[CONTRIBUTING.md](../../CONTRIBUTING.md) देखें।

## ⭐ स्टार इतिहास

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
