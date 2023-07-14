# coding:utf-8
import json
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class AuthenticationFailureException(Exception):
    pass


class RequestFailException(Exception):
    pass


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CGTEAMWORK_REQUEST_TIMEOUT = 20


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_maxsize=50)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class CheckStatusCode:
    def __init__(self, func):
        self.func = func
        self.cur_result = None

    def __call__(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs["timeout"] = CGTEAMWORK_REQUEST_TIMEOUT
        need_raw_content = kwargs.pop("need_raw_content", False)
    #     kwargs["proxy"] = {
    # 'http':'127.0.0.1:7890',
    # 'https':'127.0.0.1:7890'
    # }
        result = self.func(*args, **kwargs)
        # print(result.request.body)
        self.cur_result = result
        if result.status_code == 401:
            raise AuthenticationFailureException("authentication failed")
        elif result.status_code // 100 == 5 or result.status_code // 100 == 4:
            # TODO： 结果中含有中文不知何种编码
            error_message = {"status_code": result.status_code, "reason": result.content.decode("utf-8")}
            raise RequestFailException(error_message)
        else:
            if need_raw_content:
                result_raw = result.content
                result.close()
                return result_raw
            # print(result.content)
            json_data = result.json()
            result.close()
            return json_data


class CustomSession(object):
    def __init__(self):
        self.session = requests_retry_session()
        self.get = CheckStatusCode(self.session.get)
        self.put = CheckStatusCode(self.session.put)
        self.post = CheckStatusCode(self.session.post)
        self.delete = CheckStatusCode(self.session.delete)
        self.options = CheckStatusCode(self.session.options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class CommonAPIWrapper:
    host = None
    def __init__(self, host=None):
        self.host = host if host else self.host
        self.current_res = None
        self.access_token = None
        self.session = CustomSession()

    def common_call(self, path, data=None, json_=None, params=None, headers=None, method="GET", add_auth=True,
                    files=None, need_raw_content=False):
        url = urljoin(self.host, path)
        if json_ is not None:
            data = json.dumps(json_)
            json_ = None
            if headers is None:
                headers = {'Content-Type': 'application/json'}
            else:
                headers["Content-Type"] = 'application/json'
        func = getattr(self.session, method.lower())
        request_data = dict(url=url, data=data, json=json_, params=params,
                            headers=headers, files=files, need_raw_content=need_raw_content)
        res = func(**request_data)

        self.current_res = func.cur_result
        return res

def main():
    pass


if __name__ == "__main__":
    main()
