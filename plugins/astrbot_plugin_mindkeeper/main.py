from astrbot.api.all import *
from astrbot.api import AstrBotConfig

from .classifier import MessageClassifier
from .markdown_writer import MarkdownWriter
from .storage_manager import StorageManager
from .exporter import ExportManager


@register("astrbot_plugin_mindkeeper", "MindKeeper Team",
          "自动分类消息并按类别保存为结构化 Markdown 到本地知识库",
          "1.0.0")
class MindKeeperPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.storage = StorageManager(
            base_path=config.get("kb_path", "/AstrBot/data/knowledge_base"),
            categories=config.get("categories", None),
            date_format=config.get("date_format", "%Y-%m"),
        )
        self.markdown_writer = MarkdownWriter()
        self.classifier = MessageClassifier(context)
        self.exporter = ExportManager(
            kb_path=self.storage.base_path,
            archive_dir=config.get("archive_dir", "/AstrBot/data/archive"),
        )

    @filter.on_message()
    async def on_message_handler(self, event: AstrMessageEvent):
        """处理每条收到的消息"""
        text = event.message_obj.message_str
        if not text or len(text.strip()) < self.config.get("min_length", 10):
            return

        platform = event.get_platform_name()
        sender = event.get_sender_name()

        # 跳过机器人自己的消息
        if (event.get_self_id() and event.get_sender_id()
                and event.get_sender_id() == event.get_self_id()):
            return

        # LLM 分类
        category, structured = await self.classifier.classify(
            text=text,
            provider_id=await self._get_provider_id(event),
            sender=sender,
            platform=platform,
        )
        if category is None:
            return

        # 生成 Markdown 并保存
        md_content = self.markdown_writer.build(
            category=category,
            structured=structured,
            sender=sender,
            platform=platform,
            raw_text=text,
        )
        file_path = await self.storage.save(
            category=category,
            content=md_content,
            source_platform=platform,
            sender=sender,
            raw_text=text,
        )

        if self.config.get("notify_on_save", True):
            short_path = file_path.replace(self.storage.base_path, "")
            yield event.plain_result(
                f"已保存至 {category}\n📁 {short_path}"
            )

    @filter.command("export")
    async def export_knowledge_base(self, event: AstrMessageEvent):
        """一键导出：/export"""
        export_path = await self.exporter.create_archive()
        yield event.plain_result(
            f"知识库已打包 📦\n{export_path}\n"
            "请从服务器下载（SCP/SFTP）"
        )

    @filter.command("record")
    async def manual_record(self, event: AstrMessageEvent):
        """手动记录：/record <内容>"""
        text = event.message_obj.message_str.replace("/record", "").strip()
        if not text:
            yield event.plain_result("用法: /record <要记录的内容>")
            return

        platform = event.get_platform_name()
        sender = event.get_sender_name()

        category, structured = await self.classifier.classify(
            text=text,
            provider_id=await self._get_provider_id(event),
            sender=sender,
            platform=platform,
        )
        if category is None:
            yield event.plain_result("无法分类，请补充更多上下文")
            return

        md_content = self.markdown_writer.build(
            category=category,
            structured=structured,
            sender=sender,
            platform=platform,
            raw_text=text,
        )
        file_path = await self.storage.save(
            category=category,
            content=md_content,
            source_platform=platform,
            sender=sender,
            raw_text=text,
        )
        short_path = file_path.replace(self.storage.base_path, "")
        yield event.plain_result(
            f"已手动记录至 {category}\n📁 {short_path}"
        )

    async def _get_provider_id(self, event: AstrMessageEvent):
        """获取当前 LLM 提供者 ID"""
        try:
            umo = event.unified_msg_origin
            return await self.context.get_current_chat_provider_id(umo=umo)
        except Exception:
            return self.config.get("default_provider_id")

    async def terminate(self):
        """插件卸载时清理"""
        await self.classifier.close()
