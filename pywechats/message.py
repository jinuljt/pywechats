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
                if type(v) == list:
                    for cd in v:
                        child = doc.createElement(k)                    
                        make_nodes(child, cd)
                        node.appendChild(child)
                    continue
                
                child = doc.createElement(k)
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

class WCPlainMessage(WCMessage):
    
    def __init__(self, msg, star=False):
        self.ToUserName = msg.FromUserName
        self.FromUserName = msg.ToUserName
        self.MsgType = "text"
        self.CreateTime = int(time.time())
        self.FuncFlag = 1 if star else 0
