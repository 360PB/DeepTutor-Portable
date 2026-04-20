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

[🇬🇧 English](../../README.md) · [🇨🇳 中文](README_CN.md) · [🇯🇵 日本語](README_JA.md) · [🇪🇸 Español](README_ES.md) · [🇫🇷 Français](README_FR.md) · [🇸🇦 العربية](README_AR.md) · [🇷🇺 Русский](README_RU.md) · [🇮🇳 हिन्दी](README_HI.md) · [🇵🇹 Português](README_PT.md) · [🇹🇭 ภาษาไทย](README_TH.md)

</div>

---
### 📦 रिलीज़

> **[2026.4.18]** [v1.1.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.2) — स्कीमा-चालित Channels टैब व सीक्रेट मास्किंग; एकल RAG पाइपलाइन; RAG/KB स्थिरता मजबूत; चैट प्रॉम्प्ट बाहरी फ़ाइलों में; थाई README।

> **[2026.4.17]** [v1.1.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.1) — सभी क्षमताओं पर सार्वभौमिक «अभी उत्तर दें»; Co-Writer स्क्रॉल सिंक; नोटबुक में सहेजते समय संदेश चयन; एकीकृत सेटिंग्स पैनल; स्ट्रीमिंग Stop बटन; TutorBot कॉन्फ़िगरेशन परमाणु लेखन।

> **[2026.4.15]** [v1.1.0](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0) — LaTeX ब्लॉक गणित पार्सिंग ओवरहॉल; `agents.yaml` के माध्यम से LLM डायग्नोस्टिक प्रोब; अतिरिक्त हेडर फॉरवर्डिंग फिक्स; SaveToNotebook UUID फिक्स; Docker + स्थानीय LLM मार्गदर्शिका।

