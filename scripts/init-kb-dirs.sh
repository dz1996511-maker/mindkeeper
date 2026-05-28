#!/usr/bin/env bash
# 初始化知识库目录结构
set -euo pipefail

BASE="${1:-./data/knowledge_base}"

echo "初始化知识库目录结构..."
mkdir -p "$BASE/01__investment"
mkdir -p "$BASE/02__philosophy"
mkdir -p "$BASE/03__questions"
mkdir -p "$BASE/04__decisions"

for dir in "$BASE"/[0-9]*__*/; do
    name=$(basename "$dir")
    if [ ! -f "$dir/README.md" ]; then
        cat > "$dir/README.md" <<-READE
# ${name#*__}

${name#*__} 类别知识库。

创建时间: $(date +%Y-%m-%d)
READE
    fi
done

echo "完成。目录结构:"
find "$BASE" -maxdepth 2 -type d | sort
