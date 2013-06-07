#-*- coding:utf-8 -*-
#created:      Thu Jun  6 18:27:11 2013
#filename:     test.py
#author:       juntao liu
#email:        jinuljt@gmail.com


from pywechats import WeChatServer, WCMessage, WCPlainMessage

token="token"

wcserver = WeChatServer(TOKEN)

def receive_default(message):
   msg = WCPlainMessage(message)
   msg.Content = "reply"
   return msg.to_xml()


wcserver.register_default(receive_default)
wcserver.register_message("text", receive_default)
wcserver.register_event("subscribe", receive_default)

xml = '<xml><ToUserName><![CDATA[toUser]]></ToUserName><FromUserName><![CDATA[fromUser]]></FromUserName><CreateTime>1370573337</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[H]]></Content><MsgId>5886567659184586792</MsgId></xml>'

wcserver.feed(xml)
