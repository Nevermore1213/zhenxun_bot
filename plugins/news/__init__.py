from nonebot import on_command
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import requests
from utils.manager import group_manager
from utils.utils import scheduler, get_bot
from configs.config import Config
from configs.config import NICKNAME

__zx_plugin_name__ = "每日60秒早报"
__plugin_usage__ = """
usage：
    每日60秒早报
    指令：
        早报/新闻
""".strip()
__plugin_des__ = "第一次写插件"
__plugin_cmd__ = ["早报/新闻"]
__plugin_version__ = 0.1
__plugin_author__ = "Nevermore"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["早报", "新闻"],
}
__plugin_task__ = {"zaobao": "早报"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_zaobao",
    True,
    help_="被动 早报 进群默认开关状态",
    default_value=True,
)


zaobao = on_command("早报", aliases={"早报", "新闻"}, priority=5, block=True)

url = "https://v2.alapi.cn/api/zaobao"
payload = "token=Q0jJjDgBxD1oBg7B&format=json"
headers = {'Content-Type': "application/x-www-form-urlencoded"}

async def msg(bot: Bot, type_event: str):

    response = requests.request("POST", url, data=payload, headers=headers)
    text = response.json()
    text_1 = text['data']['news']
    data = {
        "type": "node",
        "data": {
            "name": f"这里是{NICKNAME}酱",
            "uin": f"{bot.self_id}",
            "content": text['data']['date'],
        }
    }
    msg_list = [data]
    for i in text_1:
        if type_event == 'Group':
            _message = i
            data = {
                "type": "node",
                "data": {
                    "name": f"这里是{NICKNAME}酱",
                    "uin": f"{bot.self_id}",
                    "content": _message,
                },
            }
            msg_list.append(data)
    return msg_list, 200

@zaobao.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    response = requests.request("POST", url, data=payload, headers=headers)
    text = response.json()
    text_1 = text['data']['news']
    str = text['data']['date'] + '\n'
    for i in text_1:
        str += i
        str += '\n'
    result = str
    await zaobao.send(result)

# 早报定时
@scheduler.scheduled_job(
    "cron",
    hour=7,
    minute=30,
)
async def _():
    bot = get_bot()
    gl = await bot.get_group_list()
    gl = [g["group_id"] for g in gl]
    msg_list, code = await msg(bot, "Group")
    for g in gl:
        if await group_manager.check_group_task_status(g, "zaobao"):
            try:
                if msg_list and code == 200:
                    await bot.send_group_forward_msg(group_id=g, messages=msg_list)
                else:
                    await bot.send_group_msg(group_id=g)
            except Exception as e:
                logger.error(f"早报获取错误")
