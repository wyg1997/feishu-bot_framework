import logging

from handlers.register import msg_handle_register
from core.data_structure import MsgInfo, ActionType
from core.bot import bot_pool


@msg_handle_register.register_handle(keys=["/default"])
def new_bing_handle(msg_info: MsgInfo):
    logging.info(f"new_bing_handle, msg_info: {msg_info}")
    bot_pool.ask(msg_info, ActionType.chat)
