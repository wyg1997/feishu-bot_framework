import os
import json
import time
from typing import List, Union
import logging
import asyncio

from EdgeGPT import Chatbot
from ImageGen import ImageGen

from core.data_structure import MsgInfo, ActionType
from core.service import reply_message


class Bot(object):
    def __init__(self, cookie_path):
        self._chat_bot = None
        self._image_bot = None
        self.cookie_path = cookie_path
        self.timestamp = time.time()
        self.message_ids = set()

    def __del__(self):
        if self._chat_bot is not None:
            asyncio.run(self._chat_bot.close())
        self._chat_bot = None
        self._image_bot = None

    def is_timeout(self, timeout):
        raise NotImplementedError("is_timeout not implemented yet")

    def chat(self, msg_info: MsgInfo):
        if msg_info.msg_id in self.message_ids:
            return
        self.message_ids.add(msg_info.msg_id)
        self._update_timestamp()
        bot = self._get_chat_bot()
        reply = asyncio.run(bot.ask(msg_info.text))
        logging.info(f"chat reply: {reply}")
        reply_message(msg_info, text=reply["item"]["messages"][-1]["text"])

    def image_gen(self, msg_info: MsgInfo):
        raise NotImplementedError("image gen not implemented yet")

    def _update_timestamp(self):
        self.timestamp = time.time()

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

    def _get_image_bot(self) -> ImageGen:
        if self._image_bot is not None:
            return self._image_bot

        # init image bot
        if not os.path.exists(self.cookie_path):
            raise FileNotFoundError(f"cookie file not found: {self.cookie_path}")

        with open(self.cookie_path, "r") as f:
            cookies = json.load(f)
        self._image_bot = ImageGen(cookies, quiet=True)
        return self._image_bot


class BotPool(object):
    def __init__(self, bot_count):
        self.bot_count = bot_count
        self.bots: List[Union[None, Bot]] = [None] * bot_count
        self.chat_id2bot_idx = {}

    def __contains__(self, chat_id):
        return chat_id in self.chat_id2bot_idx

    def __getitem__(self, chat_id):
        assert chat_id in self.chat_id2bot_idx, f"chat_id: {chat_id} not in pool"
        return self.bots[self.chat_id2bot_idx[chat_id]]

    def ask(self, msg_info: MsgInfo, action_type: ActionType):
        if msg_info.chat_id not in self:
            self._create_bot(msg_info.chat_id)

        bot = self[msg_info.chat_id]
        assert bot is not None, "Unexpected error: bot is None"

        if action_type == ActionType.chat:
            bot.chat(msg_info)
        else:
            bot.image_gen(msg_info)

    def try_free_bots(self):
        # TODO: free bots which are timeout
        for i in range(self.bot_count):
            bot = self.bots[i]
            if bot is None:
                del bot
            self.bots[i] = None

    def _create_bot(self, chat_id):
        assert (
            chat_id not in self.chat_id2bot_idx
        ), f"chat_id: {chat_id} already in pool"
        for i in range(self.bot_count):
            if self.bots[i] is None:
                # TODO: read cookie path from config
                self.bots[i] = Bot("cookies.json")
                self.chat_id2bot_idx[chat_id] = i
                return self.bots[i]
        self.try_free_bots()
        for i in range(self.bot_count):
            if self.bots[i] is None:
                self.bots[i] = Bot("cookies.json")
                self.chat_id2bot_idx[chat_id] = i
                return self.bots[i]
        raise RuntimeError("Don't have enough space to create new bot")


# TODO: load bot count from config
bot_pool = BotPool(bot_count=10)
