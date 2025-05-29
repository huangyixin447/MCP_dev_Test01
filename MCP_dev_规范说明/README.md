# MCP_dev项目说明

此项目目的在为MCP的开发进行封装，用以简化，结构化MCP的开发流程

首先mcp的开发大致分为两类:

### 1.MCP的工具类开发，用于执行核心工具逻辑base_Mcp_Handles.py:

在本项目的基类中，将所有的工具放入list容器中，并且对于MCP规范所必须的
`run_tool` `get_tool_description` 方法做了接口规范，强制子类继承

工具基类如下:

在这个文件所在的python包下，直接新建你要创建的工具，例如操作mysql，操作邮件服务器发邮件 的python类，并且继承这个类，重写其中两个类属性，以及`get_tool_description` `run_tool` 方法即可自动进行注册。实现逻辑并且按照这两个方法的要求返回参数即可。

### 2.MCP的提示词开发模块

对于不同情景下问题要有不同的提示词，每一种场景的提示词的逻辑与刚刚的1的工具模块的逻辑差不多, 也存在一个基类base_Prompt.py，具体封装的方式见源码, 使用的方法同样是去继承

`BasePrompt`类,并且重写属性

![image.png](MCP_dev%E9%A1%B9%E7%9B%AE%E8%AF%B4%E6%98%8E%20201787de5786800b99e5e244bb13199f/image.png)

以及重写以下两个方法

![image.png](MCP_dev%E9%A1%B9%E7%9B%AE%E8%AF%B4%E6%98%8E%20201787de5786800b99e5e244bb13199f/image%201.png)

即可完成自动注册

### 3.此外还有一个统一配置的模块

config下的dbconfig.py

新建一个.env 文件, 并且复制路径

修改以下的路径为你自己的路径

![image.png](MCP_dev%E9%A1%B9%E7%9B%AE%E8%AF%B4%E6%98%8E%20201787de5786800b99e5e244bb13199f/image%202.png)

.env填写的示范例子如下

```python
# MySQL数据库配置
mysql_host=localhost
mysql_port=11801
mysql_user=root
mysql_password=123456
mysql_database=MCP_taobao
# 可选值: readonly, writer, admin，默认为 readonly
mysql_role=readonly
```

当然其他配置也行，都可以被dbconfig读取

具体看源码的示例

4.实际构建mcp服务的server.py

将以上各种封装好的，tool，prompt交给mcp的server，并且sse或者stdio的server不一样，要采用不同的方式实现。具体见源码。