import os
import logging
import asyncio
import json

from EdgeGPT import Chatbot

from handlers import msg_handle_register, bot_register
from core.data_structure import MsgInfo, ActionType
from core.bot import bot_pool, BotBase
from core.card_builder import CardBuilder, CardTemplate
from core.service import reply_message


@msg_handle_register.register_object(key=["/chat"])
def new_bing_handle(msg_info: MsgInfo):
    logging.info(f"new_bing_handle, msg_info: {msg_info}")
    bot_pool.ask(msg_info, ActionType.chat)


@bot_register.register_object(key=[ActionType.chat])
class ChatBot(BotBase):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self._chat_bot = None
        self.cookie_path = "cookies.json"

    def __del__(self):
        if self._chat_bot is not None:
            asyncio.run(self._chat_bot.close())
        self._chat_bot = None

    def _do(self, msg_info: MsgInfo):
        bot = self._get_chat_bot()
        reply = asyncio.run(bot.ask(msg_info.text))

        # reply message
        logging.info(f"chat reply: {reply}")
        card_builder = CardBuilder().add_markdown(reply["item"]["messages"][-1]["text"])
        # first message, add header
        if len(self.message_ids) == 1:
            card_builder.add_header(CardTemplate.wathet, "🥳 新话题已创建，进入卡片可连续对话")
        reply_message(msg_info, content=card_builder.build())

    def _get_chat_bot(self) -> Chatbot:
        if self._chat_bot is not None:
            return self._chat_bot

        # init chat bot
        if not os.path.exists(self.cookie_path):
            raise FileNotFoundError(f"cookie file not found: {self.cookie_path}")

        with open(self.cookie_path, "r") as f:
            cookies = json.load(f)
        self._chat_bot = Chatbot(cookies)
        return self._chat_bot
