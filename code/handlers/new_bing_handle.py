import logging

from handlers.register import msg_handle_register
from core.data_structure import MsgInfo
from core.service import reply_message


@msg_handle_register.register_handle(keys=["/default"])
def new_bing_handle(msg_info: MsgInfo):
    logging.info(f"new_bing_handle, msg_info: {msg_info}")
    reply_message(msg_info, "{" + f'"text": "复读机: {msg_info.text}"' + "}")
