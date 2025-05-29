import  asyncio
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Prompt, Tool
from mysql_mcp_server_pro.handles.base import ToolRegistry
from starlette.applications import Starlette
from starlette.routing import Route, Mount

from .prompts.base_Prompt import *


# 初始化MCP的服务器
app=Server("myMCP_server")

# 使用对应的装饰器来开放我们刚刚的端口


#开放所有提示词的接口
@app.list_prompts()
async  def handle_list_prompts() -> list[Prompt]:
    return PromptRegistry.get_all_prompts()

# 获取单个提示词接口
@app.get_prompt()
async  def handle_get_prompt(name: str, arguments: Dict[str, Any] | None) -> GetPromptResult:
    prompt=PromptRegistry.get_prompt(name)
    return  await prompt.run_prompt(arguments)

# 获取工具列表的接口
@app.list_tools()
async def list_tools()-> list[Tool]:

    return ToolRegistry.get_all_tools()


#调用指定工具的接口
@app.call_tool()
async  def call_tool(name:str ,arguments:Dict[str,Any])-> Sequence[TextContent]:
    tool=ToolRegistry.get_tool(name)
    return await tool.run_tool(arguments)

# 用于运行stdio的服务器
async  def run_stdio():
    from  mcp.server.stdio import  stdio_server

    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            print(f"服务器错误: {str(e)}")
            raise


def run_sse():
    """运行SSE(Server-Sent Events)模式的服务器

    启动一个支持SSE的Web服务器，允许客户端通过HTTP长连接接收服务器推送的消息
    服务器默认监听0.0.0.0:9000
    """
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        """处理SSE连接请求

        Args:
            request: HTTP请求对象
        """
        async with sse.connect_sse(
                request.scope, request.receive, request._send
        ) as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message)
        ],
    )
    uvicorn.run(starlette_app, host="0.0.0.0", port=9000)


def main(mode="sse"):
    """
    主入口函数，用于命令行启动
    支持两种模式：
    1. SSE 模式（默认）：mysql-mcp-server
    2. stdio 模式：mysql-mcp-server --stdio

    Args:
        mode (str): 运行模式，可选值为 "sse" 或 "stdio"
    """
    import sys

    # 命令行参数优先级高于默认参数
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # 标准输入输出模式
        asyncio.run(run_stdio())
    elif len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式
        run_sse()
    else:
        # 使用传入的默认模式
        if mode == "stdio":
            asyncio.run(run_stdio())
        else:
            run_sse()



if __name__ == "__main__":
    main()