> **[2026.4.14]** [v1.1.0-beta](https://github.com/HKUDS/DeepTutor/releases/tag/v1.1.0-beta) — URL-आधारित बुकमार्क योग्य सत्र; Snow थीम; WebSocket हार्टबीट व ऑटो-रीकनेक्ट; ChatComposer प्रदर्शन सुधार; एम्बेडिंग प्रदाता रजिस्ट्री ओवरहॉल; Serper खोज प्रदाता।

> **[2026.4.13]** [v1.0.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.3) — बुकमार्क व श्रेणियों के साथ प्रश्न नोटबुक; Visualize में Mermaid; एम्बेडिंग बेमेल पहचान; Qwen/vLLM अनुकूलता; LM Studio व llama.cpp समर्थन; Glass थीम।

> **[2026.4.11]** [v1.0.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.2) — SearXNG फ़ॉलबैक के साथ खोज समेकन; प्रदाता स्विच फिक्स; फ्रंटएंड संसाधन रिसाव फिक्स।

> **[2026.4.10]** [v1.0.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.1) — Visualize क्षमता (Chart.js/SVG); क्विज़ डुप्लिकेट रोकथाम; o4-mini मॉडल समर्थन।

> **[2026.4.10]** [v1.0.0-beta.4](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.4) — दर सीमा पर पुनःप्रयास के साथ एम्बेडिंग प्रगति; क्रॉस-प्लेटफ़ॉर्म निर्भरता फिक्स; MIME सत्यापन।

> **[2026.4.8]** [v1.0.0-beta.3](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.3) — नेटिव OpenAI/Anthropic SDK (litellm हटाया); Windows पर Math Animator; मजबूत JSON पार्सिंग; पूर्ण चीनी i18n।

> **[2026.4.7]** [v1.0.0-beta.2](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.2) — गर्म सेटिंग रीलोड; MinerU नेस्टेड आउटपुट; WebSocket फिक्स; न्यूनतम Python 3.11+।

> **[2026.4.4]** [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) — एजेंट-नेटिव आर्किटेक्चर रिराइट (~200k पंक्तियाँ): Tools + Capabilities प्लगइन मॉडल, CLI व SDK, TutorBot, Co-Writer, Guided Learning, स्थायी मेमोरी।

<details>
<summary><b>पिछले रिलीज़</b></summary>

> **[2026.1.23]** [v0.6.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.6.0) — सत्र स्थिरता, इंक्रीमेंटल अपलोड, लचीला RAG, पूर्ण चीनी स्थानीयकरण।

> **[2026.1.18]** [v0.5.2](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.2) — Docling, लॉग, बग फिक्स।

> **[2026.1.15]** [v0.5.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.5.0) — एकीकृत कॉन्फ़िग, KB प्रति RAG, प्रश्न जनरेशन, साइडबार।

> **[2026.1.9]** [v0.4.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.4.0) — मल्टी-प्रोवाइडर LLM/एम्बेडिंग, नया होम, RAG डिकप्लिंग, env वेरिएबल।

> **[2026.1.5]** [v0.3.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.3.0) — PromptManager, CI/CD, GHCR इमेज।

> **[2026.1.2]** [v0.2.0](https://github.com/HKUDS/DeepTutor/releases/tag/v0.2.0) — Docker, Next.js 16 व React 19, WebSocket, कमज़ोरियाँ।

</details>

### 📰 समाचार

> **[2026.4.4]** बहुत दिन बाद! ✨ DeepTutor v1.0.0 आ गया — Apache-2.0 के तहत एजेंट-नेटिव विकास: ज़मीन से आर्किटेक्चर रिराइट, TutorBot, लचीले मोड। नया अध्याय शुरू!

> **[2026.2.6]** 🚀 39 दिनों में 10k सितारे — समुदाय का धन्यवाद!

> **[2026.1.1]** नया साल मुबारक! [Discord](https://discord.gg/eRsjPgMU4t), [WeChat](https://github.com/HKUDS/DeepTutor/issues/78), [Discussions](https://github.com/HKUDS/DeepTutor/discussions) से जुड़ें।

> **[2025.12.29]** DeepTutor आधिकारिक रूप से जारी।

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

### पूर्वापेक्षाएँ

शुरू करने से पहले सुनिश्चित करें कि ये स्थापित हैं:

| आवश्यकता | संस्करण | जाँच | नोट |
|:---|:---|:---|:---|
| [Git](https://git-scm.com/) | कोई भी | `git --version` | क्लोन के लिए |
| [Python](https://www.python.org/downloads/) | 3.11+ | `python --version` | बैकएंड |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` | फ्रंटएंड बिल्ड (केवल CLI या Docker पर अनिवार्य नहीं) |
| [npm](https://www.npmjs.com/) | 9+ | `npm --version` | आमतौर पर Node के साथ |

कम से कम एक LLM प्रदाता की **API कुंजी** आवश्यक है (उदा. [OpenAI](https://platform.openai.com/api-keys), [DeepSeek](https://platform.deepseek.com/), [Anthropic](https://console.anthropic.com/))। सेटअप टूर इसे भरवाने और कनेक्शन परीक्षण में मदद करता है।

### विकल्प A — सेटअप टूर (अनुशंसित)

**एक इंटरैक्टिव स्क्रिप्ट** निर्भरताएँ स्थापित करती है, वातावरण सेट करती है, लाइव कनेक्शन टेस्ट करती है और लॉन्च करती है। `.env` का मैनुअल संपादन लगभग अनावश्यक।

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# Python वर्चुअल वातावरण (एक चुनें):
conda create -n deeptutor python=3.11 && conda activate deeptutor   # Anaconda/Miniconda हो तो
python -m venv .venv && source .venv/bin/activate                    # अन्यथा (macOS/Linux)
python -m venv .venv && .venv\Scripts\activate                       # अन्यथा (Windows)

python scripts/start_tour.py
```

टूर पूछता है कि आप DeepTutor कैसे उपयोग करना चाहते हैं:

- **वेब मोड** (अनुशंसित) — सभी निर्भरताएँ (pip + npm) स्थापित करता है, अस्थायी सर्वर चालू करता है और ब्राउज़र में **सेटिंग्स** खोलता है; LLM, एम्बेडिंग व खोज के लिए चार चरणों में लाइव टेस्ट; पूरा होने पर आपकी कॉन्फ़िगरेशन के साथ DeepTutor स्वतः पुनः आरंभ।
- **CLI मोड** — पूरा इंटरैक्टिव टर्मिनल प्रवाह: प्रोफ़ाइल, स्थापना, प्रदाता, सत्यापन और लागू — बिना शेल छोड़े।

दोनों स्थितियों में परिणाम [http://localhost:3782](http://localhost:3782) है।

> **दैनिक लॉन्च** — टूर केवल एक बार चलाएँ। उसके बाद:
>
> ```bash
> python scripts/start_web.py
> ```
>
> यह एक ही कमांड से बैकएंड व फ्रंटएंड चालू करता है और ब्राउज़र खोलता है। केवल प्रदाता बदलने या निर्भरताएँ पुनः स्थापित करने पर `start_tour.py` दोबारा चलाएँ।

<a id="option-b-manual"></a>
### विकल्प B — मैन्युअल स्थानीय इंस्टॉल

पूर्ण नियंत्रण चाहिए तो सब कुछ स्वयं स्थापित व कॉन्फ़िगर करें।

**1. निर्भरताएँ स्थापित करें**

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor

# वर्चुअल वातावरण बनाएँ व सक्रिय करें (विकल्प A जैसा)
conda create -n deeptutor python=3.11 && conda activate deeptutor

# बैकएंड + वेब सर्वर निर्भरताओं के साथ DeepTutor
pip install -e ".[server]"

# फ्रंटएंड (Node.js 18+ आवश्यक)
cd web && npm install && cd ..
```

**2. वातावरण कॉन्फ़िगर करें**

```bash
cp .env.example .env
```

`.env` संपादित करें और कम से कम आवश्यक फ़ील्ड भरें:

```dotenv
# LLM (आवश्यक)
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-xxx
LLM_HOST=https://api.openai.com/v1

# एम्बेडिंग (नॉलेज बेस के लिए आवश्यक)
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
<summary><b>समर्थित एम्बेडिंग प्रदाता</b></summary>

| प्रदाता | Binding | मॉडल उदाहरण | डिफ़ॉल्ट आयाम |
|:--|:--|:--|:--|
| OpenAI | `openai` | `text-embedding-3-large` | 3072 |
| Azure OpenAI | `azure_openai` | परिनियोजन नाम | — |
| Cohere | `cohere` | `embed-v4.0` | 1024 |
| Jina | `jina` | `jina-embeddings-v3` | 1024 |
| Ollama | `ollama` | `nomic-embed-text` | 768 |
| vLLM / LM Studio | `vllm` | कोई भी एम्बेडिंग मॉडल | — |
| OpenAI-संगत | `custom` | — | — |

OpenAI-संगत प्रदाता (DashScope, SiliconFlow, आदि) `custom` या `openai` binding से काम करते हैं।

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

**3. सेवाएँ शुरू करें**

सबसे तेज़ तरीका:

```bash
python scripts/start_web.py
```

बैकएंड व फ्रंटएंड एक साथ चालू करता है और ब्राउज़र खोलता है।

अलग-अलग टर्मिनल में मैन्युअल:

```bash
# Backend (FastAPI)
python -m deeptutor.api.run_server

# Frontend (Next.js) — दूसरा टर्मिनल
cd web && npm run dev -- -p 3782
```

| सेवा | डिफ़ॉल्ट पोर्ट |
|:---:|:---:|
| Backend | `8001` |
| Frontend | `3782` |

[http://localhost:3782](http://localhost:3782) खोलें।

### विकल्प C — Docker

Docker बैकएंड व फ्रंटएंड को एक कंटेनर में लपेटता है; स्थानीय Python या Node.js अनावश्यक। [Docker Desktop](https://www.docker.com/products/docker-desktop/) (या Linux पर Docker Engine + Compose) पर्याप्त है।

**1. पर्यावरण चर** (नीचे दोनों विकल्पों के लिए आवश्यक)

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
```

`.env` में कम से कम आवश्यक फ़ील्ड भरें ([विकल्प B](#option-b-manual) जैसा)।

**2a. आधिकारिक इमेज खींचें (अनुशंसित)**

आधिकारिक इमेज [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor) पर प्रत्येक रिलीज़ के लिए `linux/amd64` व `linux/arm64` के लिए प्रकाशित होती हैं।

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

संस्करण पिन करने के लिए `docker-compose.ghcr.yml` में इमेज टैग संपादित करें:

```yaml
image: ghcr.io/hkuds/deeptutor:1.0.0  # या :latest
```

**2b. स्रोत से बिल्ड**

```bash
docker compose up -d
```

`Dockerfile` से स्थानीय रूप से इमेज बनाता है और कंटेनर चालू करता है।

**3. सत्यापन व प्रबंधन**

कंटेनर healthy होने पर [http://localhost:3782](http://localhost:3782) खोलें।

```bash
docker compose logs -f   # लॉग टेल
docker compose down       # कंटेनर रोकें व हटाएँ
```

<details>
<summary><b>क्लाउड / रिमोट सर्वर</b></summary>

रिमोट सर्वर पर ब्राउज़र को बैकएंड API का सार्वजनिक URL चाहिए। `.env` में जोड़ें:

```dotenv
# सार्वजनिक URL जहाँ बैकएंड पहुँच योग्य है
NEXT_PUBLIC_API_BASE_EXTERNAL=https://your-server.com:8001
```

फ्रंटएंड स्टार्टअप स्क्रिप्ट रनटाइम पर यह मान लागू करती है — रीबिल्ड अनावश्यक।

</details>

<details>
<summary><b>डेव मोड (हॉट-रिलोड)</b></summary>

स्रोत माउंट करने व दोनों सेवाओं पर हॉट-रिलोड के लिए डेव ओवरले लगाएँ:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

`deeptutor/`, `deeptutor_cli/`, `scripts/` व `web/` में परिवर्तन तुरंत दिखते हैं।

</details>

<details>
<summary><b>कस्टम पोर्ट</b></summary>

`.env` में डिफ़ॉल्ट पोर्ट ओवरराइड करें:

```dotenv
BACKEND_PORT=9001
FRONTEND_PORT=4000
```

फिर पुनः आरंभ करें:

```bash
docker compose up -d     # या docker compose -f docker-compose.ghcr.yml up -d
```

</details>

<details>
<summary><b>डेटा स्थिरता</b></summary>

उपयोगकर्ता डेटा व नॉलेज बेस Docker वॉल्यूम के माध्यम से स्थानीय निर्देशिकाओं पर मैप होते हैं:

| कंटेनर पथ | होस्ट पथ | सामग्री |
|:---|:---|:---|
| `/app/data/user` | `./data/user` | सेटिंग्स, मेमोरी, वर्कस्पेस, सत्र, लॉग |
| `/app/data/knowledge_bases` | `./data/knowledge_bases` | अपलोड दस्तावेज़ व वेक्टर इंडेक्स |

`docker compose down` के बाद भी ये निर्देशिकाएँ बनी रहती हैं और अगले `up` पर पुनः उपयोग होती हैं।

</details>

<details>
<summary><b>पर्यावरण चर संदर्भ</b></summary>

| चर | आवश्यक | विवरण |
|:---|:---:|:---|
| `LLM_BINDING` | **हाँ** | LLM प्रदाता (`openai`, `anthropic`, आदि) |
| `LLM_MODEL` | **हाँ** | मॉडल नाम (उदा. `gpt-4o`) |
| `LLM_API_KEY` | **हाँ** | LLM API कुंजी |
| `LLM_HOST` | **हाँ** | API URL |
| `EMBEDDING_BINDING` | **हाँ** | एम्बेडिंग प्रदाता |
| `EMBEDDING_MODEL` | **हाँ** | एम्बेडिंग मॉडल नाम |
| `EMBEDDING_API_KEY` | **हाँ** | एम्बेडिंग API कुंजी |
| `EMBEDDING_HOST` | **हाँ** | एम्बेडिंग एंडपॉइंट |
| `EMBEDDING_DIMENSION` | **हाँ** | वेक्टर आयाम |
| `SEARCH_PROVIDER` | नहीं | खोज (`tavily`, `jina`, `serper`, `perplexity`, आदि) |
| `SEARCH_API_KEY` | नहीं | खोज API कुंजी |
| `BACKEND_PORT` | नहीं | बैकएंड पोर्ट (डिफ़ॉल्ट `8001`) |
| `FRONTEND_PORT` | नहीं | फ्रंटएंड पोर्ट (डिफ़ॉल्ट `3782`) |
| `NEXT_PUBLIC_API_BASE_EXTERNAL` | नहीं | क्लाउड के लिए सार्वजनिक बैकएंड URL |
| `DISABLE_SSL_VERIFY` | नहीं | SSL सत्यापन बंद (डिफ़ॉल्ट `false`) |

</details>

### विकल्प D — केवल CLI

यदि केवल CLI चाहिए, वेब फ्रंटएंड के बिना:

```bash
pip install -e ".[cli]"
```

LLM प्रदाता कॉन्फ़िगर करना अभी भी आवश्यक है। सबसे तेज़:

```bash
cp .env.example .env   # फिर .env में API कुंजियाँ भरें
```

कॉन्फ़िगरेशन के बाद:

```bash
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
| 🎯 | **प्रमाणीकरण व लॉगिन** — सार्वजनिक डिप्लॉय के लिए वैकल्पिक लॉगिन पृष्ठ व बहु-उपयोगकर्ता समर्थन |
| 🎯 | **थीम व रूप** — विविध थीम व अनुकूलित UI दिखावट |
| 🎯 | **इंटरैक्शन में सुधार** — आइकन डिज़ाइन व इंटरैक्शन विवरणों का अनुकूलन |
| 🔜 | **बेहतर मेमोरी** — बेहतर मेमोरी प्रबंधन का एकीकरण |
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
