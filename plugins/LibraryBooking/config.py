# import send_email
from . import send_email
from .send_email import *

def sendEMail(subject,content):
    '''

    :param content: 邮件内容
    :return:
    '''
    try:
        # 发件人-填写自己的邮箱
        userName_SendMail = '3086151468@qq.com'
        # 邮箱发件授权码-为发件人生成的授权码
        userName_AuthCode = 'pmjktlouptvgdege'
        # 定义邮件的接收者
        received_mail = ['2139511496@qq.com']
        # 发送邮件
        smtp = send_email.SendMsg(userName_SendMail, received_mail, userName_AuthCode)
        smtp.send_msg(subject, content)
    except:
        print('邮件发送失败！')

#用户名
username = '16605407609'
#密码
password = 'Liming2002'
#预约房间
room_id = 4
#优先座位
perfer_seat = [120]
#元组 按顺序依次为上午预约时间、上午预约持续时间、下午预约时间、下午预约持续时间，可填空字符串
time_tuple = ("9:00", 350, "15:00", 350)
'''
learn_am = "9:00"
duration_am = 350
learn_pm = "15:00"
duration_pm = 350
'''

#房间信息
room = [
    {
        'id': '100455533',
        'name': '自主学习专区B203室',
        'area': '浮山'
    },
    {
        'id': '100455535',
        'name': '考研学习专区B204室',
        'area': '浮山'
    },
    {
        'id': '100455537',
        'name': '网络学习专区B205室',
        'area': '浮山'
    },
    {
        'id': '100455539',
        'name': '信息共享专区B206室',
        'area': '浮山'
    },
    {
        'id': '100455541',
        'name': '二楼A区自修区',
        'area': '浮山'
    },
    {
        'id': '100455543',
        'name': '二楼B区自修区',
        'area': '浮山'
    },
    {
        'id': '100455545',
        'name': '三楼A区自修区',
        'area': '浮山'
    },
    {
        'id': '100455547',
        'name': '三楼B区自修区',
        'area': '浮山'
    },
    {
        'id': '100455549',
        'name': '三楼大厅自修区',
        'area': '浮山'
    }
]