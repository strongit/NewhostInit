# -*- coding:utf-8 -*-
"""
https://github.com/littlecodersh/ItChat
根据itchat编写微信报警机器人
"""
import itchat
import email
import imaplib
from email.parser import Parser
from HTMLParser import HTMLParser
reload(sys)
sys.setdefaultencoding('utf8')

imapserver = "your imap and port"
username = "your username"
password = "your passwd"
itchat.auto_login(hotReload=True)
admin = itchat.search_friends(name=u'大叔')
admin = admin[0]['UserName']

def getEmail():
    conn = imaplib.IMAP4(imapserver,143)
    conn.login(username, password)
    conn.select("INBOX")
    state, data = conn.search(None, 'ALL')
    elist = data[0].split()
    state,data=conn.fetch(elist[len(elist)-1],'(RFC822)')
    msg=email.message_from_string(data[0][1])
    msg_content=msg.get_payload(decode=True)
    return msg_content

class MyHTMLParser(HTMLParser):  
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.flag = False  
        self.list = []
    def handle_starttag(self, tag, attrs):

        if tag == 'td':
            for (variable, value) in attrs:
                if variable == 'style':
                    self.flag = True
    def handle_data(self,data):
        if self.flag:
            self.list.append(data)

def alarmInfo():
    getemail = getEmail()
    parser = MyHTMLParser()
    parser.feed(getemail)
    parlist = parser.list
    emailtext = ''.join(parlist).replace("\t","").replace("\r\n","").replace(" ","")
    emailtext = emailtext.decode('utf-8')\
    .replace('攻击事件报告',' 攻击事件报告如下：')\
    .replace('事件概况：','\n事件概况：\n')\
    .replace('事件解释：', '\n事件解释：\n')\
    .replace('安全处置建议', '\n安全处置建议')\
    .replace('1、临时处理方案：', '\n1、临时处理方案')\
    .replace('2、漏洞处理', '\n2、漏洞处理')\
    .replace('3、事件动态追踪', '\n3、事件动态追踪')
    return emailtext


@itchat.msg_register(itchat.content.TEXT)
def reply_text(msg):
    if u'报警邮件' in msg['Text']:
        itchat.send_msg(alarmInfo, toUserName=admin)


if __name__ == "__main__":   
    alarmInfo = alarmInfo()
    while 1:
        time.sleep(60*60*60)
        itchat.send_msg(alarmInfo, toUserName=admin)
    itchat.run()
