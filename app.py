# coding:utf-8

import json
import os

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from utils.event_utils import EventManager, UrlVerificationEvent, MessageReceiveEvent
from utils.log_utils import init_env

from utils.variables import LOGGER
from utils.feishu_api import FeiShuAPI
from model import db_wrapper, Task, DATABASE, create_app

load_dotenv()
init_env()
app = create_app()

# If we want to exclude particular views from the automatic connection
# management, we list them this way:
FLASKDB_EXCLUDED_ROUTES = ('logout',)

peewee_db = db_wrapper.database

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY")
MAX_THREAD_NUM = int(os.getenv("MAX_THREAD_NUM", 5))
feishu_api = FeiShuAPI(APP_ID, APP_SECRET)

event_manager = EventManager()


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        LOGGER.warning("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    LOGGER.info("openid %s", open_id)
    LOGGER.info("message %s", req_data)
    text_content = json.loads(message.content)["text"]
    if text_content.startswith("@"):
        text_content = text_content.split(" ", 1)[-1]
    with db_wrapper.database.atomic():
        Task.create(user=open_id, params=json.dumps({"prompt": text_content}), status="init",
                    task_type="imagine", chat_type=message.chat_type,
                    chat_id=message.chat_id, message_id=message.message_id)
    access_token = feishu_api.get_tenant_access_token()["tenant_access_token"]
    feishu_api.set_access_token(access_token)
    feishu_api.reply_message(message.message_id, json.dumps({"text": "图片生成中请稍后。。。"}), msg_type="text")
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    LOGGER.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/message", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)
    return event_handler(event)


@app.route("/create_task", methods=["POST"])
def create_task():
    t = request.json["text"]
    with db_wrapper.database.atomic():
        Task.create(user="ou_903c5bc25e57543d52c6869634fa681c", params=json.dumps({"prompt": t}), status="init",
                    task_type="imagine")
    return jsonify({})


@app.route("/card_message", methods=["POST"])
def card_message():
    try:
        LOGGER.info("get card message")
        args = request.args  # args 请求的参数
        args_dict = args.to_dict()  # 获取请求参数 字典格式
        LOGGER.info("args %s", args_dict)
        LOGGER.info("card message %s", request.json)
        action = request.json.get("action", "")

        if action:
            open_id = request.json["open_id"]
            open_message_id = request.json["open_message_id"]
            open_chat_id = request.json["open_chat_id"]
            action_value = action.get("value", {})
            task_action = action_value.get("action", "")
            # "upscale", "variation"
            if task_action and task_action.startswith("u"):
                with db_wrapper.database.atomic():
                    Task.create(user=open_id, params=json.dumps(action_value), status="init",
                                task_type="upscale", chat_id=open_chat_id, chat_type="",
                                message_id=open_message_id)
            elif task_action and task_action.startswith("v"):
                with db_wrapper.database.atomic():
                    Task.create(user=open_id, params=json.dumps(action_value), status="init",
                                task_type="variation", chat_id=open_chat_id, chat_type="",
                                message_id=open_message_id)
            else:
                return "BAD REQUEST", 400
            access_token = feishu_api.get_tenant_access_token()["tenant_access_token"]
            feishu_api.set_access_token(access_token)
            feishu_api.reply_message(open_message_id, json.dumps({"text": "图片生成中请稍后。。。"}), msg_type="text")
        return jsonify({"challenge": request.json.get("challenge", "")})
    except:
        LOGGER.error("card_message error", exc_info=True)
        return jsonify({})


def main():
    app.run()


if __name__ == "__main__":
    main()
