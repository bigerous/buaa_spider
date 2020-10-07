#!/usr/local/bin/python3

import requests
import re
import json
from mylog import myLog
import re
from mail import sendMail
import time
import datetime
import random
import urllib.parse
import yaml


todaySuccess = False

def login(s, username, password):
    url = "https://app.buaa.edu.cn/uc/wap/login/check"
    data = {"username":username,"password":password}
    try:
        response = s.get(url, data = data, timeout = 10)
        myLog.logger.info("login cookie : %s"%str(response.headers["set-cookie"]))
    except requests.RequestException:
        myLog.logger.error("无法登陆")
        return None

def getParam(s):
    url = "https://app.buaa.edu.cn/xisuncov/wap/open-report/index"
    try:
        response = s.get(url, timeout = 10)
        return response.text
    except requests.RequestException:
        myLog.logger.error("无法获取上次数据")
        return None

def upload(s, data):
    url = 'https://app.buaa.edu.cn/xisuncov/wap/open-report/save'
    try:
        response = s.post(url, data=data, timeout = 10)
        return response.text
    except requests.RequestException:
        myLog.logger.error("上次失败")
        return None

def report(username, password, email):
    global todaySuccess
    s = requests.Session()
    encodedStr = 'sfzx=1&tw=0&area=北京市 海淀区&city=北京市&province=北京市&address=北京市海淀区花园路街道北京航空航天大学北京航空航天大学学院路校区&geo_api_info={"type":"complete","position":{"Q":39.980123969185,"R":116.35079806857698,"lng":116.350798,"lat":39.980124},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":40,"isConverted":true,"status":1,"addressComponent":{"citycode":"010","adcode":"110108","businessAreas":[{"name":"五道口","id":"110108","location":{"Q":39.99118,"R":116.34157800000003,"lng":116.341578,"lat":39.99118}},{"name":"牡丹园","id":"110108","location":{"Q":39.977965,"R":116.37172700000002,"lng":116.371727,"lat":39.977965}}],"neighborhoodType":"生活服务;生活服务场所;生活服务场所","neighborhood":"北京航空航天大学","building":"","buildingType":"","street":"学院路","streetNumber":"141号","country":"中国","province":"北京市","city":"","district":"海淀区","township":"花园路街道"},"formattedAddress":"北京市海淀区花园路街道北京航空航天大学北京航空航天大学学院路校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}&sfcyglq=0&sfyzz=0&qtqk=&askforleave=0'
    data = (urllib.parse.parse_qs(encodedStr))
    login(s, username, password)
    myLog.logger.info("get index: %s"% getParam(s).replace('\n', ' '))
    result = upload(s, data)
    myLog.logger.info("upload response: %s" % result.replace('\n', ' '))
    now = time.localtime()
    if ('成功' in result or '您已上报过' in result):
        myLog.logger.info(username + " 填报成功！")
        try:
            if '成功' in result and email != '':
                sendMail( '成功%s 温度上报！'% time.strftime("%Y-%m-%d %H:%M", now), "haha" , email)
        except Exception as e:
            myLog.logger.error(username + ' 发送邮件失败')

        todaySuccess = True
        return True
    else :
        myLog.logger.fatal("填报失败!")
        return False
    s.close()

if __name__ == "__main__":
    with open('config.yaml','r') as f:
        config = yaml.load(f)
    for u in config['users']:
        print(u)
    
    # upload once when start 
    for u in config['users']:
        try:
            if (not report(u['username'], u['password'], u.get('email',''))):
                myLog.logger.error(u['username'] + '上报失败')  
        except:
            myLog.logger.error(u['username'] + '上报失败')


    while True:
        while True:
            now = datetime.datetime.now()
            print(now.hour)
            if (now.hour==18):
                break
            myLog.logger.info("tick : %s",now)
            time.sleep(3660 - now.minute * 60 + random.randint(1,120))
        
        with open('config.yaml','r') as f:
            config = yaml.load(f)
        need = { x for x in range(len(config['users'])) }
        while len(need):
            success = set()
            for index in need:
                u = config['users'][index]
                try:
                    if (not report(u['username'], u['password'], u.get('email',''))):
                        myLog.logger.error(u['username'] + '上报失败')
                    else:
                        success.add(index)
                except Exception as e:
                    myLog.logger.error(u['username'] + '上报失败' + str(e))
            for x in success:
                need.remove(x)
            time.sleep(600)
        time.sleep(3600)
        