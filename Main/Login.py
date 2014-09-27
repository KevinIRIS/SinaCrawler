# -*- coding: utf-8 -*-  
'''
Created on 2014年4月14日

@author: 凯
'''
import sys
import base64
import urllib.request
import urllib.parse
import json
import re
import rsa
import binascii
import http.cookiejar
from urllib.error import URLError,HTTPError
from json.decoder import JSONObject


class Login:
    def __init__(self,userName,passWord):
            self.postData = {
               "encoding":"UTF-8",
               "entry":"weibo",
               "from": "",
               "gateway":"1",
               "nonce":"",  # 这里要获取   ok
#               "pagerefer":"http://www.baidu.com/link?url=bmanhDiv8vL8rTP8WSO5xVBhKCCcqpHNbjyeq45wBWa&wd=weibo&tn=baidu&ie=utf-8&inputT=1482",
               "prelt":"199",
               "pwencode":"rsa2",
               "returntype":"META",
               "rsakv":"",  # 需要获取        ok
               "savestate":"0",
               "servertime":"",  # 需要获取  ok
               "service":"miniblg",
               "sp":"",   #encrypted password   加密的密码
               "su":"",   #encode username  加密的用户名
               "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
               "useticket":"1",
               "vsnf":"1"
               }
            self.userName = userName
            self.passWord = passWord
            
    def baseEncode(self,username):
        self.encodedName = base64.b64encode(username,altchars = None)  #username must be bytes
        return self.encodedName
    def getRespond(self):
        requestUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTU4MzMxMjc2MjE%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)&_=1397635485617"
#        respond = urllib.request.urlopen(requestUrl, data = None, timeout = 100)
        respond = urllib.request.urlopen(requestUrl, data=None,
                                 timeout= 30)  
        self.respondData =respond.read()
        return self.respondData
    def getJsonOfresponse(self,data):
        rule = r"\((.*)\)"
        p = re.compile(rule, flags = 0)
        jsonData = re.findall(p, str(data), flags = 0)[0]
        return jsonData   #json
    def getservertime(self,jsonData):   # data is bytes
        try:
            #print(jsonData)
            jsonobj = json.loads(jsonData)   # no error
            self.servertime = jsonobj["servertime"]
        except:
            print("getservertime error")
        return self.servertime
    def getnonce(self,jsonData):
        try:
            jsonObj = json.loads(jsonData)
            self.nonce = jsonObj["nonce"]
        except:
            print("getnonce error")
        return self.nonce
    def getrsakv(self,jsonData):
        try:
            jsonobj = json.loads(jsonData)
            self.rsakv = jsonobj["rsakv"]
        except:
            print("get rsakv error")
        return self.rsakv
    def getpubkey(self,jsonData):
        try:
            jsonObj = json.loads(jsonData)
            self.pubkey = jsonObj["pubkey"]
        except:
            print("get pubkey error")
            return
        return self.pubkey  
    def crtytionPsw(self,servertime ,nonce ,psw,rsapubkey):
        info = str(servertime) + "\t" + str(nonce) + "\n"+ str(psw)   #data to encrypt
        rsapubkey = int(rsapubkey,16)   #转乘10进制
#        print(rsapubkey)
        pubkey = rsa.PublicKey(rsapubkey,65537)   #js enceyption
#        print(pubkey)    # public key
        encrypsw = rsa.encrypt(str.encode(info),pubkey)    #encrypt 
        password = binascii.b2a_hex(encrypsw)
        password = str(password)
#        print(password)
        return password
    def getmainurl(self):
        url = 'http://www.weibo.com/?wvr=5&lf=reg'
        return url
    def getcookie(self): 
        return self.cookiejar
    def savecookie(self):
        return 
    @property
    def login(self):
        name = self.userName.encode(encoding='utf_8', errors='strict')
        encodedName = self.baseEncode(name)  #must be bytes
#        print(encodedName)
        self.getRespond()
        jsonData = self.getJsonOfresponse(self.respondData)
        self.getservertime(jsonData)
        self.getnonce(jsonData)
        self.getpubkey(jsonData)
        self.getrsakv(jsonData)
        encryptedPsw = self.crtytionPsw(self.servertime, self.nonce, self.passWord, self.pubkey)
        self.postData['nonce']  = self.nonce
        self.postData['rsakv'] = self.rsakv
        self.postData['servertime'] = self.servertime
        self.postData['su'] = encodedName
        self.postData['sp'] = encryptedPsw
#        post ok
#        print(self.postData)
#        print(encryptedPsw)
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
#        data = urllib.parse.urlencode(self.postData, doseq = False, safe = '', encoding = None, errors = None)
        self.cookiejar = http.cookiejar.CookieJar()   # create cookie instance policy=None   cookie in memory
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar) ,
                                            urllib.request.HTTPHandler)  #bind cookiejar with a httpcookieProcessor and then
        urllib.request.install_opener(opener)  # auto deal with cookie
        #print ("cookie inite" ,self.cookiejar)
        data = urllib.parse.urlencode(self.postData, doseq = False)
        data = data.encode('utf-8')
        full_url = urllib.request.Request(url, data=data, headers=headers, origin_req_host=None, unverifiable=False)  #create post obj
        try:
            respond1 = urllib.request.urlopen(full_url)
        except HTTPError as e:
            print(e.code)
        result = respond1.getcode()
        if result >= 200 and result < 300:  #deal with state code
            result = respond1.read().decode('GBK')
            result = str(result)  # string is encoded in unicode when using python
            # print(result)
            pattern = 'location\.replace\(\"(.*?)\"\)'
            role = re.compile(pattern, flags=0)
            result = role.findall(str(result))[0]
            if "retcode=0" in result:
                print("login sucessfully")
                #print(sRedirectData(result.decode("gbk")))
                array = result.split("?")
                print(urllib.unquote(array[1][4:]).decode('utf-8', 'replace').encode('gbk', 'replace'))
                manUrl = urllib.unquote(array[1][4:]).decode('utf-8', 'replace').encode('gbk', 'replace')
                respond2 = urllib.request.urlopen(manUrl)
                print(respond2.read())
                #print(urllib2.urlopen("http://weibo.com/u/1949648361/home?wvr=5").read())
            else:
                print("longin error")
        else:
            print("return error!")