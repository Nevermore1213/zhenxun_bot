from nonebot import on_command
import datetime
from . import library
from . import config
from . import send_email
import json
from configs.config import Config
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from utils.utils import scheduler, get_bot
from nonebot.typing import T_State

#TODO 将图书馆代码移植过来，增加查看预约状况功能cmd=查看预约 1.xxx 2.xxx 3.xxx，增加删除特定预约功能cmd删除{}预约，？随时查看图书馆成员功能
__zx_plugin_name__ = "图书馆预约 [Superuser]"
__plugin_usage__ = """
usage：
    图书馆预约
    指令：
        
""".strip()
__plugin_des__ = ""
__plugin_cmd__ = ["查看预约"]
# __plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "Nevermore"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查看预约"],
}
__plugin_task__ = {"booking": "图书馆预约"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_LibraryBooking",
    True,
    help_="被动 图书馆预约 进群默认开关状态",
    default_value=True,
)

yuyue = on_command("查看预约", aliases={"查看预约"}, priority=5, block=True)

@yuyue.handle()
async def handle(bot:Bot, event:MessageEvent, state:T_State):
    username = config.username
    password = config.password
    person = library.Person(username, password, room_id=4)
    person.login()
    orderinfo = person.queryHistory()[0]
    msg = f'预约成功:\n{orderinfo[0]}已生效:\n{orderinfo[1]}'
    await yuyue.send(msg)


# @zaobao.handle()
# async def handle(bot: Bot, event: MessageEvent, state: T_State):
#     response = requests.request("POST", url, data=payload, headers=headers)
#     text = response.json()
#     text_1 = text['data']['news']
#     str = text['data']['date'] + '\n'
#     for i in text_1:
#         str += i
#         str += '\n'
#     result = str
#     await zaobao.send(result)
# ------------配置区----------------#
def learn_time(*time_tuple):
    # 提前一天预约
    timestamp = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    # timestamp = (datetime.datetime.now() ).date()
    learn_am = time_tuple[0]
    duration_am = time_tuple[1]
    learn_pm = time_tuple[2]
    duration_pm = time_tuple[3]
    time_str = [[(str(timestamp) + ' ' + learn_pm), duration_pm, 'pm'],
                [(str(timestamp) + ' ' + learn_am), duration_am, 'am']]
    return time_str
    # print(timestamp)


async def save_json_file(log):
    '''
    将预约信息存为json文件，相对路径Booking\2022-09-29.json
    :param log:
    :return:
    '''
    booking_time = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    # booking_time = (datetime.datetime.now() ).date()
    txt = json.dumps(log, indent=2, ensure_ascii=False)
    with open(f'Booking/{booking_time}.json', 'w', encoding='utf-8') as f:
        f.write(txt)
    content = str(log)
    subject = f'{booking_time},预约成功'
    config.sendEMail(subject, content)


@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=2,
)
async def _():
    msg = '2'
    # username = config.username
    # password = config.password
    # room_id = config.room_id
    # perfer_seat = config.perfer_seat
    # time_str = learn_time(*config.time_tuple)
    # # -------------------------------#
    # try:
    #     username = sys.argv[1]
    #     password = sys.argv[2]
    #     # print("使用传入信息")
    # except:
    #     if username == "" and password == "":
    #         logger.warning("账号或密码为空")
    #
    # # print(f"👉账号:{username}")
    # # print(f"👉密码:{password}")
    #
    # person = library.Person(username, password, room_id)
    # person.login()
    # # log列表储存上午、下午两个时间段的预约信息 [{'am':'008'},{'pm':'009'}]
    # log = []
    # # print(time_str)
    # for i in time_str:
    #     '''
    #     i[0] 开始时间
    #     i[1] 持续时间
    #     '''
    #     try:
    #         seatInfo = person.queryRoom(person.showRoom(room_id), perfer_seat, str(i[0]), i[1])
    #         if seatInfo is None:
    #             logger.warning("找不到位置")
    #             seat_id = ' '
    #         else:
    #             print(f"查询到 {seatInfo['name']} 位置满足要求")
    #             duration = i[1]
    #             person.submit(seatInfo, str(i[0]), duration)
    #             seat_id = str(seatInfo['name'][-3:])
    #         if i[2] == 'am':
    #             get_time_duration = 'am'
    #         else:
    #             get_time_duration = 'pm'
    #
    #         dict = {get_time_duration: seat_id}
    #         log.append(dict)
    #         msg += f'{str(dict)}'
    #     except:
    #         logger.warning('pass')
    #         pass
    # await save_json_file(log)
    bot = get_bot()
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=2139511496,
        message=msg
    )

# bot = get_bot()
# gl = await bot.get_group_list()
# gl = [g["group_id"] for g in gl]
# bot.send_group_msg(group_id=,message=)
# msg = await
# for g in gl:
#     if await group_manager.check_group_task_status(g, "weather"):
#         try:
#             if msg and code == 200:
#                 await bot.send_group_forward_msg(group_id=g, messages=msg_list)
#             else:
#                 await bot.send_group_msg(group_id=g)
#         except Exception as e:
#             logger.error(f"早报获取错误")
# if __name__ == '__main__':
#     username = config.username
#     password = config.password
#     room_id = config.room_id
#     perfer_seat = config.perfer_seat
#     print(config.time_tuple[0])
#     print(config.time_tuple[1])
#     time_str = learn_time(*config.time_tuple)
#     # -------------------------------#
#     try:
#         username = sys.argv[1]
#         password = sys.argv[2]
#         print("使用传入信息")
#     except:
#         if username == "" and password == "":
#             logger.warning("账号或密码为空")
#
#     print(f"👉账号:{username}")
#     # print(f"👉密码:{password}")
#
#     person = library.Person(username, password, room_id)
#     person.login()
#     # log列表储存上午、下午两个时间段的预约信息 [{'am':'008'},{'pm':'009'}]
#     log = []
#     print(time_str)
#     for i in time_str:
#         '''
#         i[0] 开始时间
#         i[1] 持续时间
#         '''
#         try:
#             seatInfo = person.queryRoom(person.showRoom(room_id), perfer_seat, str(i[0]), i[1])
#             if seatInfo is None:
#                 logger.warning("找不到位置")
#                 seat_id = ' '
#             else:
#                 print(f"查询到 {seatInfo['name']} 位置满足要求")
#                 duration = i[1]
#                 person.submit(seatInfo, str(i[0]), duration)
#                 seat_id = str(seatInfo['name'][-3:])
#             if i[2] == 'am':
#                 get_time_duration = 'am'
#             else:
#                 get_time_duration = 'pm'
#
#             dict = {get_time_duration: seat_id}
#             log.append(dict)
#         except:
#             logger.warning('pass')
#             pass
#     save_json_file(log)
