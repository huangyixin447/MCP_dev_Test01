from typing import ClassVar, Dict, Type, Any, Sequence
from mcp.types import Prompt, TextContent, GetPromptResult


# 提示词的基类
class BasePrompt:
    name:str =""
    description:str =""
    def __init_subclass__(cls, **kwargs):
        """子类继承的时候自动注册"""
        super().__init_subclass__(**kwargs)

#             进行注册


    def get_prompt(self)->Prompt:
        #抛出一个为实现的异常
        raise  NotImplementedError()

    async  def run_prompt(self,arguments:Dict[str,Any]) -> GetPromptResult:

        raise NotImplementedError()




class PromptRegistry:
    # 静态变量_prompts的作用
    _prompts:ClassVar[Dict[str,BasePrompt]] = {}

    @classmethod
    def register(cls, prompt_class:Type[BasePrompt])->Type['BasePrompt']:
        prompt=prompt_class()
        if prompt  not in cls._prompts:
            cls._prompts[prompt.name]=prompt
        else:
            print("提示词已经注册")

        return  prompt_class

    @classmethod
    def get_prompt(cls,name:str)->BasePrompt:
        if name not in cls._prompts:
            raise  ValueError (f"未知的prompt:{name}")
        return cls._prompts[name]

    @classmethod
    def get_all_prompts(cls)->list[Prompt]:
        return [p.get_prompt() for p in cls._prompts.values()]







