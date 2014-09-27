# -*- coding: utf-8 -*-  
import base64
from Main.Login import Login
from Fetcher.Fetcher import Fetcher

username = ''.encode(encoding='utf_8', errors='strict')
weibo1 = Login("15833127621", "zk19920927")
weibo1.login
cookie = weibo1.getcookie()
fetcher = Fetcher(cookie)
content = fetcher.fetch('http://www.weibo.com/?wvr=5&lf=reg')
print(content)