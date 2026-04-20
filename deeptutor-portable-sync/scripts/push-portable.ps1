# Push-Portable.ps1
# 一键推送 DeepTutor-Portable 到 GitHub
# 用法: Push-Portable [-Message "提交信息"]

param(
    [string]$Message = "update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

$ErrorActionPreference = "Stop"
$root = "D:\DeepTutor-Portable"

function Write-Step($text) {
    Write-Host "`n[=== $text ===]" -ForegroundColor Cyan
}

Set-Location $root

# Step 1: 大文件预检
Write-Step "Step 1: 大文件预检"
$largeFiles = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 100MB }
if ($largeFiles) {
    Write-Host "发现超过 100MB 的文件，禁止推送：" -ForegroundColor Red
    $largeFiles | Select-Object FullName, @{N="SizeMB";E={[math]::Round($_.Length/1MB,2)}}
    exit 1
}
Write-Host "通过：未检测到超过 100MB 的文件" -ForegroundColor Green

# Step 2: 确认根 .gitignore
Write-Step "Step 2: 确认 .gitignore"
$requiredPatterns = @("runtime/", "configs/.env", "deeptutor-src/.git.bak")
$gitignoreContent = if (Test-Path .gitignore) { Get-Content .gitignore -Raw } else { "" }
foreach ($pattern in $requiredPatterns) {
    if ($gitignoreContent -notmatch [regex]::Escape($pattern)) {
        Write-Host "警告: .gitignore 缺少 '$pattern'，自动追加" -ForegroundColor Yellow
        Add-Content -Path .gitignore -Value $pattern
    }
}
Write-Host "通过：.gitignore 检查完成" -ForegroundColor Green

# Step 3: 临时移走子仓库 .git
Write-Step "Step 3: 备份 deeptutor-src/.git"
if (-not (Test-Path deeptutor-src\.git)) {
    Write-Error "deeptutor-src/.git 不存在，可能已备份或目录结构异常"
    exit 1
}
if (Test-Path deeptutor-src\.git.bak) {
    Remove-Item -Recurse -Force deeptutor-src\.git.bak
}
Move-Item deeptutor-src\.git deeptutor-src\.git.bak
Write-Host "已备份为 deeptutor-src/.git.bak" -ForegroundColor Green

# Step 4: 提交并推送
Write-Step "Step 4: 提交并推送"
try {
    git add .
    $status = git status --short
    if (-not $status) {
        Write-Host "没有变更需要提交" -ForegroundColor Yellow
    } else {
        Write-Host "待提交变更：`n$status" -ForegroundColor Gray
        git commit -m "$Message"
        git push origin main
        Write-Host "推送成功: https://github.com/360PB/DeepTutor-Portable" -ForegroundColor Green
    }
} finally {
    # Step 5: 恢复子仓库 .git
    Write-Step "Step 5: 恢复 deeptutor-src/.git"
    if (Test-Path deeptutor-src\.git.bak) {
        Move-Item deeptutor-src\.git.bak deeptutor-src\.git
        Write-Host "已恢复 deeptutor-src/.git" -ForegroundColor Green
    }
}
