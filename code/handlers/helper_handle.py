import logging
from larksuiteoapi.api import Request
from larksuiteoapi.service.im.v1 import model

from handlers.register import msg_handle_register
from core.data_structure import MsgInfo, MessageType
from core.config import sdk_config, service


@msg_handle_register.register_handle(keys=["/help", "/start", "帮助"])
def helper_handle(msg_info: MsgInfo):
    body = model.MessageReplyReqBody()
    body.content = '{"text": "Hellow world!"}'
    body.msg_type = MessageType.text.name

    req_call = service.messages.reply(body)
    req_call.set_message_id(str(msg_info.msg_id))

    resp = req_call.do()
    if resp.code != 0:
        logging.error(
            f"reply message failed, code: {resp.code}, msg: {resp.msg}, error: {resp.error}"
        )
