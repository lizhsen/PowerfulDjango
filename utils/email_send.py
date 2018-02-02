# -*- coding: utf-8 -*-
from users.models import EmailVerifyRecord
import random
from MxOnline.settings import EMAIL_FROM

from django.core.mail import send_mail


def random_str(randomlength=8):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "李志森在线教育网站注册账号"
        email_body = "请点击下面的连接激活账号：http:/127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    if send_type == "forget":
        email_title = "李志森在线教育网站更改密码"
        email_body = "请点击下面的连接更改账号密码：http:/127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

