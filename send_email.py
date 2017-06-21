#!/usr/bin/python
# coding : utf-8

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os, sys

print("begin")
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, str) else addr))

from_addr = '1531040932@qq.com'
password = 'fpnvshrchyxtjhff'
smtp_server = 'smtp.qq.com'
to_addr = '764676555@qq.com'

text = sys.argv[1] + " error mail"
msg = MIMEText(text, 'plain', 'utf-8')
msg['From'] = _format_addr('<%s>' % from_addr)
msg['To'] = _format_addr('<%s>' % to_addr)
msg['Subject'] = Header('ERROR mail', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 587) 
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
print("end")