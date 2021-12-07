import logging
import datetime


class Logger:
    # 在一次进程中只存在一个
    __instance = None

    def __init__(self):
        # 创建一个日志对象
        self.logger = logging.getLogger(__name__)
        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler , 用于写入日志文件
        path = datetime.datetime.today().strftime('%Y-%m-%d')

        file_handler = logging.FileHandler(f'./logs/{path}.log', mode='w')
        file_handler.setLevel(logging.DEBUG)

        # 创建一个handler，用于输出到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(levelname)s|%(asctime)s|%(filename)s|%(message)s'
        )

        # 将格式添加到handler
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # 将handler 添加到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    # 静态方法类可以直接调用
    @staticmethod
    def get_logger():
        # 返回日志实例
        if Logger.__instance is None:
            Logger.__instance = Logger()
        return Logger.__instance.logger


logger = Logger.get_logger()

