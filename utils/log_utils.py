# coding:utf-8
import os
import logging
from logging.handlers import RotatingFileHandler

_LOGGER = logging.getLogger()


def init_env(filename="feishu_mj_bot.log"):
    log_dir = os.path.join(os.path.abspath(os.path.curdir), "log")
    log_file = os.path.join(log_dir, filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_config_dict = {}
    fmt = "%(levelname)s,%(name)s %(asctime)s %(module)s,%(lineno)s %(message)s"
    # todo:debug
    level = "INFO"
    log_config_dict[
        "format"] = fmt
    log_config_dict["level"] = level
    logging.basicConfig(**log_config_dict)
    _LOGGER.info('get log config dict %s', log_config_dict)

    file_rotaing_handler = RotatingFileHandler(
        filename=log_file,
        backupCount=10,
        maxBytes=1024 * 1024 * 50,
        encoding='utf-8'
    )
    file_rotaing_handler.setLevel(level)
    formatter = logging.Formatter(fmt)
    file_rotaing_handler.setFormatter(formatter)
    _LOGGER.addHandler(file_rotaing_handler)



def main():
    pass


if __name__ == "__main__":
    main()
