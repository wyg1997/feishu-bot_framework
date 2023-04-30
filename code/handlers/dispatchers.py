from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler

from core.data_structure import HandlerType, MessageType, parse_msg_info
from core.config import sdk_config
from core.service import reply_message
from core.card_builder import CardBuilder, CardTemplate
from handlers import msg_handle_register


_chat_cache = set()


def message_receive_event_dispatcher(ctx, conf, event):
    msg_info = parse_msg_info(event)

    # Ignore message from group and not mentioned bot
    if msg_info.handler_type == HandlerType.group and not msg_info.is_mentioned:
        return None

    # TODO: support the message which is not text
    if msg_info.msg_type != MessageType.text:
        return None

    if msg_info.chat_id in _chat_cache:
        return None

    # avoid repeated message
    if len(_chat_cache) > 1000:
        _chat_cache.clear()
    _chat_cache.add(msg_info.chat_id)

    try:
        if msg_info.text in msg_handle_register:
            return msg_handle_register.get(msg_info.text, force=True)(msg_info)
        else:
            return msg_handle_register.get("/chat", force=True)(msg_info)
    except Exception as e:
        card_builder = (
            CardBuilder().add_markdown(str(e)).add_header(CardTemplate.red, "⛔️ 出错啦")
        )
        return reply_message(msg_info, content=card_builder.build())


MessageReceiveEventHandler.set_callback(sdk_config, message_receive_event_dispatcher)
