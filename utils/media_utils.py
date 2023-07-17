# coding:utf-8
import io

import requests

from utils.func_utils import retry_try


@retry_try()
def download_image_io(url, timeout=60):
    response = requests.get(url, timeout=timeout)
    return io.BytesIO(response.content)


def main():
    pass


if __name__ == "__main__":
    main()
