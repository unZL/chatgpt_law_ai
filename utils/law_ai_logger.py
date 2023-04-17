# -*- encoding:utf-8 -*-
import logging
import logging.config

class ai_log:
    def __init__(self, filename,logName):
        super().__init__()
        # 加载配置文件
        logging.config.fileConfig(filename)
        # 创建一个 logger 对象
        self.logger = logging.getLogger(logName)

if __name__ == "__main__":
    filename = "logging.ini"
    logName = "test"
    ai_log_name = ai_log(filename,logName)
    ai_log_name.logger.info("yes!")

