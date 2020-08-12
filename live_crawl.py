from bs4 import BeautifulSoup as bs
from mongoengine import *
import requests
import sys
from dbs import Live
import json
import pprint

# connect('live')
count = 1
base_url = "https://www.douyu.com/gapi/rkc/directory/mixList/0_0/"

while count < 200:
    connect('live')
    request_url = base_url + str(count)
    response2 = requests.get(request_url)
    # load json
    json_data = json.loads(response2.text)
    for host_info in json_data["data"]["rl"]:
        # 解析json里面的房间名，房间类型，主播名称，房间人数
        home_name = host_info["rn"].replace(" ", "").replace(",", "")
        home_type = host_info["c2name"]
        host_name = host_info["nn"]
        home_user_num = host_info["ol"]
        home_dict = {}
        home_dict['home_name']= home_name
        home_dict['type'] = home_type
        home_dict['host_name'] = host_name
        home_dict['number'] = str(home_user_num)
        # print(home_dict)
        print("\033[31m房间名：\033[0m%s，\033[31m房间类型：\033[0m%s，\033[31m主播名称：\033[0m%s，\033[31m房间人数：\033[0m%s"\
              % (home_name, home_type, host_name, home_user_num))
        Live(home_name=home_dict['home_name'],
             type=home_dict['type'],
             host_name=home_dict['host_name'],
             number=home_dict['number']).save()
    count += 1

