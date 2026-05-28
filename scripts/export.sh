#!/usr/bin/env bash
# 知识库导出脚本（在服务器上直接运行）
set -euo pipefail

KB_DIR="${1:-./data/knowledge_base}"
OUTPUT_DIR="${2:-./data/archive}"
FORMAT="${3:-zip}"

mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="mindkeeper_kb_${TIMESTAMP}"

cd "$KB_DIR"

if [ "$FORMAT" = "zip" ]; then
    zip -r "${OUTPUT_DIR}/${ARCHIVE_NAME}.zip" .
    echo "已导出: ${OUTPUT_DIR}/${ARCHIVE_NAME}.zip"
    echo "下载: scp $(hostname):${OUTPUT_DIR}/${ARCHIVE_NAME}.zip ./"
else
    tar czf "${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz" .
    echo "已导出: ${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz"
    echo "下载: scp $(hostname):${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz ./"
fi
