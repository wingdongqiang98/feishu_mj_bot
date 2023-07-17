# coding:utf-8
from utils.variables import LOGGER


def error_cap(error_return=None):
    def wrap(func):
        def wrapper(*args, **kwargs):
            try:
                LOGGER.info(f"{func.__name__} params args %s kwargs %s", args, kwargs)
                return func(*args, **kwargs)
            except:
                LOGGER.error(f"{func.__name__} run error", exc_info=True)
                return error_return
        return wrapper
    return wrap


class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)


def retry_try(times=3):
    def wrapp(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except:
                    if i >= times-1:
                        raise

        return wrapper
    return wrapp

def main():
    pass


if __name__ == "__main__":
    main()
