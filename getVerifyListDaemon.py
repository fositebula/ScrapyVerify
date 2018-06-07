import requests
from config import *
import subprocess
import time

import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests import ConnectionError
from smtpd import COMMASPACE

def send_mail(sub, content, send_mail_list):
    try:
        mail_obj = smtplib.SMTP(SMPT_HOST, SMPT_PORT)
        mail_obj.docmd(DOCMD, MAIL_ACCOUNT)
        mail_obj.starttls()
        mail_obj.login(MAIL_ACCOUNT, PASSWD)
        msg = MIMEMultipart()
        msg['From'] = MAIL_FROM
        msg['To'] = COMMASPACE.join(send_mail_list)
        msg['Subject'] = sub
        con = MIMEText(content, 'html', 'utf-8')
        msg.attach(con)
        mail_obj.sendmail(MAIL_ACCOUNT, send_mail_list, msg.as_string())
        mail_obj.quit()
    except:
        traceback.print_exc()

def get_time_stamp():
    ltime = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", ltime)

def scrapy_verify_page():
    try:
        out = open('log/daemon_{}_out'.format(get_time_stamp()), 'w')
        err = open('log/daemon_{}_err'.format(get_time_stamp()), 'w')
        cmd = ['scrapy', 'crawl', 'cmverify', '-o', BRANCHS_PROJECTS]
        log = subprocess.Popen(cmd, stdout=out, stderr=err, cwd=CWD)
        log.wait()
        if log.returncode != 0:
            content = "<b>Scrapy return code %s</b><br>"%log.returncode
            subject = "Scrapy occur some error!"
            send_mail(subject, content, TO_SOMEONE)
            return log.returncode
        return 'ok'
    except:
        send_mail('Scrapy Exception', traceback.format_exc(), TO_SOMEONE)
        traceback.print_exc()
        return False

def scrapyVerify():
    ret = scrapy_verify_page()
    # print ret
    if ret == 'ok':
        with open(BRANCHS_PROJECTS) as fd:
            j_str = fd.read()
            try:
                res = requests.post(WHITE_URL, data=j_str)
                # print 'requests status_code {}'.format(res.status_code)
                return res.status_code
            except ConnectionError:
                send_mail('Scrapy Exception', 'requests Exception ConnectionError!', TO_SOMEONE)
                return 'requests Exception ConnectionError!'
    return 'Scrapy fail!'

if __name__ == '__main__':
    print scrapyVerify()