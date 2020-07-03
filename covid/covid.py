
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

s = requests.session()
username = 北航账号名
password = 北航密码
todaySuccess = False

def login():
    url = "https://app.buaa.edu.cn/uc/wap/login/check"
    data = {"username":username,"password":password}
    try:
        response = s.get(url, data = data, timeout = 10)
        myLog.logger.info("login cookie : %s"%str(response.headers["set-cookie"]))
    except requests.RequestException:
        myLog.logger.error("无法登陆")
        return None

def getParam():
    url = "https://app.buaa.edu.cn/ncov/wap/default/index"
    try:
        response = s.get(url, timeout = 10)
        return response.text
    except requests.RequestException:
        myLog.logger.error("无法获取上次数据")
        return None

def upload(data):
    url = 'https://app.buaa.edu.cn/ncov/wap/default/save'
    try:
        response = s.post(url, data=data, timeout = 10)
        return response.text
    except requests.RequestException:
        myLog.logger.error("上次失败")
        return None

def report():
    global todaySuccess

    html = (getParam())
    pattern = re.compile( r'oldInfo: (\{.*\})')
    data = pattern.findall(html)

    if data:
        data = json.loads(data[0])
        del data["created_uid"]
        data["sfsqhzjkk"  ]  = ""
        data["sfygtjzzfj" ]  = ""
        data["gwszdd"     ]  = ""
        data["sfyqjzgc"   ]  = ""
        data["jrsfqzys"   ]  = ""
        data["jrsfqzfy"   ]  = ""
        data['created'] = str(int(time.time()))
        data['date'] = time.strftime("%Y%m%d", time.localtime())
        pattern = re.compile(r'def = (\{.*\})')
        data2 = pattern.findall(html)
        data2 = json.loads(data2[0])
        data["id"] = data2["id"]
        myLog.logger.info("get json data: %s",json.dumps(data))
    else:
        myLog.logger.error("can't get json data,retry login")
        login()
        return False
    result = upload(data)
    myLog.logger.info("upload response: %s" % result)
    now = time.localtime()
    if ('成功' in result or '今天已经填报了' in result):
        myLog.logger.info("填报成功！")
        sendMail( '成功%s 疫情信息填报成功！'% time.strftime("%Y-%m-%d %H:%M", now), "haha" )
        todaySuccess = True
        return True
    else :
        myLog.logger.fatal("填报失败!")
        sendMail( '失败%s 疫情信息填报失败！'% time.strftime("%Y-%m-%d %H:%M", now), "sad~" )
        return False

retryTime = 10
if __name__ == "__main__":
    while True:
        while True:
            now = datetime.datetime.now()
            if (now.hour==0):
                todaySuccess = False
            if (not todaySuccess):
                break
            myLog.logger.info("tick : %s",now)
            time.sleep(3660 - now.minute * 60 + random.randint(1,120))
        try:
            if report():
                now = datetime.datetime.now()
                time.sleep(3660 - now.minute * 60 + random.randint(1,120))
            else :
                time.sleep(retryTime)
        except Exception as e:
            myLog.logger.error(str(e))
            time.sleep(retryTime)







