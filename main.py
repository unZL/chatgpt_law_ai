from fastapi import FastAPI, Depends
from uvicorn import Config, Server
import utils.ai_config as ai_config
import openai
# import socks5_utils
import utils.law_ai_logger as law_ai_logger
from pydantic import BaseModel
import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
import logging
import utils.openai_utils as openai_utils
from functools import lru_cache
# import sys
# 已经使用logging配置，这里弃用
# # 设置日志级别为 DEBUG（调试模式）
# logging.basicConfig(level=logging.DEBUG)

config_file_path = "config.ini"
log_config_file_path = "logging.ini"
log_name = "ai_app"
ai_log = law_ai_logger.ai_log(log_config_file_path,log_name)

openai_logger = logging.getLogger('openai')
openai_logger.addHandler(logging.handlers.TimedRotatingFileHandler('./log/chatgpt_law_ai_log.log'))

# 创建一个 FastAPI 对象
app = FastAPI()

# 如果出现连接失败，请使用代理
# 不使用代理有可能被封禁
# 下面的函数将开启 socks5 代理

# 在服务器启动前执行此函数
async def before_server_start():
    # 可以在此处执行一些初始化操作
    print("服务器正在启动中……")
    
    # 下面的函数将开启 socks5 代理 如不需要请将其注释
    # socks5_config = socks5_utils.Socks5_config(config_file_path)
    # # 执行 Socks5 配置对象的初始化方法
    # # socks5_config.init()
    # # 打印代理信息
    # socks5_config.print_info_proxy()
    print("服务器启动完成")
    print（"可以通过：localhost:端口/state 查看接口状态"）



@app.on_event("startup")
async def startup_event():
    await before_server_start()

# 读取配置文件中的 api key 并注入依赖
# 为函数提供一个缓存机制，避免重复计算，提高函数性能。
# @lru_cache(maxsize=None)
def get_config(config: ai_config.Config = Depends(lambda:ai_config.Config(config_file_path))):
    return config

# 配置读取
# 为函数提供一个缓存机制，避免重复计算，提高函数性能。
# @lru_cache(maxsize=None)
def get_config_dict(all_config):
    # all_config = ai_config.Config(config_file_path)

    # 获取各个部分的配置

    # socks5_config = all_config.get_config("SOCKS5")
    openai_api = all_config.get_config("openai_api")
    openai_completion_davinci_config = all_config.get_config("openai_Completion_davinci_config")
    openai_completion_turbo_config = all_config.get_config("openai_Completion_turbo_config")
    require_config = all_config.get_config("require_name")
    return openai_api,openai_completion_davinci_config,openai_completion_turbo_config,require_config

{
  # 使用 get 请求
    # 
    # @app.get('/get/r/{require_name}/{law_text}')
    # def text_extract(
    #     config:ai_config.Config = Depends(get_config),
    #     law_text: str = None,
    #     require_name: str = None
    #     ):
    #     openai_completion_config,require_config = get_config_dict(config)    
    #     # 启动 openai
    #     res = openai_utils.processing_demands(openai_completion_config,require_config,require_name,law_text)
    #     return res  
}

# 使用 post 请求

# 声明了一个 JSON 对象
class Law_item_require(BaseModel):
    require_name: str
    law_text: str

# 使用模型： text-davinci-003
@app.post('/post/r/')
def text_extract_davinci(
    config:ai_config.Config = Depends(get_config),
    law_item_require: Law_item_require = None
    ):
    if law_item_require == None:
        return "post == None !"
 
    openai_api,openai_completion_davinci_config,openai_completion_turbo_config,require_config = get_config_dict(config)
    # 初始化  
    davinci = openai_utils.gpt_requst_davinci(
        openai_api,
        openai_completion_davinci_config,
        law_item_require
        )
    # 通过 law_item 获取参数
    require,require_type,prompts = davinci.get_require_by_law_item(require_config)


    # 启动 openai
    res = davinci.processing_demands(require,require_type,prompts)

    return res


# 使用模型： gpt-3.5-turbo
@app.post('/post/r/turbo/')
def text_extract_turbo(
    config:ai_config.Config = Depends(get_config),
    law_item_require: Law_item_require = None
    ):
    if law_item_require == None:
        return "post == None !"
 
    openai_api,openai_completion_davinci_config,openai_completion_turbo_config,require_config = get_config_dict(config)

    # 初始化  
    turbo = openai_utils.gpt_requst_turbo(
        openai_api,
        openai_completion_turbo_config,
        law_item_require
        )

    # 通过 law_item 获取参数
    require,require_type,prompts = turbo.get_require_by_law_item(require_config)


    # 启动 openai
    res = turbo.processing_demands(require,require_type,prompts)
    return res

# 捕获参数校验异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "message": "请求参数错误",
            "details": exc.errors(),
        },
    )

# 启动成功提示
@app.get('/state')
def app_start_state():

    return "服务已启动  当前时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
if __name__ == '__main__':
    # 配置 uvicorn 服务器
    uvicorn_config = Config(app=app,
                host="127.0.0.1",
                port=8080,
                workers=1)
    # 创建服务器实例
    server = Server(uvicorn_config)
    # 运行服务器
    server.run()
