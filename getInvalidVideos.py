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
    responsed_jobject = json.loads(resp)
    archive = responsed_jobject['data']['archive']

    for i in range(0, len(archive)):
        fav_folder_obj = archive[i]
        fav_folder_id = fav_folder_obj['fid']
        fav_folder_name = fav_folder_obj['name']
        fav_list.append(fav_folder_id)
        fav_name_list.append(fav_folder_name)

    print_f('mid={user} has fav folders: {folder}'.format(user=uid, folder=fav_name_list))


#given a fav folder id, find pages and parse videos info
def process_fav_folder(uid, fav_list_index):
    global fav_list

    fav_folder_content = ''
    url = 'https://api.bilibili.com/x/space/fav/arc?vmid={userid}&ps=30&fid={favid}&tid=0&keyword=&pn=1&order=fav_time&jsonp=jsonp'.format(userid=uid, favid=fav_list[fav_list_index])
    resp = get_HTML_text(url, agent)
    responsed_jobject = json.loads(resp)
    page_count = responsed_jobject['data']['pagecount']
    print_f('{favid} has {page} pages.'.format(id=uid,favid=fav_name_list[fav_list_index],page=page_count))

    video_jobject = responsed_jobject['data']['archives']
    fav_folder_content += handle_jobject_per_page(video_jobject, fav_list_index, 1)

    for i in range(2, page_count + 1):
        url = 'https://api.bilibili.com/x/space/fav/arc?vmid={userid}&ps=30&fid={favid}&tid=0&keyword=&pn={page_index}&order=fav_time&jsonp=jsonp'.format(userid=uid, favid=fav_list[fav_list_index], page_index=i)
        resp = get_HTML_text(url, agent)
        responsed_jobject = json.loads(resp)
        video_jobject = responsed_jobject['data']['archives']
        fav_folder_content += handle_jobject_per_page(video_jobject, fav_list_index, i)

    return fav_folder_content


def handle_jobject_per_page(page_jobjects, fav_list_index, page_index):
    global output_index
    global fav_name_list

    page_info = ''
    valid_count = 0
    invalid_count = 0
    for i in range(0, len(page_jobjects)):
        jObject = page_jobjects[i]
        if int(jObject['state']) >= 0:
            valid_count += 1
            continue
        invalid_count += 1
        s = '#{number}{title}\n'.format(number=output_index, title=jObject['title'])
        s += 'AV{vid} 收藏夹:{favFolder},Page:{page},Index:{num}\n'.format(vid=jObject['aid'], favFolder=fav_name_list[fav_list_index], page=page_index, num=i)
        s += 'UP主:{up}<space.bilibili.com/{mid}>\n'.format(up=jObject['owner']['name'], mid=jObject['owner']['mid'])
        s += '注释:\n{desc}\n\n\n'.format(desc=jObject['desc'])
        page_info += s
        output_index += 1
    print_f('    {}:Page {} has {} valid videos and {} invalid videos, index reach to \'{}\'. '.format(fav_name_list[fav_list_index], page_index, valid_count, invalid_count, output_index))
    return page_info


def get_HTML_text(url, agent):
    try:
        headers = {'User-Agent': agent}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'Error: Unable to query Bilibili server!'


def print_f(info):
    if sys.getdefaultencoding() == 'ascii':
        info.encode('gb2312')
        print(info)
    else:
        info.encode('utf-8')
        print(info)
