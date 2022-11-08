from nonebot import on_command
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import requests
from configs.config import Config

__zx_plugin_name__ = "词语字典"
__plugin_usage__ = """
usage：
    词语字典
    指令：
        查询词语/解释词语
""".strip()
__plugin_des__ = ""
__plugin_cmd__ = ["查询词语/解释词语"]
__plugin_version__ = 0.1
__plugin_author__ = "Nevermore"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查询词语", "解释词语"],
}
# __plugin_task__ = {"zaobao": "早报"}
# Config.add_plugin_config(
#     "_task",
#     "DEFAULT_zaobao",
#     True,
#     help_="被动 早报 进群默认开关状态",
#     default_value=True,
# )


zaobao = on_command("查询词语", aliases={"查询词语", "解释词语"}, priority=5, block=True)