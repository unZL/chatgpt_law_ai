from fastapi import FastAPI, Depends
from uvicorn import Config, Server
import ai_config
import openai
# import socks5_utils
import logging
from pydantic import BaseModel
import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
# import sys
# 设置日志级别为 DEBUG（调试模式）
logging.basicConfig(level=logging.DEBUG)

config_file_path = "config.ini"

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



@app.on_event("startup")
async def startup_event():
    await before_server_start()

# 读取配置文件中的 api key 并注入依赖
def get_config(config: ai_config.Config = Depends(lambda:ai_config.Config(config_file_path))):
    return config

# 配置读取
def get_config_dict(all_config):
    # all_config = ai_config.Config(config_file_path)

    # 获取各个部分的配置

    # socks5_config = all_config.get_config("SOCKS5")

    openai_completion_config = all_config.get_config("openai_Completion_config")
    require_config = all_config.get_config("require_name")
    return openai_completion_config,require_config



# 创建 openai 请求
def use_openai(openai_completion_config:dict=None,
               prompts:str = None):
    
    if openai_completion_config == None:
        return -1
    if prompts == None:
        return -1
    # 获取 key
    openai_key = openai_completion_config["api_key"]
    
    initial_prompt = openai_completion_config['initial_prompt']
    temperature=float(openai_completion_config['temperature'])
    max_tokens=int(openai_completion_config['max_tokens'])
    top_p=float(openai_completion_config['top_p'])
    frequency_penalty=float(openai_completion_config['frequency_penalty'])
    presence_penalty=float(openai_completion_config['presence_penalty'])

    openai.api_key = openai_key
    # 借用国内代理进行跳转
    openai.api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai-proxy.com/v1")
    response = openai.Completion.create(
        model=openai_completion_config['model'],
        prompt=initial_prompt+prompts,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    # response = openai_key
    return response

# 调用 api
def processing_demands(
        openai_completion_config,
        require_config,
        require_name,
        law_text):
    # 获取任务名
    require = require_config[f"require_{require_name}"]
    # require = openai_config.get("require_name","require_"+require_name)
    
    if require == None:
        return "require == None"
    
    # 输入参数，获取回答 response
    prompts = require + "\n" + law_text
    response = use_openai(openai_completion_config,prompts)

    if response == -1:
        return "openai_config == None | require_name == None | law_text == None !"
    
    if type(response) != type(""):
        response_text = str(response.choices[0].text.strip())
        response = response_text

    # 获取任务类型
    require_type = require_config[f"require_type_{require_name}"]
    # require_type = openai_config.get("require_name","require_type_"+require_name)
    res = {"材料文本":law_text,"任务类型":require_type,"回答":response}
    # print(res)
    return res


# 使用 get 请求
# 
@app.get('/get/r/{require_name}/{law_text}')
def text_extract(
    config:ai_config.Config = Depends(get_config),
    law_text: str = None,
    require_name: str = None
    ):
    openai_completion_config,require_config = get_config_dict(config)    
    # 启动 openai
    res = processing_demands(openai_completion_config,require_config,require_name,law_text)
    return res


# 使用 post 请求

# 声明了一个 JSON 对象
class Law_item_require(BaseModel):
    require_name: str
    law_text: str


# 
@app.post('/post/r/')
def text_extract(
    config:ai_config.Config = Depends(get_config),
    law_item_require: Law_item_require = None
    ):
    if law_item_require == None:
        return "post == None !"

    require_name = law_item_require.require_name
    law_text = law_item_require.law_text

    openai_completion_config,require_config = get_config_dict(config)    
    # 启动 openai
    res = processing_demands(openai_completion_config,require_config,require_name,law_text)
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
