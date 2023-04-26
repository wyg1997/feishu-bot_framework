from flask import Flask, request
from flask.helpers import make_response

from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event.model import BaseEvent
from larksuiteoapi.model import OapiHeader, OapiRequest
from larksuiteoapi.service.im.v1 import MessageReceiveEventHandler

from core.config import sdk_config
from handlers.dispatchers import message_receive_event_dispatcher


app = Flask(__name__)

MessageReceiveEventHandler.set_callback(sdk_config, message_receive_event_dispatcher)


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
