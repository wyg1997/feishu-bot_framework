from enum import Enum
from dataclasses import dataclass
from core.config import global_config
from typing import List

from larksuiteoapi.service.im.v1.model import MentionEvent


class HandlerType(Enum):
    kPersonal = 1
    kGroup = 2


class MessageType(Enum):
    kText = 1
    kOther = 2


@dataclass(frozen=True)
class MsgInfo(object):
    handler_type: HandlerType
    msg_type: MessageType
    msg_id: int
    chat_id: int
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
        # handler type
        handler_type=HandlerType.kPersonal
        if event.event.message.chat_type == "user"
        else HandlerType.kGroup,
        # message type
        msg_type=MessageType.kText
        if event.event.message.message_type == "text"
        else MessageType.kOther,
        # other info
        msg_id=event.event.message.message_id,
        chat_id=event.event.message.chat_id,
        text=event.event.message.content.text.strip(),
        is_mentioned=_is_mentioned(
            event.event.message.mentions, global_config["bot_name"]
        ),
    )
