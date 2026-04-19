# DeepTutor Portable

DeepTutor 离线整合包，无需安装 Python/Node.js，解压即用。

下载: https://pan.quark.cn/s/b0ae07ff3fdb

## 快速开始

1. **配置环境变量**
   ```
   复制 configs\.env.example 为 configs\.env
   编辑 configs\.env，填写你的 LLM API Key
   ```

2. **一键启动**
   ```
   双击 scripts\start.bat
   ```

3. **访问**
   - 前端: http://localhost:3782
   - 后端: http://localhost:8001

## 目录结构

```
DeepTutor-Portable/
├── runtime/
│   ├── python/          # 嵌入式 Python 3.11
│   └── nodejs/          # 嵌入式 Node.js 20
├── deeptutor-src/       # DeepTutor 源码
│   ├── deeptutor/       # Python 后端
│   ├── web/             # Next.js 前端
│   └── requirements/    # 依赖定义
├── workspace/           # 用户数据持久化
│   └── data/
├── scripts/
│   └── start.bat        # 一键启动脚本
├── configs/
│   └── .env             # 环境配置（用户填写）
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

## 常见问题

**Q: 启动后无法访问前端？**
A: 检查 configs/.env 是否配置正确，确保 API Key 已填写。

**Q: 知识库上传失败？**
A: 确保 Embedding 配置正确，且模型支持文本嵌入。

**Q: 如何更新源码？**
A: 直接替换 `deeptutor-src/` 目录中的文件，保留 `workspace/` 数据。

## 源码

- DeepTutor 官方: https://github.com/HKUDS/DeepTutor
- 整合包制作参考: 离线整合包制作 Skill.md
