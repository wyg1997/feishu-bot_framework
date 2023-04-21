from handlers.register import msg_handle_register
from core.data_structure import MsgInfo


@msg_handle_register.register_handle(keys=["/help", "/start", "帮助"])
def helper_handle(msg_info: MsgInfo):
    raise NotImplementedError()
