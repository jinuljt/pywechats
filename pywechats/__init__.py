#-*- coding:utf-8 -*-
#created:      Tue Jun  4 19:32:01 2013
#filename:     __init__.py
#author:       juntao liu
#email:        jinuljt@gmail.com


__all__ = ['__version__',
           '__author__',
           "WeChatServer",
           "WCTextMessage",
           "WCNewsMessage",
           "WCMessage"]

from .wechat import WeChatServer
from .message import WCTextMessage, WCMessage, WCNewsMessage

__version__ = "0.0.1"
__author__ = "Juntao Liu"

