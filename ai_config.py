import configparser



class Config(configparser.ConfigParser):

    def __init__(self, filename):
        super().__init__()
        self.read(filename,encoding="utf-8")

    def get_config(self, section):
        return dict(self[section])
    


if __name__ == "__main__":
    # 1.创建config对象
    # config = configparser.ConfigParser()
    config_path = "config.ini"
    config = Config(config_path)
    # 2.使用config对象读取配置文件
    config.read('config.ini')
    # 3.获取配置信息
    key = config.get('openai', 'api_key')
    # 输出配置信息
    print(f"key={key}")
