# buaa_spider

## 北hang疫情信息每日自动填报
- 每天0点1-3分随机时间上报
- 上报信息为你的昨日填报信息
- 上报结果会发qq邮件通知,需要你的qq邮箱[开启SMTP功能 、获得授权码](https://jingyan.baidu.com/article/b0b63dbf1b2ef54a49307054.html)


参数填写：
```
# covid.py
username = "name"
password = "password"
# mail.py
_user = "bigerous@qq.com" #发件邮箱
_pwd  = "asdfasdfgdsfa"   #授权码
_to   = "bigerous@qq.com" #收件人
```
运行:
```
python3 covid.py 
```

## 温度每日上报
- 每天18：05左右上报
- 可以在temperature/config.yaml中填写多人的账号，一起上报
- 其他的与疫情上报类似
