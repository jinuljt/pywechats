#-*- coding:utf-8 -*-
#created:      Tue Jun  4 19:31:29 2013
#filename:     wechat.py
#author:       juntao liu
#email:        jinuljt@gmail.com

from hashlib import sha1
import urllib
import time

from .auth import WeChatAuth
from .message import WCMessage

MIN_SECONDS=30
MAX_SECONDS=30

EVENT_DEFAULT="default"
EVENT_TYPE="event"


class WeChatServer(object):
    def __init__(self, token):
        self.handlers = {}
        self.handler_default = None
        self.token = token
        self.auth = WeChatAuth(token, MIN_SECONDS, MAX_SECONDS)

    def authorized(self, signature, timestamp, nonce):
        return self.auth.authorized(signature, timestamp, nonce)

    def register_default(self, handler):
        self.handler_default = handler

    def register_message(self, name, handler):
        self.handlers[name] = handler

    def register_event(self, event, handler, key=EVENT_DEFAULT):
        if not self.handlers.has_key(EVENT_TYPE): self.handlers[EVENT_TYPE] = {}
        if not self.handlers[EVENT_TYPE].has_key(event):
            self.handlers[EVENT_TYPE][event] = {}
        self.handlers[EVENT_TYPE][event][key] = handler

    def feed(self, data):
        msg = WCMessage(data)
        handler = self.handlers.get(msg.get('MsgType', ""))
        if handler:
            if msg.get('MsgType', "") == "event":
                handler = handler.get(msg.get('Event'))
                if handler:
                    handler = handler.get(msg.get('EventKey') or EVENT_DEFAULT)
        handler = handler or self.handler_default
        if not handler: return None
        return handler(msg)
         
