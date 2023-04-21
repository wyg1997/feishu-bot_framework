import json
import regex


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
