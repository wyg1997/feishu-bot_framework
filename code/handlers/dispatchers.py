from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler

from core.data_structure import HandlerType, MessageType, parse_msg_info
from core.config import sdk_config
from handlers.register import msg_handle_register


def message_receive_event_dispatcher(ctx, conf, event):
    msg_info = parse_msg_info(event)

    # Ignore message from group and not mentioned bot
    if msg_info.handler_type == HandlerType.kGroup and not msg_info.is_mentioned:
        return None

    # TODO: support the message which is not text
    if msg_info.msg_type != MessageType.kText:
        return None

    if msg_info.text in msg_handle_register:
        return msg_handle_register.get(msg_info.text, force=True)(msg_info)
    else:
        return msg_handle_register.get("/default", force=True)(msg_info)


MessageReceiveEventHandler.set_callback(sdk_config, message_receive_event_dispatcher)
