#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


import re

class thread:
    def __init__(self, id, info, t_content):
        self.id = id

        self.title = info.get("title")
        self.email = info.get("email")
        self.createdat = info.get("createdat")
        self.uid = info.get("uid")

        self.t_content = t_content

    def disp_thread(self):
        str = "{} {} {} {} {}".format(self.id, self.title, self.email, self.createdat, self.uid)
        print(str)
        print("----\r")
        #nob_c = re.sub('(^\s*)','', self.t_content) 
        nob_c = self.t_content.lstrip()
        print(nob_c)

        print("---------------------------------\r\n")
        



url = "https://adnmb1.com/f/%E6%97%B6%E9%97%B4%E7%BA%BF"
html = requests.get(url).text

soup = BeautifulSoup(html,'lxml')
 
thread_list = []

for link in soup.find_all('div', class_='h-threads-item uk-clearfix'):
    #thread_list.append( thread(link.find('a', class_='h-threads-info-id').get_text()) )

    id = link.find('a', class_='h-threads-info-id').get_text()
    info = {
        "title": link.find('span', class_='h-threads-info-title').get_text(),
        "email": link.find('span', class_='h-threads-info-email').get_text(),
        "createdat": link.find('span', class_='h-threads-info-createdat').get_text(),
        "uid": link.find('span', class_='h-threads-info-uid').get_text()
    }
    t_content =  link.find('div', class_='h-threads-content').get_text()

    thread_list.append( thread(id, info, t_content) )

for t in thread_list:
    t.disp_thread()