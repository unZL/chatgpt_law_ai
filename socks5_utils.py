import socket
import openai
import socks
import ai_config

config = ai_config.Config("config.ini")


# proxies = {
#         "http": f"socks5://{proxt_host}:{proxt_port}",
#         "https": f"socks5://{proxt_host}:{proxt_port}"
#     }
# 设置 Socks5 代理，并设置接下来程序都使用代理

class Socks5_config:
    def __init__(self,config_file):
        # 实例化 ai_config.Config 类读取配置文件，这里传入配置文件路径（字符串类型）
        self.config = ai_config.Config(config_file)
        self.proxt_host = config.get("SOCKS5","SOCKS5_PROXY_HOST")
        self.proxt_port = int(config.get("SOCKS5","SOCKS5_PROXY_PORT"))
        # 调用 use_socks5 方法，设置 Socks5 代理
        self.use_socks5()

    # 设置 Socks5 代理
    def use_socks5(self):
        # 使用 socks 模块将代理绑定到 socket 连接中
        socks.set_default_proxy(socks.SOCKS5, self.proxt_host, self.proxt_port)
        # 所有后续的 socket 连接将使用代理
        socket.socket = socks.socksocket
    
    # 下面是测试函数
    # 正常情况下使用 socks5 代理的方法 (测试用)
    def socks5_test(self):
        # 设置代理服务器的 IP 和端口号
        socks.set_default_proxy(socks.SOCKS5, self.proxt_host, self.proxt_port)
        # 测试代理服务器是否可以连接
        # 创建一个已经设置 SOCKS5 代理的 socket 连接
        s = socks.socksocket()


        # 设置 socket 连接的相关参数（可选）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 连接远程服务器 (此时连接使用已经设置 SOCKS5 代理)
        s.connect(("https://www.youtube.com/", 80))

        # 测试代理服务器是否可以连接
        

    # 在使用 OpenAI API 时
    def socks5_test_openai(self):
        # 初始化 OpenAI API 密钥
        openai.api_key = self.config.get("openai_Completion_config","api_key")

        # 执行 OpenAI API 请求
        try:  
            response = openai.Completion.create(
            model='text-davinci-003',
            prompt="100-1=?",
            temperature=0.5,
            max_tokens=300,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )

            ai_response = response.choices[0].text
            # 输出 API 响应结果
            # print(response)
            print(f"100-1=?\nai_response:{ai_response}")
            print("代理服务器有效。")
        except socket.error:
            print("代理服务器无法连接！")
        
    def print_info_proxy(self):
        proxy_info = socks.get_default_proxy()
        print(f"当前代理设置为：{proxy_info}")

        


if __name__ == "__main__":
    proxy_info = socks.get_default_proxy()
    print(f"当前代理设置为：{proxy_info}")
    print("开始设置代理服务器")
    test_socks5 = Socks5_config("config.ini")
    proxy_info = socks.get_default_proxy()
    print(f"当前代理设置为：{proxy_info}")
    test_socks5.socks5_test_openai()