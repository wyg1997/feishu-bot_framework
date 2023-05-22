import logging
from typing import Union

from larksuiteoapi.service.im.v1 import model

from core.data_structure import MsgInfo, MessageType
from core.config import service


def reply_message(msg_id: str, content):
    body = model.MessageReplyReqBody()
    body.content = content
    body.msg_type = "interactive"

    req_call = service.messages.reply(body)
    req_call.set_message_id(msg_id)

    resp = req_call.do()
    if resp.code != 0:
        logging.error(
            f"reply message failed, code: {resp.code}, msg: {resp.msg}, error: {resp.error}"
        )
