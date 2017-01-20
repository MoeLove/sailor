#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import logging
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

from conf import SENDER_ADDR, SENDER_PASSWD, SMTP_SERVER

logger = logging.getLogger("root")


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail(receive_addrs, msg_type=None, is_ssl =False, **kwargs):
    u"""Send email function

    :arg list receive_addrs: 收件人列表

    :arg str msg_type: 消息类型
         options:
             test: Test

    :arg bool ssl_type: 发送邮件时是否使用SSl来连接服务器, 有时会出现连接超时的情况

    """
    sender_addr = SENDER_ADDR
    sender_passwd = SENDER_PASSWD
    server = smtplib.SMTP(host=SMTP_SERVER['host'], port=SMTP_SERVER['ssl_port'] if is_ssl else SMTP_SERVER['port'])

    try:
        server.login(sender_addr, sender_passwd)
        server.set_debuglevel(1)
        server.sendmail(sender_addr, receive_addrs, format_msg(sender_addr, receive_addrs, msg_type, **kwargs))
    except Exception, e:
        print e
        logger.error(str(e))


def format_msg(sender_addr, receive_addrs, msg_type, **kwargs):
    """format msg function
    """
    if msg_type == 'test':
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header('Sailor'.format(**kwargs), 'utf-8').encode()
        html = MIMEText(
            '''您好:<br/><br/>
            登陆 MoeLove 官网 <a href="{url}">{url}</a> <br/>
            <img src="cid:img1"><br/><br/>
            '''.format(**kwargs), 'html', 'utf-8')
        msg.attach(html)

        fimg1 = open('img1.png', 'rb')
        img1 = MIMEImage(fimg1.read())
        fimg1.close()
        img1.add_header('Content-ID', '<img1>')
        msg.attach(img1)
    else:
        raise Exception

    msg['From'] = _format_addr(u'MoeLove <%s>' % sender_addr)
    msg['To'] = ','.join(receive_addrs)

    return msg.as_string()


if __name__ == '__main__':
    send_mail(['me@moelove.info'], 'test',  url="http://moelove.info")
