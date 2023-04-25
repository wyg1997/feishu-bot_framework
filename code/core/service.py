import logging
import json
from larksuiteoapi.service.im.v1 import model

from core.data_structure import MsgInfo, MessageType
from core.config import service


def reply_message(msg_info: MsgInfo, **content_dict):
    content = json.dumps(content_dict)

    body = model.MessageReplyReqBody()
    body.content = content
    body.msg_type = MessageType.text.name

    req_call = service.messages.reply(body)
    req_call.set_message_id(str(msg_info.msg_id))

    resp = req_call.do()
    if resp.code != 0:
        logging.error(
            f"reply message failed, code: {resp.code}, msg: {resp.msg}, error: {resp.error}"
        )
