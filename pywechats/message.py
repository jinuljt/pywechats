#-*- coding:utf-8 -*-
#created:      Thu Jun  6 17:07:07 2013
#filename:     message.py
#author:       juntao liu
#email:        jinuljt@gmail.com

import time
from xml.dom import minidom
from collections import OrderedDict

class WCMessage(dict):
    def __init__(self, xml=""):
        if xml: self.from_xml(xml)
    
    def from_xml(self, xml):
        '''
        only allow depth 1
        '''
        try:
            dom = minidom.parseString(xml)
            top = dom.childNodes[0]
            for node in top.childNodes:
                if node.childNodes:
                    child = node.childNodes[0]
                    if  (child.nodeType == child.TEXT_NODE or
                         child.nodeType == node.CDATA_SECTION_NODE):
                        self[node.tagName] = node.childNodes[0].data
        except Exception, e:
            pass
    
    def to_xml(self):
        def make_nodes(node, d):
            for k, v in d.iteritems():
                child = doc.createElement(k)                    
                if type(v) == list:
                    for cd in v:
                        make_nodes(child, cd)
                if type(v) == str or type(v) == unicode:
                    qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
                    child.appendChild(doc.createCDATASection(qv))
                elif type(v) == int:
                    child.appendChild(doc.createTextNode(str(v)))
                elif type(v) == dict:
                    make_nodes(child, v)
                node.appendChild(child)
                    
        impl = minidom.getDOMImplementation()
        doc = impl.createDocument(None, "xml", None)

        top_element = doc.documentElement
        make_nodes(top_element, self)
        return top_element.toxml()

    def __setattr__(self, attr, value):
        self[attr] = value

    def __getattr__(self, attr):
        return self[attr]

class WCTextMessage(WCMessage):
    
    def __init__(self, msg, star=False):
        self.ToUserName = msg.FromUserName
        self.FromUserName = msg.ToUserName
        self.MsgType = "text"
        self.CreateTime = int(time.time())
        self.FuncFlag = 1 if star else 0

    def add_content(self, content):
        self.Content = content


class WCNewsMessage(WCMessage):

    def __init__(self, msg, star=False):
        self.ToUserName = msg.FromUserName
        self.FromUserName = msg.ToUserName
        self.MsgType = "news"
        self.CreateTime = int(time.time())
        self.FuncFlag = 1 if star else 0
        self.ArticleCount = 0
        self.Articles = []

    def add_article(self, title, description, pic_url, url):
        item = {"item":{"Title": title,
                        "Description": description,
                        "PicUrl": pic_url,
                        "Url": url}}
        self.Articles.append(item)
        self.ArticleCount += 1

class WCMusicMessage(WCMessage):
    
    def __init__(self, msg, star=False):
        self.ToUserName = msg.FromUserName
        self.FromUserName = msg.ToUserName
        self.MsgType = "music"
        self.CreateTime = int(time.time())
        self.FuncFlag = 1 if star else 0
        self.Music = {}

    def add_article(self, title, description, url, hq_url):
        self.Music = {"Title": title,
                      "Description": description,
                      "MusicUrl": url,
                      "HQMusicUrl": hq_url}
