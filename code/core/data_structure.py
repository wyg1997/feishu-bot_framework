from enum import Enum
from dataclasses import dataclass


class HandlerType(Enum):
    kPersonal = 1
    kGroup = 2


@dataclass(frozen=True)
class MsgInfo(object):
    handler_type: HandlerType
    msg_type: str
    msg_id: int
    chat_id: int
    text: str
    is_mentioned: bool  # or all mentioned users name
    # TODO: add more properties
