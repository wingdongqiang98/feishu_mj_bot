# coding:utf-8
import datetime
import json
import os
import threading
import time
from multiprocessing import Process

from dotenv import load_dotenv
load_dotenv()

from utils.feishu_api import FeiShuAPI
from utils.log_utils import init_env
from utils.media_utils import download_image_io
from utils.task_api import MJApi
from utils.variables import LOGGER, CARD_MSG_TEMPLATE
from utils.func_utils import error_cap
threads = []


APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")
VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY")
MAX_THREAD_NUM = int(os.getenv("MAX_THREAD_NUM", 5))
feishu_api = FeiShuAPI(APP_ID, APP_SECRET)
from model import Task, initialize_db
initialize_db()


@error_cap()
def send_text_msg(msg, user):
    LOGGER.info("will send msg %s to user %s", msg, user)
    print("********", repr(msg), repr(user))
    access_token = feishu_api.get_tenant_access_token()["tenant_access_token"]
    feishu_api.set_access_token(access_token)
    feishu_api.send_message(user, json.dumps({"text": msg}), msg_type="text")


def process_task(task_params, task_type, task_id, user_id, chat_type, chat_id, message_id):
    try:
        init_env(filename="feishu_mj_bot_thread.log")
        Task.update(status="schedule").where(Task.id == task_id).execute()
        api = MJApi(os.getenv("MJ_TASK_APIKEY"))
        task_params = json.loads(task_params)
        LOGGER.info("task %s params %s", task_id, task_params)
        if task_type == "imagine":
            mj_task_id = api.create_task(**task_params)["data"]["task_id"]
        elif task_type in ["upscale", "variation"]:
            mj_task_id = api.child_task(**task_params)["data"]["task_id"]
        else:
            raise Exception("not support task type %s" % task_type)
        timeout = int(os.getenv("TASK_TIMEOUT", "600"))
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                Task.update(status="error", desc="timeout").where(Task.id == task_id).execute()
                send_text_msg("timeout", user_id)
                break
            result = api.query_task(mj_task_id)
            status = result["data"]["status"]
            Task.update(status=status).where(Task.id == task_id).execute()
            if result["data"]["status"] == "finished":
                access_token = feishu_api.get_tenant_access_token()["tenant_access_token"]
                feishu_api.set_access_token(access_token)
                image_url = result["data"]["image_url"]
                image_io = download_image_io(image_url)
                image_key = feishu_api.upload_image(image_io, os.path.basename(image_url))["data"]["image_key"]
                if task_type in ["upscale", "variation"]:
                    if chat_type == "group":
                       feishu_api.reply_message(message_id, "{\"image_key\": \"%s\"}" % image_key) 
                    else:
                        feishu_api.send_message(chat_id, "{\"image_key\": \"%s\"}" % image_key, receive_id_type="chat_id")
                else:
                    msg = CARD_MSG_TEMPLATE.replace("${img_key}", image_key).replace("${task_id}", mj_task_id)
                    if chat_type == "group":
                        feishu_api.reply_message(message_id, msg, msg_type="interactive") 
                    else:
                        feishu_api.send_message(chat_id, msg, msg_type="interactive")
                break
            if result["data"]["status"] == "error":
                msg = result.get("msg", "")
                Task.update(status="error", desc=msg).where(Task.id == task_id).execute()
                send_text_msg(msg, user_id)
                break
            time.sleep(1)
    except Exception as e:
        Task.update(status="error", desc=str(e)).where(Task.id == task_id).execute()
        send_text_msg(str(e), user_id)
        LOGGER.error("run error", exc_info=True)


@error_cap()
def delete_old_data():
    check_time = datetime.datetime.now() - datetime.timedelta(days=7)
    query = Task.delete().where(Task.timestamp < check_time)
    query.execute()


def process_tasks():
    init_env()
    time.sleep(10)
    while True:
        try:
            delete_old_data()
            tasks = Task.select().where(Task.status == "init", Task.retry_count <= 3)
            for t in tasks:
                if len(threads) >= MAX_THREAD_NUM:
                    LOGGER.warning("max thread !")
                    continue
                th = threading.Thread(target=process_task, args=(t.params, t.task_type, t.id, t.user, t.chat_type,
                                                                    t.chat_id, t.message_id))
                th.start()
                threads.append(th)
            for i in range(len(threads) - 1):
                t = threads[i]
                if not t.is_alive():
                    threads.pop(i)
            time.sleep(3)
        except:
            LOGGER.error("run error", exc_info=True)


def main():
    p = Process(target=process_tasks)
    p.start()
    p.join()


if __name__ == "__main__":
    main()
