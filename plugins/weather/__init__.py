from nonebot import on_regex
from .data_source import get_weather_of_city, get_city_list
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from jieba import posseg
from services.log import logger
from nonebot.params import RegexGroup
from typing import Tuple, Any
from configs.config import Config
from utils.utils import scheduler, get_bot
from utils.manager import group_manager
from .data_source import *

__zx_plugin_name__ = "天气查询"
__plugin_usage__ = """
usage：
    普普通通的查天气吧
    指令：
        [城市]天气
""".strip()
__plugin_des__ = "出门要看看天气，不要忘了带伞"
__plugin_cmd__ = ["[城市]天气/天气[城市]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查询天气", "天气", "天气查询", "查天气"],
}
__plugin_task__ = {"weather": "近期天气预报"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_WeatherPrediction",
    True,
    help_="被动 天气预报 进群默认开关状态",
    default_value=True,
)


weather = on_regex(r".{0,10}?(.*)的?天气.{0,10}", priority=5, block=True)


@weather.handle()
async def _(event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    msg = reg_group[0]
    city = ""
    if msg:
        city_list = get_city_list()
        for word in posseg.lcut(msg):
            if word.flag == "ns" or word.word[:-1] in city_list:
                city = str(word.word).strip()
                break
            if word.word == "火星":
                await weather.finish(
                    "没想到你个小呆子还真的想看火星天气！\n火星大气中含有95％的二氧化碳,气压低，加之极度的干燥，"
                    "就阻止了水的形成积聚。这意味着火星几乎没有云,冰层覆盖了火星的两极，它们的融化和冻结受到火星与太"
                    "阳远近距离的影响,它产生了强大的尘埃云，阻挡了太阳光，使冰层的融化慢下来。\n所以说火星天气太恶劣了，"
                    "去过一次就不想再去第二次了"
                )
    if city:
        city_weather = await get_weather_of_city(city)
        logger.info(
            f'(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else "private"} ) '
            f"查询天气:" + city
        )
        await weather.finish(city_weather)
#TODO  天气预测和实际天气情况分开一下，尝试一下合并分发消息，增加定时任务（需求不合理，群友来自各地如果发送到群里的话没有意义，还是默认发给超级用户吧）

# @scheduler.scheduled_job(
#     "cron",
#     hour=7,
#     minute=30,
# )
# async def _():
#     bot = get_bot()
#     gl = await bot.get_group_list()
#     gl = [g["group_id"] for g in gl]
#     bot.send_group_msg(group_id=,message=)
#     msg = await
#     for g in gl:
#         if await group_manager.check_group_task_status(g, "weather"):
#             try:
#                 if msg and code == 200:
#                     await bot.send_group_forward_msg(group_id=g, messages=msg_list)
#                 else:
#                     await bot.send_group_msg(group_id=g)
#             except Exception as e:
#                 logger.error(f"早报获取错误")