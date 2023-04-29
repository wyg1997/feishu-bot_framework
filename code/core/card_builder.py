import enum
import json
from typing import Any, Dict


class CardTemplate(enum.Enum):
    blue = 1
    wathet = 2
    turquoise = 3
    green = 4
    yellow = 5
    orange = 6
    red = 7
    carmine = 8
    purple = 9
    indigo = 10
    gray = 11
    default = 12



# NOTE: See document: 
# https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN
class CardBuilder:
    def __init__(self):
        self.card: Dict[str, Any] = {
            "config": {
                "wide_screen_mode": True
            }
        }

    def add_header(self, template, title):
        """
        Document: https://open.feishu.cn/document/ukTMukTMukTM/ukTNwUjL5UDM14SO1ATN
        """
        self.card["header"] = {
            "template": template.name,
            "title": {
                "content": title,
                "tag": "plain_text"
            },
        }

    def add_markdown(self, content, text_align="left"):
        """
        Document: https://open.feishu.cn/document/ukTMukTMukTM/uYDN1UjL2QTN14iN0UTN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        assert text_align in ["left", "center", "right"], \
          f'text_align must be one of "left", "center", "right", but got {text_align}'

        self.card["elements"].append({
            "tag": "markdown",
            "content": content,
            "text_align": text_align,
        })

    def add_image(self, img_key, content="", mode="", preview="", compact_width=False):
        """
        Document: https://open.feishu.cn/document/ukTMukTMukTM/uUjNwUjL1YDM14SN2ATN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        self.card["elements"].append({
            "tag": "img",
            "img_key": img_key,
            "alt": {
                "tag": "plain_text",
                "content": content,
            },
            "mode": mode,
            "preview": preview,
            "compact_width": compact_width,
        })

    # TODO: add more elements
