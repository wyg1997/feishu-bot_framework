__import__("pkg_resources").declare_namespace(__name__)

from core.register import Register

msg_handle_register = Register(name="event handle register")
card_handle_register = Register(name="card handle register")
bot_register = Register(name="bot register")

from handlers.all import *
