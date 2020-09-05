
import smtplib
import yaml
from email.mime.text import MIMEText



with open('config.yaml','r') as f:
        config = yaml.load(f)
_user = config['mail_sender']['from']
_pwd  = config['mail_sender']['password']    

def sendMail(subject, text, to):
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"]    = _user
    msg["To"]      = to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, to, msg.as_string())
        s.quit()
    except smtplib.SMTPException as e: 
        print ("Falied,%s" %e) 
    return