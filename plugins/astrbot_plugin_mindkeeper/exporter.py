import os
import shutil
from datetime import datetime
from astrbot.api import logger


class ExportManager:
    def __init__(self, kb_path: str, archive_dir: str):
        self.kb_path = kb_path
        self.archive_dir = archive_dir
        os.makedirs(archive_dir, exist_ok=True)

    async def create_archive(self, fmt: str = "zip") -> str:
        """创建知识库压缩包"""
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"mindkeeper_kb_{now}"
        archive_path = os.path.join(self.archive_dir, archive_name)

        if fmt == "zip":
            shutil.make_archive(archive_path, "zip", self.kb_path)
            archive_path += ".zip"
        else:
            shutil.make_archive(archive_path, "gztar", self.kb_path)
            archive_path += ".tar.gz"

        logger.info(f"知识库已导出: {archive_path}")
        return archive_path
