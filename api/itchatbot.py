#coding:utf-8
import os
import re
import shutil
import time
import sqlite3
import itchat
import json
import requests
from itchat.content import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

jianjie = {

}
a = jianjie.keys() 

msg_dict = {}
rev_tmp_dir = "/root/wxbot/file"
face_bug = None

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def getip(ip):
    site = 'http://ip.taobao.com//service/getIpInfo.php?ip=' + ip
    r = requests.get(site, headers=headers)
    rdata = r.json().get('data')
    code = r.json()['code']
    if code == 0:
        ipp = rdata['ip']
        city = rdata['city']
        isp = rdata['isp']
        rr = u'小黄人偷偷的告诉你IP:%s是来自%s的,运营商为%s' % (ipp,city,isp)    
    else:
        rr = u'你不要骗我，这个ip不存在的！'
    return rr


conn = sqlite3.connect('wx.db')
print 'good db!'
cur = conn.cursor()
#cur.execute("DROP TABLE SHENDUNJU ")
#cur.execute("CREATE TABLE SHENDUNJU (ID TEXT,NAME TEXT,TIME TEXT,MESSAGE TEXT);")

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
#@itchat.msg_register(TEXT, isGroupChat=True)
def group_text(msg):
    global name
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_time = msg['CreateTime']
    msg_content = msg['Content']
    msg_shar_url = None 
    content = msg['Text']
    name = content[5:]


    #print msg['MsgId'].encode('utf-8')
    #print msg['ActualUserName'].encode('utf-8')
    #print msg['CreateTime']
    #print type(msg['CreateTime'])
    #print msg['Content'].encode('utf-8')
    
    if msg['isAt'] and (name in jianjie.keys()):
        itchat.send_msg(jianjie[name], msg['FromUserName'])

    if msg['isAt'] and ('ip' in msg['Text']):
	ipa = msg['Text']
	ipa = re.findall(r'\d+.\d+.\d+.\d+', ipa)
	ip = ipa[0]
	itchat.send(getip(ip), msg['FromUserName'])
    
    while 1:
        if msg:
            all_msg = [
                msg['MsgId'].decode('utf-8'),
                msg['ActualUserName'].decode('utf-8'),
                msg['CreateTime'],
                msg['Content'].decode('utf-8')
                ]
            cur.executemany("INSERT INTO SHENDUNJU VALUES (?,?,?,?)",all_msg)
            conn.commit()
    
    cur.execute('SELECT * FROM SHENDUNJU')
    print cur.fetchone()
    print cur.fetchall()

    mmm = msg['Content'].encode('utf-8')
    if u'撤回了一条消息' in msg['Content']:
        print 'HAHAHAHAH'
    else:
        with open('wx.txt', 'w') as f:
            f.write(mmm)
    
        with open('wx.txt', 'r') as f:
	    global lll
            lines = f.readlines()
            lll = lines[-1]
    aaa = u'被我看到了，你撤回的消息是:%s' % lll

    if msg['MsgType'] == 10002:
	aaa = cur.execute("SELECT MESSAGE FROM SHENDUNJU")
	itchat.send_msg(aaa, msg['FromUserName'])
	print type(msg)


    cur.close()
    conn.close()
itchat.auto_login(hotReload=True, enableCmdQR=2)
admin = itchat.search_friends(name=u'大叔')
admin = admin[0]['UserName']
if __name__ == "__main__":
    try:
        itchat.send(u'机器人上线!', toUserName=admin)
	itchat.run()
	itchat.send(u'机器人下线!', toUserName=admin)
    except KeyboardInterrupt:
	itchat.logout()
