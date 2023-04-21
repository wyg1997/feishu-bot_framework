from handlers.register import msg_handle_register
from core.data_structure import MsgInfo


@msg_handle_register.register_handle(keys=["/default"])
def new_bing_handle(msg_info: MsgInfo):
    raise NotImplementedError()
