# 简介
chatgpt_law_ai是一个通过调用openai的api来进行法律相关文本处理的https接口，由一个fastapi初学者制作

# 安装
1. 下载
2. 在解压目录运行 pip install -r requirements.txt 安装依赖包
3. 运行main

# 使用说明
运行main后
根据设置的端口号访问接口
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```
查看接口是否成功启动
```
http://127.0.0.1:8080/state
```
输出：启动成功 + 当前时间即为启动成功


**get请求（不推荐）：**
传入参数：
require_name：任务类型，例如：extract
law_text：需要处理的法律文本。
返回值：
res：一个形如 {"材料文本":law_text,"任务类型":require_type,"回答":response} 的字典
```
http://127.0.0.1:8080/get/r/任务类型/需要处理的法律文本
```
例如：

如果执行提取要素任务
```
http://127.0.0.1:8080/get/r/extract/需要处理的法律文本
```

现在支持的任务类型有：
extract=提取要素，
strategy=调解策略，
contention=争议焦点

更多的可以通过配置文件进行添加

**post请求：**
```
http://127.0.0.1:8080/post/r/
```

提供的json请求：

```json
{"require_name": "extract","law_text": "你需要处理的法律文本"}
```
其中，require_name 字段和 get 请求中的 参数require_name 一样，用来确定任务类型，law_text 字段则是 法律文本


# 注意事项

如果不需要 socks5 代理，请注释main.py中的

`socks5_config = socks5_utils.Socks5_config(config_file_path)`

# 代理

放弃socks5代理，选择使用其他代理

具体地址：

https://www.openai-proxy.com/