from functools import wraps
import time


def do_again_decorator(func):
    """
    如果func函数异常，则 进程停止20s，然后再次运行func函数，防止服务器反应时间过长，导致程序失败
    :param func: 被装饰的函数
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print(f'{"-" * 80:^100}')
            print(f'function {func.__name__} run failed! now suspend 20 seconds')
            time.sleep(20)
            print(f'function {func.__name__} run again')
            return func(*args, **kwargs)
    return wrapper
