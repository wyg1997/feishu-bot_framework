import enum
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Union, Tuple


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


@dataclass(frozen=True)
class Button:
    """
    Document:
        https://open.feishu.cn/document/ukTMukTMukTM/uEzNwUjLxcDM14SM3ATN
    """

    class ButtonType(enum.Enum):
        primary = 1
        default = 2
        danger = 3

    text: str
    url: str = ""
    type: ButtonType = ButtonType.default
    android_url: str = ""
    ios_url: str = ""
    pc_url: str = ""
    value: Union[None, Dict[str, Any]] = field(default=None)
    # set confirm windows title and text
    confirm: Union[None, Tuple[str, str]] = None

    def to_dict(self):
        data = {
            "tag": "button",
            "text": {"tag": "plain_text", "content": self.text},
            "type": self.type.name,
        }
        if self.value is not None:
            data["value"] = self.value
        if any([self.url, self.android_url, self.ios_url, self.pc_url]):
            data["multi_url"] = {
                "url": self.url,
                "android_url": self.android_url,
                "ios_url": self.ios_url,
                "pc_url": self.pc_url,
            }
        if self.confirm is not None:
            data["confirm"] = {
                "title": {"tag": "plain_text", "content": self.confirm[0]},
                "text": {"tag": "plain_text", "content": self.confirm[1]},
            }
        return data


# NOTE: See document:
# https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN
class CardBuilder:
    def __init__(self):
        self.card: Dict[str, Any] = {"config": {"wide_screen_mode": True}}

    def build(self) -> str:
        return json.dumps(self.card)

    def dict(self) -> Dict[str, Any]:
        return self.card

    def add_header(self, template: Union[str, CardTemplate], title: str):
        """
        Document:
            https://open.feishu.cn/document/ukTMukTMukTM/ukTNwUjL5UDM14SO1ATN
        """
        assert "header" not in self.card, "header already exists"
        if isinstance(template, CardTemplate):
            template = template.name
        self.card["header"] = {
            "template": template,
            "title": {"content": title, "tag": "plain_text"},
        }
        return self

    def add_markdown(self, content: str, text_align="left"):
        """
        Document:
            https://open.feishu.cn/document/ukTMukTMukTM/uYDN1UjL2QTN14iN0UTN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        assert text_align in [
            "left",
            "center",
            "right",
        ], f'text_align must be one of "left", "center", "right", but got {text_align}'

        self.card["elements"].append(
            {
                "tag": "markdown",
                "content": content,
                "text_align": text_align,
            }
        )
        return self

    def add_image(
        self,
        img_key: str,
        content: str = "",
        mode: str = "fit_horizontal",
        preview="",
        compact_width=False,
    ):
        """
        Document:
            https://open.feishu.cn/document/ukTMukTMukTM/uUjNwUjL1YDM14SN2ATN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        self.card["elements"].append(
            {
                "tag": "img",
                "img_key": img_key,
                "alt": {
                    "tag": "plain_text",
                    "content": content,
                },
                "mode": mode,
                "preview": preview,
                "compact_width": compact_width,
            }
        )
        return self

    def add_dividing_line(self):
        """
        Document:
            https://open.feishu.cn/document/ukTMukTMukTM/uQjNwUjL0YDM14CN2ATN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        self.card["elements"].append(
            {
                "tag": "hr",
            }
        )
        return self

    def add_note(
        self,
        note_content,
        *,
        img_key="img_v2_041b28e3-5680-48c2-9af2-497ace79333g",
        img_content="",
    ):
        """
        Document:
            https://open.feishu.cn/document/ukTMukTMukTM/ucjNwUjL3YDM14yN2ATN
        """
        if "elements" not in self.card:
            self.card["elements"] = []

        self.card["elements"].append(
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "img",
                        "img_key": img_key,
                        "alt": {
                            "tag": "plain_text",
                            "content": img_content,
                        },
                    },
                    {
                        "tag": "plain_text",
                        "content": note_content,
                    },
                ],
            }
        )
        return self

    def add_button_group(self, buttons, *, layout="default"):
        assert layout in (
            "default",
            "bisected",
            "trisection",
            "flow",
        ), f'layout must be one of "default", "bisected", "trisection", "flow", but got {layout}'

        if "elements" not in self.card:
            self.card["elements"] = []

        self.card["elements"].append(
            {
                "tag": "action",
                "actions": [button.to_dict() for button in buttons],
                "layout": layout,
            }
        )
        return self

    # TODO: add more elements
