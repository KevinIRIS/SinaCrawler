__author__ = '凯'
# -*- coding: utf-8 -*-

import threading
import urllib
import urllib.request
import gzip
_DEFAULT_TIMEOUT = 30
class Fetcher:
    def __init__(self,cookie = None):
        # self.cookie = cookie
        # self.openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie),urllib.request.HTTPHandler)
        # urllib.request.install_opener(self.openner)
        pass
    def unzip(self,content):
        file = gzip.open(filename=content, mode="rb")
        try:
            return file.read()
        finally:
            file.close()
    def fetch(self,url):
        print ('fetching url:' , url)
        content = urllib.request.urlopen(url,data=None,timeout=_DEFAULT_TIMEOUT)
        return content.read()

