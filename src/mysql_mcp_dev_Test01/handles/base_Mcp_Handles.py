# 为所有的工具类
from typing import ClassVar, Dict, Type, Any

from jedi.inference.value.iterable import Sequence
from mcp import  Tool
from mcp.types import TextContent
"""
	•	所有工具类都会从一个统一的 BaseHandler（或你自定义的类似基类）继承；
	•	MCP 会通过调用 .run_tool() 来触发工具的执行逻辑；
	•	MCP 要求这个方法是 异步的（async），这样能支持异步模型调用、数据库访问、网络请求等操作；
	•	传入的是一个 Dict[str, Any]，代表用户的 JSON 格式请求参数；
	•	返回的是 Sequence[TextContent]，表示工具处理结果，供模型/系统输出使用
"""

class BaseHandler(object):
    """工具基类"""
#     工具的名称
    name: str =""
#    工具的描述(提示词)
    tool_Prompt: str =""
#     创建内置方法，用与在类加载时自动进行注册
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.name:
            tool_Registry.register(cls)
    # 获取工具的方法
    """返回MCP的tool类型"""
    def get_tool_description(self)->Tool:
        # 此方法一定要子类实现
        # 否则报错
        raise NotImplementedError

#     工具的核心自行逻辑方法
    """同样此方法也必须被工具子类继承"""
    async  def run_tool(self,arguments:Dict[str,Any]) -> Sequence[TextContent]:
        raise  NotImplementedError









# 工具注册类
class tool_Registry:
    # 初始为none，并且静态
    Tool_Map: ClassVar[Dict[str,'BaseHandler']]={}


#    注册方法
    @classmethod
    def register(cls,tool_Class : Type['BaseHandler'])->Type['BaseHandler']:
#         首先实例工具类
        tool=tool_Class()
        #
        cls.Tool_Map[tool.name]=tool
        return  tool_Class

    @classmethod
    def get_tool(cls,name:str)-> BaseHandler:
        if name not in cls.Tool_Map:
            raise ValueError(f"未知的工具{name}")
        return cls.Tool_Map[name]

    @classmethod
    def get_all_tools(cls)-> list[Tool_Map]:
        return  [tool.tool_Prompt for tool in cls.Tool_Map.values()]
