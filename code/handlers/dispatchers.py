import logging
from typing import Union

from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler
from larksuiteoapi.card.card import set_card_callback

from core.data_structure import HandlerType, MessageType, parse_msg_info
from core.config import sdk_config
from core.service import reply_message
from core.card_builder import CardBuilder, CardTemplate
from handlers import msg_handle_register, card_handle_register


_msg_cache = set()


def message_receive_event_dispatcher(ctx, conf, event):
    msg_info = parse_msg_info(event)

    # Ignore message from group and not mentioned bot
    if msg_info.handler_type == HandlerType.group and not msg_info.is_mentioned:
        return None

    # TODO: support the message which is not text
    if msg_info.msg_type != MessageType.text:
        return None

    if msg_info.msg_id in _msg_cache:
        return None

    # avoid repeated message
    if len(_msg_cache) > 1000:
        _msg_cache.clear()
    _msg_cache.add(msg_info.msg_id)

    try:
        if msg_info.text in msg_handle_register:
            return msg_handle_register.get(msg_info.text, force=True)(msg_info)
        else:
            return msg_handle_register.get("/chat", force=True)(msg_info)
    except Exception as e:
        card_builder = (
            CardBuilder().add_markdown(str(e)).add_header(CardTemplate.red, "⛔️ 出错啦")
        )
        return reply_message(msg_info.msg_id, content=card_builder.build())


MessageReceiveEventHandler.set_callback(sdk_config, message_receive_event_dispatcher)


def card_dispatcher(ctx, conf, card) -> Union[dict, None]:
    """
    Process message card.

    If you want to update the card, you can return a dict object.
    Otherwise, return None and do nothing.
    """
    logging.info(f"Get card: {card}")

    action_dict = card.action.value
    try:
        if "conversation_style" in action_dict:
            handle = card_handle_register.get("conversation_style_card", force=True)
        else:
            raise ValueError(f"Unknown card type, action_dict: {action_dict}")
        return handle(card)
    except Exception as e:
        card_builder = (
            CardBuilder().add_markdown(str(e)).add_header(CardTemplate.red, "⛔️ 出错啦")
        )
        return reply_message(msg_id=card.open_message_id, content=card_builder.build())


set_card_callback(sdk_config, card_dispatcher)
