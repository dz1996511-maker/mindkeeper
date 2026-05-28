import json
import hashlib
import time
from astrbot.api import logger
from .llm_prompts import CLASSIFICATION_SYSTEM_PROMPT


class MessageClassifier:
    def __init__(self, context):
        self.context = context
        # 简单去重: {hash: timestamp}
        self._dedup_cache = {}

    def _check_dedup(self, text: str) -> bool:
        """检查是否重复消息（5分钟窗口）"""
        msg_hash = hashlib.md5(text.encode()).hexdigest()
        now = time.time()
        if msg_hash in self._dedup_cache:
            if now - self._dedup_cache[msg_hash] < 300:
                return True  # 重复
        self._dedup_cache[msg_hash] = now
        # 清理过期缓存
        for h in list(self._dedup_cache.keys()):
            if now - self._dedup_cache[h] > 300:
                del self._dedup_cache[h]
        return False

    async def classify(self, text: str, provider_id: str,
                       sender: str, platform: str) -> tuple:
        """返回 (category, structured_dict) 或 (None, None)"""
        if self._check_dedup(text):
            logger.debug("跳过重复消息")
            return None, None

        user_prompt = f"""请分析以下消息，判断是否需要记录到个人知识库。

发送者: {sender}
来源平台: {platform}
消息内容: {text}

请严格按照系统指令的 JSON 格式返回。"""

        try:
            resp = await self.context.llm_generate(
                chat_provider_id=provider_id,
                prompt=user_prompt,
                system_prompt=CLASSIFICATION_SYSTEM_PROMPT,
            )
            raw = resp.completion_text.strip()
            # 提取 JSON（兼容代码块包裹的情况）
            if "```json" in raw:
                raw = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0].strip()

            result = json.loads(raw)
            if result.get("category") is None:
                return None, None
            return result["category"], result
        except Exception as e:
            logger.error(f"分类失败: {e}")
            return None, None

    async def close(self):
        self._dedup_cache.clear()
