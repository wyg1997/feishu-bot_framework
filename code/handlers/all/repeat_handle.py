import logging

from core.service import reply_message
from core.data_structure import MsgInfo, ActionType
from core.bot import bot_pool, BotBase
from core.card_builder import CardBuilder, CardTemplate
from handlers import msg_handle_register, bot_register


@msg_handle_register.register_object(key=["/repeat", "复读机"])
def repeat_handle(msg_info: MsgInfo):
    logging.info(f"repeat handle: msg_info: {msg_info}")
    bot_pool.ask(msg_info, ActionType.repeat)


@bot_register.register_object(key=ActionType.repeat)
class RepeatBot(BotBase):
    def _do(self, msg_info: MsgInfo):
        card_builder = CardBuilder()
        # first message
        if len(self.message_ids) == 1:
            card_builder.add_markdown("继续对话吧～").add_header(
                CardTemplate.wathet, "复读机已启动"
            )
        else:
            card_builder.add_markdown(msg_info.text)
        reply_message(msg_info, card_builder.build())
