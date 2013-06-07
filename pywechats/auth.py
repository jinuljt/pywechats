#-*- coding:utf-8 -*-
#created:      Thu Jun  6 15:59:47 2013
#filename:     auth.py
#author:       juntao liu
#email:        jinuljt@gmail.com

import time
from hashlib import sha1

class WeChatAuth(object):
    def __init__(self, token, min_seconds, max_seconds):
        '''
        bucket will delete nonce which overtime then min_seconds
        '''
        self.min_seconds=min_seconds
        self.max_seconds=max_seconds
        self.token = token
        self.bucket = {}
        self.clean_time = int(time.time())

    def authorized(self, signature, timestamp, nonce):
        if not self.fill_bucket(timestamp, nonce): return False
        if (sha1("".join(sorted([self.token,
                                 str(timestamp),
                                 nonce]))).hexdigest() ==
            signature):
            return True
        return False

    def fill_bucket(self, timestamp, nonce):
        now = int(time.time())
        if not ((now - self.min_seconds) <=
                timestamp <=
                (now + self.max_seconds)):
            return False
        
        if (now - self.clean_time) >= self.min_seconds:
            self.clean_bucket(now-self.min_seconds)
        if self.bucket.has_key(nonce): return False
        self.bucket[nonce] = timestamp
        return True

    def clean_bucket(self, timestamp):
        new_bucket = {}
        for k,v in self.bucket.interitems():
            if v >= timestamp: new_bucket[k] = v
        self.bucket = new_bucket
