# 🧠 MindKeeper — 震惊！你的微信聊天记录自动变成了知识库

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![AstrBot](https://img.shields.io/badge/AstrBot-4.x-7C3AED?logo=robot&logoColor=white)](https://github.com/Soulter/AstrBot)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**🏆 微信/钉钉/飞书发消息 → AI自动分类归档 → 永不遗忘的个人知识库**

[English](#english) · [中文](#中文)

</div>

<a name="中文"></a>

## 📖 这是啥？

你有没有这种体验：微信上看到的干货、群里讨论的精华、突然蹦出来的灵感——当时觉得"先放着回头整理"，然后就再也没找到过？

**MindKeeper** 解决了这个问题。连上你的微信/钉钉/飞书/Telegram，所有消息经过 **Claude/DeepSeek** 自动理解、分类、归档为结构化 Markdown 笔记。你只管聊天，它帮你整理。

> 💡 适合：经常在微信上学习/工作的知识工作者、投资者、产品经理、创业者

### ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 📱 **多平台接入** | 微信、钉钉、飞书、Telegram 统一管理 |
| 🤖 **AI 自动分类** | Claude / DeepSeek 语义理解，自动归入 4 类知识库 |
| 📝 **结构化 Markdown** | 自动生成标题、摘要、要点、标签、待办事项 |
| 🔄 **智能去重** | MD5 哈希 + 5 分钟时间窗口，避免重复保存 |
| 📦 **一键导出** | 随时打包为 ZIP / tar.gz 下载 |
| 🎯 **手动记录** | `/record` 命令手动强制分类保存 |
| ⚙️ **可配置** | 分类自定义、消息长度阈值、通知开关 |

### 🗂️ 分类体系

| 分类 | 目录 | 说明 |
|------|------|------|
| 💰 **#投资记录** | `01__investment/` | 投资决策、市场分析、交易记录、财务规划 |
| 🌏 **#哲学观** | `02__philosophy/` | 人生感悟、价值观、哲学思考、认知升级 |
| ❓ **#问题库** | `03__questions/` | 踩坑经验、技术难点、待研究事项 |
| ✅ **#决策闭环** | `04__decisions/` | 决策复盘、执行结果、经验教训 |

每条消息经过 LLM 理解后，按照 `知识库/<分类目录>/<YYYY-MM>/<时间戳>_<MD5>.md` 的路径自动归档。

### 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/dz1996511-maker/mindkeeper.git
cd mindkeeper

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 WebUI 密码和 LLM API Key

# 3. 启动
docker compose up -d

# 4. 打开 WebUI http://<服务器IP>:6185
#    - 配置 LLM Provider（Claude / DeepSeek）
#    - 连接 IM 平台（微信/钉钉/飞书）
#    - 启用 mindkeeper 插件
```

### 📁 项目结构

```
mindkeeper/
├── docker-compose.yml              # Docker 编排
├── .env.example                     # 环境变量模板
├── config/
│   ├── astrbot.yaml                # AstrBot 核心配置
│   └── plugins/
│       └── mindkeeper_categories.json  # 分类体系定义
├── plugins/
│   └── astrbot_plugin_mindkeeper/  # 🧠 核心分类逻辑
│       ├── main.py                 # 插件入口
│       ├── classifier.py           # LLM 消息分类 + 去重
│       ├── llm_prompts.py          # AI 提示词模板
│       ├── markdown_writer.py      # Markdown 构建
│       ├── storage_manager.py      # 文件系统存储
│       └── exporter.py             # 知识库导出
├── scripts/
│   ├── setup.sh                    # 一键部署脚本
│   └── export.sh                   # 知识库导出脚本
└── docs/
    ├── wechat-guide.md             # 微信接入指南
    ├── dingtalk-guide.md           # 钉钉接入指南
    └── feishu-guide.md             # 飞书接入指南
```

### 🔧 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `ASTRBOT_PASS` | WebUI 管理员密码 | ✅ |
| `CLAUDE_API_KEY` / `DEEPSEEK_API_KEY` | LLM API 密钥 | 至少一个 |
| `DINGTALK_APP_KEY` / `DINGTALK_APP_SECRET` | 钉钉接入凭证 | 可选 |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 飞书接入凭证 | 可选 |

### 📄 许可证

[MIT License](LICENSE)

---

<a name="english"></a>

## 📖 English — Auto-Save Your Chat History as a Knowledge Base

**MindKeeper** turns your WeChat/DingTalk/Feishu/Telegram messages into a structured knowledge base — automatically. Every message gets semantically classified by Claude/DeepSeek and saved as organized Markdown. Zero effort knowledge management.

### ✨ Features

| Feature | Description |
|---------|-------------|
| 📱 **Multi-Platform** | WeChat, DingTalk, Feishu, Telegram — unified |
| 🤖 **AI Classification** | Claude/DeepSeek semantic understanding → 4 categories |
| 📝 **Structured Output** | Auto-generated title, summary, key points, tags, action items |
| 🔄 **Smart Dedup** | MD5 hash + 5-min window prevents duplicates |
| 📦 **One-Click Export** | ZIP/tar.gz archive of entire knowledge base |
| ⚙️ **Configurable** | Custom categories, length thresholds, notification toggles |

### 🚀 Quick Start

```bash
git clone https://github.com/dz1996511-maker/mindkeeper.git
cd mindkeeper
cp .env.example .env
# Edit .env: set ASTRBOT_PASS and LLM API Key
docker compose up -d
# Open http://<your-server>:6185
```

### 📄 License

[MIT](LICENSE)

---

<div align="center">
Built with ❤️ on <a href="https://github.com/Soulter/AstrBot">AstrBot</a>
</div>
