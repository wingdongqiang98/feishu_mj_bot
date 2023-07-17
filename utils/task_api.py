# coding:utf-8
import json
import time

import requests
from urllib.parse import urljoin
from utils.common_api import CommonAPIWrapper


class MJApi(CommonAPIWrapper):
    def __init__(self, api_key, host="https://mj-api.kangtaiboshi.com/"):
        super().__init__(host=host)
        self.apikey = api_key
        self.current_res = None

    def common_call(self, path, data=None, json_=None, params=None, headers=None, method="GET", add_auth=True,
                    files=None, need_raw_content=False):
        if headers is None:
            headers = {"apikey": self.apikey}
        else:
            headers.update({"apikey": self.apikey})
        return super().common_call(path, data=data, json_=json_,
                                params=params, headers=headers,
                                method=method, add_auth=add_auth,
                                files=files, need_raw_content=need_raw_content)

    def create_task(self, prompt):
        path = "/imagine"
        params = {"prompt": prompt}
        return self.common_call(path, params=params)

    def query_task(self, task_id):
        path = "/task"
        params = {"task_id": task_id}
        return self.common_call(path, params=params)

    def child_task(self, task_id, action):
        path = "/task_update"
        params = {"task_id": task_id, "action": action}
        return self.common_call(path, params=params)


def main():
    mj = MJApi()
    # task_id = mj.create_task("Photography in the style of Erik Madigan Heck and Sonia Delaunay, Beksinski, surrealism, Translucent, reflection, mirrorlike, Lime green and blue")["data"]["task_id"]
    task_id = mj.child_task("5633266506608855", "u1")["data"]["task_id"]
    print(task_id)
    while True:
        print(mj.query_task(task_id))
        time.sleep(3)


if __name__ == "__main__":
    main()
