import  os
from  dotenv import  *

Role_Permissions={
     "readonly": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"],  # 只读权限
    "writer": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE"],  # 读写权限
    "admin": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE",
             "CREATE", "ALTER", "DROP", "TRUNCATE"]  # 管理员权限
}

# 从环境变量获取数据库配置的信息
def get_db_config():
    load_dotenv()
    # 指定.env配置文件的路径
    from  pathlib import Path
    # 填写你env的路径
    default_env_path=Path("'/Users/wzf-perfomancemac/Desktop/mcp/mcp_server_development/MCP_dev_ Test01/.env'")
    # 加载env的默认路径
    load_dotenv(dotenv_path=default_env_path)
    # 加调试输出确认是否加载成功
    print("[DEBUG] MYSQL_USER:", os.getenv("mysql_host"))
    print("[DEBUG] MYSQL_PASSWORD:", os.getenv("mysql_password"))
    print("[DEBUG] MYSQL_DATABASE:", os.getenv("mysql_database"))
    config = {
        "host": os.getenv("mysql_host","localhost"),
        "port": int(os.getenv("mysql_port","3306")),
        "user_name": os.getenv("mysql_user","root"),
        "password": os.getenv("mysql_password"),
        "used_password":"yes" if os.getenv("mysql_password") is not None else "no",
        "database":os.getenv("mysql_database"),
        # 默认角色为只读
        "role":os.getenv("mysql_role","readonly")
    }
    # 检查下数据库配置
    if not all([config["user"],config["password"],config["database"]]):
        # 抛出值异常
        raise  ValueError("缺少必须的数据库配置")

# 定义角色权限的对象
# 规定每个角色所能自行的sql语句的范围



# 对外暴露接口，提供一个查询权限的方法
def get_role_permission(role:str)->list:
    # 默认返回只读权限
    return  Role_Permissions.get(role,Role_Permissions["readonly"])
