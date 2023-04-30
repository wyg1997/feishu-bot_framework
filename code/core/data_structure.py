from enum import Enum
from dataclasses import dataclass
from core.config import global_config
from core.tools import parse_message_content
from typing import List

from larksuiteoapi.service.im.v1.model import MentionEvent


class ActionType(Enum):
    chat = 1
    image = 2
    repeat = 3


class HandlerType(Enum):
    p2p = 1
    group = 2


class MessageType(Enum):
    text = 1
    post = 2
    image = 3
    interactive = 4
    share_card = 5
    shared_user = 6
    audio = 7
    media = 8
    file = 9
    sticker = 10


@dataclass(frozen=True)
class MsgInfo(object):
    handler_type: HandlerType
    msg_type: MessageType
    msg_id: int
    root_id: int
    text: str
    is_mentioned: bool  # or all mentioned users name
    # TODO: add more properties


def _is_mentioned(mentions: MentionEvent, bot_name: str) -> bool:
    """
    Check if the bot is mentioned in the message.
    """
    if mentions is None:
        return False
    assert isinstance(mentions, List), "mentions should be a list or None"

    return any(mention.name == bot_name for mention in mentions)


def parse_msg_info(event):
    """
    Parse message info from event.
    """
    return MsgInfo(
        handler_type=HandlerType[event.event.message.chat_type],
        msg_type=MessageType[event.event.message.message_type],
        msg_id=event.event.message.message_id,
        root_id=event.event.message.root_id or event.event.message.message_id,
        text=parse_message_content(event.event.message.content),
        is_mentioned=_is_mentioned(
            event.event.message.mentions, global_config["BOT_NAME"]
        ),
    )
