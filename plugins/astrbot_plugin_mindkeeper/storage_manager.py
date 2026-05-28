import os
import hashlib
from datetime import datetime
from astrbot.api import logger

_DEFAULT_CATEGORIES = [
    {"id": "investment", "display": "#投资记录", "dir": "01__investment"},
    {"id": "philosophy", "display": "#哲学观", "dir": "02__philosophy"},
    {"id": "questions", "display": "#问题库", "dir": "03__questions"},
    {"id": "decisions", "display": "#决策闭环", "dir": "04__decisions"},
]


class StorageManager:
    def __init__(self, base_path: str, categories: list = None,
                 date_format: str = "%Y-%m"):
        self.base_path = base_path
        self.categories = categories or _DEFAULT_CATEGORIES
        self.date_format = date_format
        self._cat_display_map = {c["display"]: c for c in self.categories}
        self._cat_id_map = {c["id"]: c for c in self.categories}
        self.logger = logger
        self._ensure_dirs()

    def _ensure_dirs(self):
        """启动时创建目录结构"""
        for cat in self.categories:
            os.makedirs(os.path.join(self.base_path, cat["dir"]), exist_ok=True)

    async def save(self, category: str, content: str,
                   source_platform: str, sender: str,
                   raw_text: str) -> str:
        """将 Markdown 内容保存到对应分类目录"""
        now = datetime.now()
        date_part = now.strftime(self.date_format)

        cat_obj = (self._cat_display_map.get(category)
                   or self._cat_id_map.get(category))
        if not cat_obj:
            cat_obj = self.categories[0]

        cat_dir = os.path.join(self.base_path, cat_obj["dir"], date_part)
        os.makedirs(cat_dir, exist_ok=True)

        content_hash = hashlib.md5(raw_text.encode()).hexdigest()[:8]
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{content_hash}.md"
        filepath = os.path.join(cat_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        self.logger.info(f"记录已保存: {filepath}")
        return filepath
