from datetime import datetime
import re


class MarkdownWriter:
    def __init__(self, template_name: str = "default"):
        self.template_name = template_name

    def build(self, category: str, structured: dict,
              sender: str, platform: str, raw_text: str) -> str:
        """构建结构化 Markdown 文档"""
        now = datetime.now()
        title = structured.get("title", "未命名")

        lines = []
        # YAML 前置元数据
        lines.append("---")
        lines.append(f"title: {title}")
        lines.append(f"date: {now.strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"source: {platform}")
        lines.append(f"sender: {sender}")
        lines.append(f"category: {category}")
        tags = structured.get("tags", [])
        lines.append(f"tags: [{', '.join(tags)}]")
        lines.append("---")
        lines.append("")

        # 正文
        lines.append(f"# {title}")
        lines.append("")

        summary = structured.get("summary", "")
        if summary:
            lines.append("## 摘要")
            lines.append("")
            lines.append(summary)
            lines.append("")

        key_points = structured.get("key_points", [])
        if key_points:
            lines.append("## 要点")
            lines.append("")
            for pt in key_points:
                lines.append(f"- {pt}")
            lines.append("")

        lines.append("## 原始内容")
        lines.append("")
        lines.append(raw_text)
        lines.append("")

        actions = structured.get("action_items", [])
        if actions:
            lines.append("## 待办事项")
            lines.append("")
            for a in actions:
                lines.append(f"- [ ] {a}")
            lines.append("")

        if tags:
            lines.append("## 标签")
            lines.append("")
            lines.append(" ".join(f"#{t}" for t in tags))
            lines.append("")

        lines.append("---")
        lines.append(f"*由 MindKeeper 于 {now.strftime('%Y-%m-%d %H:%M')} 自动记录*")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def sanitize_filename(text: str) -> str:
        """移除文件名不安全字符"""
        return re.sub(r'[\\/:*?"<>|]', '', text).strip()[:60]
