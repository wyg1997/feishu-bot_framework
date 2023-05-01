import json

import regex
from EdgeGPT import ConversationStyle


def parse_message_content(content: str):
    """
    Parse request effective content.

    For example:
        content = '{"text":"@_user_1  hahaha"}'
    """
    data = json.loads(content)
    if "text" not in data:
        return ""

    # remove @user
    return regex.sub(r"@[^ ]*", "", data["text"]).strip()


_conversation_style_map = {
    ConversationStyle.creative: "创造性",
    ConversationStyle.balanced: "均衡",
    ConversationStyle.precise: "精准",
}


def get_conversation_style_string(style):
    return f"{style.name}({_conversation_style_map[style]})"
