import openai
import os

class gpt_requst_turbo:
    def __init__(self, openai_api,openai_completion_config,require_name,law_text):
        super().__init__()
        # key
        self.openai_key = openai_api["api_key"]
        self.openai_api_base = openai_api["api_base"]

        # argument
        self.model_config = openai_completion_config["model_turbo"]
        self.initial_prompt_config = openai_completion_config['initial_prompt']
        self.temperature_config = float(openai_completion_config['temperature'])
        self.max_tokens_config = int(openai_completion_config['max_tokens'])
        self.n_config = int(openai_completion_config["n"])
        self.stop_config = openai_completion_config["stop"]

        self.top_p_config = float(openai_completion_config['top_p'])
        self.frequency_penalty_config = float(openai_completion_config['frequency_penalty'])
        self.presence_penalty_config = float(openai_completion_config['presence_penalty'])


        # require
        self.require_name = require_name
        self.law_text = law_text

    # 创建 openai 请求
    def use_openai(
                    self,
                    prompts:str = None
                  ):
        # if prompts == None:
        #     return -1
        if prompts is None: 
            raise ValueError("prompts should not be None")
        # 获取 key
        openai_key = self.openai_key
        # 获取参数
        model_config = self.model_config
        initial_prompt_config = self.initial_prompt_config
        message_system = {"role": "system", "content": initial_prompt_config}
        message_user = {"role": "user", "content": prompts}
        messages_list = []
        messages_list.append(message_system)
        messages_list.append(message_user)
        temperature_config = self.temperature_config
        max_tokens_config = self.max_tokens_config
        # n_config = int(self.n_config),
        # stop_config = self.stop_config,
        top_p_config = self.top_p_config
        frequency_penalty_config = self.frequency_penalty_config
        presence_penalty_config = self.presence_penalty_config
        openai_api_base_config = self.openai_api_base
        openai.api_key = openai_key
        # 借用国内代理进行跳转
        openai.api_base = os.environ.get("OPENAI_API_BASE", openai_api_base_config)
        # 调用api
        response = openai.ChatCompletion.create(
            model=model_config,
            messages = messages_list,
            temperature=temperature_config,
            max_tokens=max_tokens_config,
            # n = n_config,
            # stop = stop_config,
            top_p=top_p_config,
            frequency_penalty=frequency_penalty_config,
            presence_penalty=presence_penalty_config,
            stream = False
        )
        # response = openai_key
        return response

    # 通过 law_item 获取参数
    def get_require_by_law_item(self,require_config):
        require_name = self.require_name
        law_text = self.law_text
        # 获取任务名
        require = require_config[f"require_{require_name}"]
        # 获取任务类型
        require_type = require_config[f"require_type_{require_name}"]
        # 输入参数，获取回答 response
        prompts = require + "```" + law_text + "```"
        return require,require_type,prompts
        


    # 调用 api
    def processing_demands(
            self,
            require,
            require_type,
            prompts
            ):
        
        if require == None:
            return "require == None"
        
        response = self.use_openai(prompts)

        if response == -1:
            return "openai_config == None | require_name == None | law_text == None !"
      
        response_text = response.get("choices")[0]["message"]["content"]
        response = response_text

        # require_type = openai_config.get("require_name","require_type_"+require_name)
        res = {"材料文本":self.law_text,"任务类型":require_type,"回答":response}
        # print(res)
        return res