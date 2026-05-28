# MindKeeper 本地部署包打包脚本（在 Windows 上运行）
# 将部署包打包为 tar.gz，方便上传到云服务器

$PROJECT_DIR = "$HOME\mindkeeper"
$OUTPUT_DIR = "$HOME\Desktop"

# 检查目录
if (-not (Test-Path $PROJECT_DIR)) {
    Write-Error "未找到项目目录: $PROJECT_DIR"
    exit 1
}

$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$ARCHIVE_NAME = "mindkeeper-deploy-$TIMESTAMP.tar.gz"

# 使用 tar 打包（Windows 10 1803+ 内置 tar）
Set-Location $HOME
tar czf "$OUTPUT_DIR\$ARCHIVE_NAME" -C "$HOME" mindkeeper/

Write-Host "部署包已创建: $OUTPUT_DIR\$ARCHIVE_NAME"
Write-Host "大小: $((Get-Item "$OUTPUT_DIR\$ARCHIVE_NAME").Length / 1MB -as [int]) MB"
Write-Host ""
Write-Host "上传到服务器:"
Write-Host "  scp $OUTPUT_DIR\$ARCHIVE_NAME user@your-server:~/"
Write-Host "  ssh user@your-server"
Write-Host "  tar xzf $ARCHIVE_NAME"
Write-Host "  cd mindkeeper && bash scripts/setup.sh"
