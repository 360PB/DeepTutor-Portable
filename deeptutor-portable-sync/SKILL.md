---
name: deeptutor-portable-sync
description: 维护 DeepTutor-Portable 离线整合包。工作流包括：(1) 从上游 HKUDS/DeepTutor 同步最新源码到 deeptutor-src/ 子目录；(2) 将 DeepTutor-Portable 根目录内容推送到 360PB/DeepTutor-Portable。当用户要求"更新项目"、"同步上游"、"拉取最新代码"、"推送"、"发布 portable 包"时触发。
---

# DeepTutor-Portable 同步与推送

## 项目结构

```
DeepTutor-Portable/          <-- 根仓库 (origin: 360PB/DeepTutor-Portable)
├── .git/
├── .gitignore               <-- 排除 runtime/、configs/.env
├── deeptutor-src/           <-- 子仓库 (origin: HKUDS/DeepTutor)
│   ├── .git/
│   └── ...                  <-- DeepTutor 源码
├── runtime/                 <-- 被 .gitignore 排除 (535MB 二进制)
├── configs/
│   └── .env                 <-- 被 .gitignore 排除 (含 API Key)
└── ...
```

**关键约束**：`deeptutor-src` 有自己的 `.git`，因此根仓库默认将其视为 submodule（不跟踪内部文件）。推送前必须临时移走 `deeptutor-src/.git`，否则根仓库无法包含源码内容。

## 工作流 A：同步上游源码

当用户要求从上游更新 DeepTutor 源码时：

1. **进入子仓库拉取上游**
   ```powershell
   Set-Location D:\DeepTutor-Portable\deeptutor-src
   git fetch origin
   git merge origin/main
   ```
   如有冲突，解决冲突后 `git commit`。

2. **忽略未提交修改**（用户要求时）
   ```powershell
   Set-Location D:\DeepTutor-Portable\deeptutor-src
   git checkout -- .
   git clean -fd
   ```

3. **验证构建**（可选，用户明确要求时）
   - 前端：`cd web && npm run build`
   - 后端：`python -m deeptutor.api.run_server`

## 工作流 B：推送 Portable 包到 GitHub

当用户要求推送当前目录到 360PB/DeepTutor-Portable 时：

### Step 1: 大文件预检

运行脚本检查是否有超过 100MB 的文件被意外加入：

```powershell
Set-Location D:\DeepTutor-Portable
$largeFiles = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 100MB }
if ($largeFiles) {
    Write-Host "发现超过 100MB 的文件，禁止推送：" -ForegroundColor Red
    $largeFiles | Select-Object FullName, @{N="SizeMB";E={[math]::Round($_.Length/1MB,2)}}
    throw "存在大文件，需先排除"
}
```

### Step 2: 确认根 .gitignore

确保根 `.gitignore` 至少包含：

```gitignore
# Git backup
deeptutor-src/.git.bak

# Runtime binaries (distributed separately)
runtime/

# Secrets
configs/.env
**/.env.local

# OS files
.DS_Store
Thumbs.db
```

### Step 3: 临时移走子仓库 .git

这是**最关键的一步**。不移走则根仓库无法跟踪 `deeptutor-src` 内部文件。

```powershell
Set-Location D:\DeepTutor-Portable
if (Test-Path deeptutor-src\.git.bak) {
    Remove-Item -Recurse -Force deeptutor-src\.git.bak
}
Move-Item deeptutor-src\.git deeptutor-src\.git.bak
```

### Step 4: 提交并推送

```powershell
Set-Location D:\DeepTutor-Portable
git add .
git status                    # 确认待提交内容合理
git commit -m "update: sync from upstream"
git push origin main
```

### Step 5: 恢复子仓库 .git

```powershell
Set-Location D:\DeepTutor-Portable
Move-Item deeptutor-src\.git.bak deeptutor-src\.git
```

## 注意事项

- **`.bat` 编码红线**：如果更新涉及修改 `.bat` 文件，必须使用 ANSI (GBK) 编码，禁止 UTF-8 BOM。详见 `offline-portable-pack` skill。
- **敏感文件**：`configs/.env` 包含 API Key，永远不应进 git。根 `.gitignore` 已排除它。
- **不要推送 `runtime/`**：该目录包含嵌入式 Python/Node 运行时（约 535MB），已通过 `.gitignore` 排除。完整包应通过网盘或 GitHub Releases 分发。
- **deeptutor-src 内部依赖**：`node_modules/`、`.next/` 等由 `deeptutor-src/.gitignore` 自动排除，无需在根 `.gitignore` 中重复。
- **版本号**：如需在 README 或发布说明中更新版本号，同步修改后一并提交。

## 一键脚本

如需自动化，执行 `scripts/push-portable.ps1`：

```powershell
. .agents\skills\deeptutor-portable-sync\scripts\push-portable.ps1
Push-Portable -Message "update: 描述信息"
```
