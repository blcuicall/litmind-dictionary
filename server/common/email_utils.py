# -*- coding: utf-8 -*-

import email.mime.text
import email.mime.multipart
import smtplib


def send_email(toAddress, code):


    try:
        msg = email.mime.multipart.MIMEMultipart()
        msg['Subject'] = '验证码'
        msg['From'] = ''
        msg['To'] = toAddress

        content = "您的验证码为：" + "<p>" + code + "</p>"
        txt = email.mime.text.MIMEText(content, 'html', 'utf-8')
        msg.attach(txt)

        from_addr = ''
        to_addr = [toAddress]
        smtp_server = ''

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login('', '')
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False
