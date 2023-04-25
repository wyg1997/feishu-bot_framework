import logging

from handlers.register import msg_handle_register
from core.data_structure import MsgInfo
from core.service import reply_message


@msg_handle_register.register_handle(keys=["/help", "/start", "帮助"])
def helper_handle(msg_info: MsgInfo):
    logging.info(f"helper_handle, msg_info: {msg_info}")
    reply_message(msg_info, text="Hello world!")
