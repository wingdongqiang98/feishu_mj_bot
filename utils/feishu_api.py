# coding:utf-8
import json
import os.path
import time

import urllib.parse

from utils.common_api import CommonAPIWrapper


class FeiShuAPI(CommonAPIWrapper):
    def __init__(self, app_id, app_secret, host="https://open.feishu.cn"):
        super().__init__(host=host)
        self.host = host
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire_time = None

    def add_auth(self, data):
        return data

    def set_access_token(self, token):
        self.access_token = token

    def common_call(self, path, data=None, json_=None, params=None, headers=None, method="GET", add_auth=True,
                    files=None, need_raw_content=False):

        if add_auth:
            if headers is None:
                headers = {}
            headers.update({"Authorization": f"Bearer {self.access_token}"})
        result = super().common_call(path, data=data, json_=json_, params=params, headers=headers,
                                     method=method,
                                     add_auth=add_auth,
                                     files=files, need_raw_content=need_raw_content)
        if result["code"] != 0:
            raise Exception(result["msg"])
        return result

    def get_tenant_access_token(self):
        path = '/open-apis/auth/v3/tenant_access_token/internal'
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        return self.common_call(path, data=data, add_auth=False, method="POST")

    def send_message(self, receive_id, content, msg_type="image", receive_id_type="open_id"):
        path = '/open-apis/im/v1/messages'
        params = {
            "receive_id_type": receive_id_type,
        }
        data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content,
        }
        return self.common_call(path, json_=data, params=params, method="POST")

    def upload_image(self, image, file_name):
        # {'code': 0, 'data': {'image_key': 'img_v2_1fb2f72f-80dd-4ab4-b6d6-1557cef165bg'}, 'msg': 'success'}
        path = '/open-apis/im/v1/images'
        data = {'image_type': 'message',
                }
        files = [
            ('image', (file_name, image, 'application/json'))
        ]
        return self.common_call(path, data=data, method="POST", files=files)

    def reply_message(self, message_id, content, msg_type="image"):
        path = f'/open-apis/im/v1/messages/{message_id}/reply'
        data = {
            "msg_type": msg_type,
            "content": content,
        }
        return self.common_call(path, json_=data, method="POST")




def main():
    pass


if __name__ == "__main__":
    main()
