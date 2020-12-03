# -*- coding: utf-8 -*-
# author: hejianxin
# date: 2020/12/3 21:21
from dingtalkchatbot.chatbot import DingtalkChatbot

from django.conf import settings


def send(message, at_mobiles=list()):
    # 引入settings里配置的丁丁群消息通知的webhook地址
    webhook = settings.DINGTALK_WEB_HOOK

    # 初始化小丁 方式一
    xiaoding = DingtalkChatbot(webhook)

    # 方式二 勾选 加签 选项时使用
    # xiaoding = DingtalkChatbot(webhook, secret=secret)

    # Text 消息@所有人
    xiaoding.send_text(msg=('面试通知: %s'%message), at_mobiles=at_mobiles)
