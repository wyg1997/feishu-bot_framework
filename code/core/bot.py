import os
import json
import time
from typing import List, Union

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
        self.history: List[str] = []

    async def __del__(self):
        if self._chat_bot is not None:
            await self._chat_bot.close()
        self._chat_bot = None
        self._mage_bot = None

    async def chat(self, msg_info: MsgInfo):
        self._update_timestamp()
        reply_message(msg_info, text=f"现在是机器人复读机: {msg_info.text}")

        # TODO: use chat bot
        #  bot = self._get_chat_bot()

    async def image_gen(self, msg_info: MsgInfo):
        raise NotImplementedError("image gen not implemented yet")

    def _update_timestamp(self):
        self.timestamp = time.time()

    def _get_chat_bot(self):
        if self._chat_bot is not None:
            return self._chat_bot

        # init chat bot
        if not os.path.exists(self.cookie_path):
            raise FileNotFoundError(f"cookie file not found: {self.cookie_path}")

        with open(self.cookie_path, "r") as f:
            cookies = json.load(f)
        self._chat_bot = Chatbot(cookies)

    def _get_image_bot(self):
        if self._image_bot is not None:
            return self._image_bot

        # init image bot
        if not os.path.exists(self.cookie_path):
            raise FileNotFoundError(f"cookie file not found: {self.cookie_path}")

        with open(self.cookie_path, "r") as f:
            cookies = json.load(f)
        self._image_bot = ImageGen(cookies, quiet=True)


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

    async def ask(self, msg_info: MsgInfo, action_type: ActionType):
        if msg_info.chat_id not in self:
            self._create_bot(msg_info.chat_id)

        bot = self[msg_info.chat_id]
        assert bot is not None, "Unexpected error: bot is None"
        bot.history.append(msg_info.text)

        if action_type == ActionType.chat:
            return await bot.chat(msg_info)
        else:
            return await bot.image_gen(msg_info)

    def _create_bot(self, chat_id):
        assert (
            chat_id not in self.chat_id2bot_idx
        ), f"chat_id: {chat_id} already in pool"
        for i in range(self.bot_count):
            if self.bots[i] is None:
                self.bots[i] = Bot("cookie.json")
                self.chat_id2bot_idx[chat_id] = i
                return self.bots[i]
        raise RuntimeError("Don't have enough space to create new bot")

    def try_free_bots(self):
        pass


# TODO: load bot count from config
bot_pool = BotPool(bot_count=10)
