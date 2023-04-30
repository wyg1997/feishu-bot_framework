import os
import logging
import asyncio
import json
import wget

import regex
from EdgeGPT import Chatbot, ConversationStyle

from handlers import msg_handle_register, bot_register
from core.data_structure import MsgInfo, ActionType
from core.bot import bot_pool, BotBase
from core.card_builder import CardBuilder, CardTemplate
from core.service import reply_message
from core.config import global_config


def _remove_message_reference_charactor(msg: str) -> str:
    # remove bing reference charactors
    return regex.sub(r"\[\^\d+\^\]", "", msg)


@msg_handle_register.register_object(key=["/chat"])
def bing_chat_handle(msg_info: MsgInfo):
    logging.info(f"bing_chat_handle, msg_info: {msg_info}")
    bot_pool.ask(msg_info, ActionType.chat)


@bot_register.register_object(key=[ActionType.chat])
class ChatBot(BotBase):
    def __init__(self, root_id):
        super().__init__(root_id)
        self._chat_bot = None
        # TODO: dynamic cookie path
        self.cookie_path = "cookies.json"
        self._conversation_style = ConversationStyle[
            global_config["CONVERSATION_STYLE"]
        ]

    def __del__(self):
        if self._chat_bot is not None:
            asyncio.run(self._chat_bot.close())
        self._chat_bot = None

    def _do(self, msg_info: MsgInfo):
        bot = self._get_chat_bot()
        reply = asyncio.run(bot.ask(msg_info.text))

        # reply message
        logging.info(f"chat reply: {reply}")
        reply_text = reply["item"]["messages"][-1]["text"]
        reply_text = _remove_message_reference_charactor(reply_text)
        card_builder = (
            CardBuilder()
            .add_markdown(reply_text)
            .add_note(note_content=f"当前对话模式: {self._conversation_style.name}")
        )
        # first message, add header
        if len(self.message_ids) == 1:
            card_builder.add_header(CardTemplate.wathet, "🥳 新话题已创建，进入卡片可连续对话")
        reply_message(msg_info, content=card_builder.build())

    def _get_chat_bot(self) -> Chatbot:
        if self._chat_bot is not None:
            return self._chat_bot

        # init chat bot
        if not os.path.exists(self.cookie_path):
            url = global_config["COOKIE_URL"]
            if url:
                wget.download(url, out="cookies.json")
                logging.info(f"Downloading cookie from {url}")
            else:
                raise FileNotFoundError(f"cookie file not found: {self.cookie_path}")

        with open(self.cookie_path, "r") as f:
            cookies = json.load(f)
        self._chat_bot = Chatbot(cookies)
        return self._chat_bot
