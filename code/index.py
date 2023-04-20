import logging
import json

from flask import Flask, request, Blueprint
from flask.helpers import make_response

from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event.model import BaseEvent
from larksuiteoapi.model import OapiHeader, OapiRequest
from larksuiteoapi.service.contact.v3 import UserUpdatedEventHandler, UserUpdatedEvent
from larksuiteoapi import (
    Store,
    Config,
    AppSettings,
    Logger,
    LEVEL_DEBUG,
    LEVEL_INFO,
    LEVEL_WARN,
    LEVEL_ERROR,
    DefaultLogger,
    Context,
    DOMAIN_FEISHU,
    DOMAIN_LARK_SUITE,
)

from core.config import global_config
from core.tools import decrypt_message

app = Flask(__name__)

app_settings = Config.new_internal_app_settings(
    app_id=global_config["APP_ID"],
    app_secret=global_config["APP_SECRET"],
    verification_token=global_config["APP_VERIFICATION_TOKEN"],
    encrypt_key=global_config["APP_ENCRYPT_KEY"],
    #  help_desk_id="HelpDeskID",
    #  help_desk_token="HelpDeskToken",
)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
conf = Config.new_config_with_memory_store(
    DOMAIN_FEISHU, app_settings, DefaultLogger(), LEVEL_DEBUG
)


@app.route("/webhook/event", methods=["GET", "POST"])
def event_handler():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_event(conf, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


def handle(ctx, conf, card):
    return {
        "config": {"wide_screen_mode": True},
        "card_link": {
            "url": "https://www.baidu.com",
            "android_url": "https://developer.android.com/",
            "ios_url": "https://developer.apple.com/",
            "pc_url": "https://www.windows.com",
        },
        "header": {"title": {"tag": "plain_text", "content": "this is header"}},
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": "This is a very very very very very very very long text;",
                },
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "Read"},
                        "type": "default",
                    }
                ],
            },
        ],
    }


set_card_callback(conf, handle)


@app.route("/webhook/card", methods=["GET", "POST"])
def card_handler():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_card(conf, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
