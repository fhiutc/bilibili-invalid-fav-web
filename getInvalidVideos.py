# -*- coding:utf-8 -*-
import sys
import requests
import re
import json


agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

fav_list = []
fav_name_list = []
output_index = 1


def get_fav_folder_list(uid):
    global fav_list

    url = 'https://api.bilibili.com/x/space/fav/nav?mid={userid}&jsonp=jsonp'.format(userid=uid)
    resp = get_HTML_text(url, agent)
    responed_jobject = json.loads(resp)
    archive = responed_jobject['data']['archive']

    for i in range(0, len(archive)):
        fav_folder_obj = archive[i]
        fav_folder_id = fav_folder_obj['fid']
        fav_folder_name = fav_folder_obj['name']
        fav_list.append(fav_folder_id)
        fav_name_list.append(fav_folder_name)

    print_f('mid={user} has fav folders: {folder}'.format(user=uid, folder=fav_name_list))



def get_HTML_text(url, agent):
    try:
        headers = {'User-Agent': agent}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ('Error: Unable to query Bilibili server!')


def print_f(info):
    if sys.getdefaultencoding() == 'ascii':
        info.encode('gb2312')
        print(info)
    else:
        info.encode('utf-8')
        print(info)