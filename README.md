# 简介
chatgpt_law_ai是一个通过调用openai的api来进行法律相关文本处理的https接口，由一个fastapi初学者制作

# 安装
1. 下载
2. 在解压目录运行 `pip install -r requirements.txt` 安装依赖包
3. 运行main

# 使用说明
运行main后
根据设置的端口号访问接口
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

**get请求（不推荐）：**
```
http://127.0.0.1:8080/get/r/任务类型/你需要处理的法律文本
```
例如：

如果执行提取要素任务
```
http://127.0.0.1:8080/get/r/extract/你需要处理的法律文本
```

更多的可以查看配置文件 config.ini

**post请求：**
```
http://127.0.0.1:8080/post/r/
```

提供的json请求：
```json
{"require_name": "extract","law_text": "你需要处理的法律文本"}
```
