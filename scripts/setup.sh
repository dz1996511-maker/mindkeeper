#!/usr/bin/env bash
# MindKeeper 云服务器一键部署脚本
# 适用系统: Ubuntu 22.04+ / Debian 12+
set -euo pipefail

MINDKEEPER_DIR="${HOME}/mindkeeper"

echo "========================================"
echo "  MindKeeper 云服务器一键部署"
echo "========================================"

# 1. 检查依赖
echo "[1/6] 检查依赖..."
for cmd in curl git docker; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "错误: $cmd 未安装。请先安装:"
        echo "  Ubuntu: sudo apt update && sudo apt install -y $cmd"
        echo "  Debian: sudo apt update && sudo apt install -y $cmd"
        exit 1
    fi
done

if ! docker compose version &>/dev/null; then
    echo "错误: Docker Compose 未安装。请安装 Docker Compose v2+"
    exit 1
fi

# 2. 创建项目目录
echo "[2/6] 创建项目目录..."
mkdir -p "$MINDKEEPER_DIR"
cd "$MINDKEEPER_DIR"

# 3. 下载部署包（如果目录为空）
echo "[3/6] 初始化部署包..."
if [ ! -f "docker-compose.yml" ]; then
    echo "请将 mindkeeper 部署包的所有文件复制到 $MINDKEEPER_DIR"
    echo "然后重新运行此脚本。"
    echo ""
    echo "上传方式（在本地电脑执行）:"
    echo "  scp -r mindkeeper/* user@your-server:$MINDKEEPER_DIR/"
    exit 1
fi

# 4. 配置环境变量
echo "[4/6] 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ">>> 请编辑 .env 文件，填入以下信息:"
    echo "    - ASTRBOT_PASS: WebUI 管理员密码（必填）"
    echo "    - LLM API Key（Claude / DeepSeek 至少一个）"
    echo "    - 平台适配器凭证（微信/钉钉/飞书）"
    echo ""
    read -p "编辑完成后按 Enter 继续..."
fi

# 5. 创建数据目录
echo "[5/6] 创建数据目录..."
mkdir -p data/knowledge_base/{01__investment,02__philosophy,03__questions,04__decisions}
mkdir -p data/archive data/logs

# 6. 启动服务
echo "[6/6] 启动 Docker 服务..."
docker compose pull
docker compose up -d

echo ""
echo "========================================"
echo "  ✅ 部署完成！"
echo "========================================"
echo ""
echo "WebUI 地址: http://$(curl -s ifconfig.me):$(grep ASTRBOT_WEBUI_PORT .env 2>/dev/null | cut -d= -f2 || echo 6185)"
echo "登录账号: $(grep ASTRBOT_USER .env 2>/dev/null | cut -d= -f2 || echo admin)"
echo "登录密码: <你设置的密码>"
echo ""
echo "后续配置:"
echo "  1. 打开 WebUI，添加 LLM Provider（Claude / DeepSeek）"
echo "  2. 配置 IM 平台适配器（微信/钉钉/飞书）"
echo "  3. 在插件管理中启用 mindkeeper 插件"
echo "  4. 发送消息即可自动记录！"
echo ""
echo "常用命令:"
echo "  docker compose logs -f    # 查看实时日志"
echo "  docker compose restart    # 重启服务"
echo "  docker compose pull       # 更新到最新版本"
echo "  docker compose down       # 停止服务"
