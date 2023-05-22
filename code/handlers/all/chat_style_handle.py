import logging

from EdgeGPT import ConversationStyle

from handlers import msg_handle_register, bot_register, card_handle_register
from core.bot import bot_pool, BotBase
from core.card_builder import CardBuilder, CardTemplate, Button
from core.config import global_config
from core.data_structure import MsgInfo, ActionType
from core.service import reply_message
from core.tools import get_conversation_style_string


def _get_chat_style_card():
    card_builder = CardBuilder()
    card_builder.add_header(CardTemplate.blue, title="请选择对话风格")

    buttons = []
    for style in ConversationStyle:
        buttons.append(
            Button(
                text=get_conversation_style_string(style),
                url="",
                type=Button.ButtonType.primary
                if global_config["CONVERSATION_STYLE"] == style
                else Button.ButtonType.default,
                value={"conversation_style": style.name},
            )
        )
    card_builder.add_button_group(buttons)
    card_builder.add_note(
        note_content=f"当前模式: {get_conversation_style_string(global_config['CONVERSATION_STYLE'])}"
    )
    return card_builder


@msg_handle_register.register_object(key=["/chat_style"])
def chat_style_handle(msg_info: MsgInfo):
    reply_message(msg_info.msg_id, _get_chat_style_card().build())


@card_handle_register.register_object(key="conversation_style_card")
def conversation_style_card_handle(card):
    msg_id = card.open_message_id
    action_dict = card.action.value

    global_config["CONVERSATION_STYLE"] = ConversationStyle[
        action_dict["conversation_style"]
    ]

    # reply success message
    card_builder = CardBuilder()
    card_builder.add_header(CardTemplate.green, title="设置成功")
    card_builder.add_markdown(
        f"已经将对话风格设置为: {get_conversation_style_string(ConversationStyle[action_dict['conversation_style']])}"
    )
    card_builder.add_note(note_content="仅在之后的对话中生效，之前的对话不会改变哦~")
    reply_message(msg_id, card_builder.build())

    # update card
    return _get_chat_style_card().dict()
