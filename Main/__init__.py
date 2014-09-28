# -*- coding: utf-8 -*-  
from LoginModule.Login import Login
from FetcherModule.Fetcher import Fetcher

weibo1 = Login("", "")
weibo1.login()
# cookie = weibo1.getcookie()
fetcher = Fetcher()
content = fetcher.fetch('http://www.weibo.com/?wvr=5&lf=reg')
print(content.decode())
# content = fetcher.fetch('http://www.weibo.com/?wvr=5&lf=reg')
#print(content)