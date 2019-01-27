#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


import re

class thread:
    def __init__(self, id, info, t_content, t_tips, rpy_list):
        self.id = id

        self.title = info.get("title")
        self.email = info.get("email")
        self.createdat = info.get("createdat")
        self.uid = info.get("uid")

        self.t_content = t_content
        self.t_tips = t_tips
        self.rpy_list = rpy_list
    
    def disp_info(self):
        return "{} {} {} {} {}".format(self.id, self.title, self.email, self.createdat, self.uid)

    def disp_content(self):
        return "{}".format(self.t_content.lstrip())

    def disp_reply(self):
        r_str = ""
        if len(self.rpy_list): 
            for r in self.rpy_list:
                rpy_info = "{} {} {} {} {}\n".format(r.get("id"), r.get("title"), r.get("email"), r.get("createdat"), r.get("uid"))
                
                rpy_c = "{}\n".format(r.get("content").strip())
                r_str = r_str + rpy_info + rpy_c
        else:
            pass
        return r_str

    def disp_thread(self):
        print("---------------------------------\n")
        title_str = "\033[4;36m{} {} {} {} {}\033[0m \n".format(self.id, self.title, self.email, self.createdat, self.uid)
        print(title_str)
        #nob_c = re.sub('(^\s*)','', self.t_content) 
        nob_c = "\033[1;37m{}\033[0m \n".format(self.t_content.lstrip())
        print(nob_c)
        tp_str = "\033[4;34m{}\033[0m \n".format(self.t_tips)
        print(tp_str)

        if len(self.rpy_list): 
            for r in self.rpy_list:
                rpy_str = "\033[4;36m{} {} {} {} {}\033[0m \n".format(r.get("id"), r.get("title"), r.get("email"), r.get("createdat"), r.get("uid"))
                print(rpy_str)
                #nob_c = re.sub('(^\s*)','', self.t_content) 
                rpy_c = "\033[0;37m{}\033[0m \n".format(r.get("content").strip())
                print(rpy_c)
        else:
            pass
        print("---------------------------------\n")
        

def get_thread(t_menu):
    url = "https://adnmb1.com{}".format(t_menu)
    html = requests.get(url).text

    thd_soup = BeautifulSoup(html,'lxml')
    
    thread_list = []

    for thd in thd_soup.find_all('div', class_='h-threads-item uk-clearfix'):
        id = thd.find('a', class_='h-threads-info-id').get_text()
        info = {
            "title": thd.find('span', class_='h-threads-info-title').get_text(),
            "email": thd.find('span', class_='h-threads-info-email').get_text(),
            "createdat": thd.find('span', class_='h-threads-info-createdat').get_text(),
            "uid": thd.find('span', class_='h-threads-info-uid').get_text()
        }
        t_content =  thd.find('div', class_='h-threads-content').get_text()

        thread_tips = thd.find('span', class_='warn_txt2')
        if thread_tips != None:
            t_tips = thread_tips.get_text()
        else:
            t_tips = ""

        rpy_list = []

        thd_rpy = thd.find('div', class_='h-threads-item-replys')
        if thd_rpy != None:
            for rpy in thd.find_all('div', class_='h-threads-item-reply'):
                rpy_id = rpy.find('a', class_='h-threads-info-id').get_text()
                rpy_content = {
                    "id": rpy_id,
                    "title": rpy.find('span', class_='h-threads-info-title').get_text(),
                    "email": rpy.find('span', class_='h-threads-info-email').get_text(),
                    "createdat": rpy.find('span', class_='h-threads-info-createdat').get_text(),
                    "uid": rpy.find('span', class_='h-threads-info-uid').get_text(),
                    "content": rpy.find('div', class_='h-threads-content').get_text()
                }
                rpy_list.append(rpy_content)
        else:
            t_tips = ""

        thread_list.append( thread(id, info, t_content, t_tips, rpy_list) )
    '''
    for t in thread_list:
        t.disp_thread()
    '''
    return thread_list


def get_menu():
    home_url = "https://adnmb1.com/Forum"
    home_html = requests.get(home_url).text
    menu_soup = BeautifulSoup(home_html,'lxml')

    menu_list = []

    for t_href in menu_soup.find_all('ul', class_='uk-nav-sub'):
        for t_menu in t_href.find_all('a'):
            menu_info = {
                "title": t_menu.get_text().strip(),
                "href": t_menu.get('href')
            }
            menu_list.append(menu_info)

    return menu_list

