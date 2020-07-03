
import smtplib
from email.mime.text import MIMEText

_user = qq邮箱   # "bigerous@qq.com"
_pwd  = qq邮箱   # "asdfasdfgdsfa"
_to   = 收件邮箱  # "bigerous@qq.com"

def sendMail(subject, text):
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"]    = _user
    msg["To"]      = _to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
    except smtplib.SMTPException as e: 
        print ("Falied,%s" %e) 