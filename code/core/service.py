import logging
from typing import Union

from larksuiteoapi.service.im.v1 import model

from core.data_structure import MsgInfo, MessageType
from core.config import service


def reply_message(msg_info: MsgInfo, content, msg_id: Union[str, None] = None):
    body = model.MessageReplyReqBody()
    body.content = content
    body.msg_type = "interactive"

    req_call = service.messages.reply(body)
    msg_id = msg_id or str(msg_info.msg_id)
    req_call.set_message_id(msg_id)

    resp = req_call.do()
    if resp.code != 0:
        logging.error(
            f"reply message failed, code: {resp.code}, msg: {resp.msg}, error: {resp.error}"
        )
