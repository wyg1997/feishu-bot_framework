import logging

from handlers.register import msg_handle_register
from core.data_structure import MsgInfo
from core.service import reply_message
from core.card_builder import CardBuilder, CardTemplate


@msg_handle_register.register_object(key=["/help", "/start", "帮助"])
def helper_handle(msg_info: MsgInfo):
    logging.info(f"helper_handle, msg_info: {msg_info}")
    card_builder = CardBuilder().add_markdown("🤖️ 我是必应，有问题直接@我对话哦~")
    reply_message(msg_info, content=card_builder.build())
