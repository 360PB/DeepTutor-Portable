# DeepTutor Portable

DeepTutor 离线整合包，无需安装 Python/Node.js，解压即用。

| 资源 | 链接 |
|------|------|
| 下载 (夸克网盘) | https://pan.quark.cn/s/b0ae07ff3fdb |
| GitHub 仓库 | https://github.com/360PB/DeepTutor-Portable |
| 上游源码 | https://github.com/HKUDS/DeepTutor |

## 快速开始

1. **配置环境变量**
   ```
   复制 configs\.env.example 为 configs\.env
   编辑 configs\.env，填写你的 LLM API Key
   ```

2. **一键启动**
   ```
   双击 start.bat
   ```

3. **访问**
   - 前端: http://localhost:3782
   - 后端: http://localhost:8001

## 目录结构

```
DeepTutor-Portable/
├── runtime/                 # 嵌入式运行时（不在 Git 仓库中）
│   ├── python/              # 嵌入式 Python 3.11
│   └── nodejs/              # 嵌入式 Node.js 20
├── deeptutor-src/           # DeepTutor 源码（可替换更新）
│   ├── deeptutor/           # Python 后端
│   ├── web/                 # Next.js 前端
│   └── requirements/        # 依赖定义
├── workspace/               # 用户数据持久化（升级时保留）
│   └── data/
├── configs/
│   ├── .env                 # 环境配置（用户填写，Git 忽略）
│   └── .env.example         # 配置模板
├── .agents/
│   └── skills/              # Kimi 维护 Skill
└── README.md
```

## 技术栈

- **后端**: Python 3.11 + FastAPI + uvicorn
- **前端**: Next.js 16 + React 19 + TypeScript
- **依赖**: 213+ Python 包 + npm 包

## 支持的功能

- 统一聊天工作区（Chat / Deep Solve / Quiz / Deep Research / Math Animator）
- AI Co-Writer
- Guided Learning
- Knowledge Hub（RAG 知识库）
- TutorBot 多平台频道
- 持久化记忆

## 配置说明

### LLM 提供商

支持 OpenAI、Anthropic、DeepSeek、DashScope、LM Studio、Ollama 等 30+ 提供商。

### Embedding 提供商

支持 OpenAI、Azure OpenAI、Ollama、vLLM 等。

### 本地部署

使用 LM Studio 或 Ollama 可实现完全离线运行：

```ini
LLM_BINDING=lm_studio
LLM_HOST=http://localhost:1234/v1
EMBEDDING_BINDING=lm_studio
EMBEDDING_HOST=http://localhost:1234/v1
```

## 更新与维护

本项目使用 `.agents/skills/deeptutor-portable-sync/` 中的 Kimi Skill 进行维护，包含以下工作流：

- **同步上游**: 从 `HKUDS/DeepTutor` 拉取最新源码到 `deeptutor-src/`
- **推送发布**: 将整合包推送到 `360PB/DeepTutor-Portable`

手动更新源码：直接替换 `deeptutor-src/` 目录中的文件，保留 `workspace/` 用户数据。

## 常见问题

**Q: 启动后无法访问前端？**
A: 检查 configs/.env 是否配置正确，确保 API Key 已填写。

**Q: 知识库上传失败？**
A: 确保 Embedding 配置正确，且模型支持文本嵌入。

**Q: runtime/ 目录缺失？**
A: `runtime/` 包含嵌入式 Python/Node 运行时（约 535MB），未包含在 Git 仓库中。请从网盘下载完整整合包，或参照 `offline-portable-pack` Skill 自行制作。

## 相关资源

- DeepTutor 官方: https://github.com/HKUDS/DeepTutor
- 离线整合包制作 Skill: `offline-portable-pack`
