# -*- coding: utf-8 -*-
'''
Created on 2014年4月14日

@author: 凯
'''
import sys
import json
import urllib
import re
from bs4 import BeautifulSoup  # html parse package

# use for save information
class Parse:
    def __init__(self,content):
        self.soup = BeautifulSoup(content)
    def setTreeStruct(self):
        self.tree = self.soup.prettify()
        #link = self.soup.link['href']
        #attributes = self.soup.link.attrs
        #tagString = self.soup.link.string
        #print(self.tree)
        #print(link)
        #head = self.soup.head
        #print(head)
        #title = self.soup.title
        #print(title.string)
        alltag = self.soup.descendants
        for string in  alltag:
            print(string)
        #html = self.soup.html
        #print(html)
        self.soup.find_all(name=None, attrs={}, recursive=True, text=None,
                          limit=None)
        return None