import logging

from flask import Flask, request, Blueprint
from flask.helpers import make_response

# TODO: remove useless import
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.api import (
    Request,
    FormData,
    FormDataFile,
    set_timeout,
    set_path_params,
    set_query_params,
    set_is_response_stream,
    set_response_stream,
    set_tenant_key,
)
from larksuiteoapi.event.model import BaseEvent
from larksuiteoapi.model import OapiHeader, OapiRequest
from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler
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
    Config,
    ACCESS_TOKEN_TYPE_TENANT,
    ACCESS_TOKEN_TYPE_USER,
    ACCESS_TOKEN_TYPE_APP,
    DOMAIN_FEISHU,
    LEVEL_ERROR,
    LEVEL_DEBUG,
)

from core.config import sdk_config


app = Flask(__name__)

#  @attr.s
#  class Message(object):
#      message_id = attr.ib(type=str)


#  def send_message(body=None):
#      body = {
#          "user_id": "",
#          "msg_type": "interactive",
#          "card": {
#              "config": {"wide_screen_mode": True},
#              "elements": [
#                  {
#                      "tag": "div",
#                      "text": {
#                          "tag": "lark_md",
#                          "content": "[飞书](https://www.feishu.cn)整合即时沟通、日历、音视频会议、云文档、云盘、工作台等功能于一体，成就组织和个人，更高效、更愉悦。",
#                      },
#                  },
#                  {
#                      "tag": "action",
#                      "actions": [
#                          {
#                              "tag": "button",
#                              "value": {"value": 1, "value2": "str"},
#                              "text": {"tag": "plain_text", "content": "主按钮"},
#                              "type": "primary",
#                          },
#                          {
#                              "tag": "button",
#                              "text": {"tag": "plain_text", "content": "次按钮"},
#                              "type": "default",
#                          },
#                          {
#                              "tag": "button",
#                              "text": {"tag": "plain_text", "content": "危险按钮"},
#                              "type": "danger",
#                          },
#                      ],
#                  },
#              ],
#          },
#      }

#      req = Request(
#          "/open-apis/message/v4/send",
#          "POST",
#          ACCESS_TOKEN_TYPE_TENANT,
#          body,
#          output_class=Message,
#          request_opts=[set_timeout(3)],
#      )
#      resp = req.do(conf)
#      print("header = %s" % resp.get_header().items())
#      print("request id = %s" % resp.get_request_id())
#      print(resp)
#      if resp.code == 0:
#          print(resp.data.message_id)
#      else:
#          print(resp.msg)
#          print(resp.error)


#  def message_receive_callback(ctx, conf, event):
#      print(f"{ctx=}")
#      print(f"{conf=}")
#      print(f"{event=}")
#      send_message()


#  MessageReceiveEventHandler.set_callback(conf, message_receive_callback)


@app.route("/webhook/event", methods=["GET", "POST"])
def event_handler():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_event(sdk_config, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


@app.route("/webhook/card", methods=["GET", "POST"])
def card_handler():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_card(sdk_config, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
