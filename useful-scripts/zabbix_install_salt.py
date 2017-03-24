#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 通过zabbix自动发现策略自动添加主机，得到的ip地址批量修改salt-minion的ID

import sys,string
import MySQLdb
import salt.client
reload(sys)
sys.setdefaultencoding('utf-8')
 
def get_ip():
    file = open('test_hosts', 'w')
    file.truncate()
    res = ()
 
    con = MySQLdb.connect(host='192.168.2.223',user='zabbix',passwd='zabbix',db='zabbix',charset='utf8')
    cur = con.cursor()
 
    cur.execute('select host from hosts where available=1 order by host;')
    file = open('test_hosts', 'a')
    for data in cur.fetchall():
        file.write(data[0] + '\n')
        res = res + data

    return res

def salt_cmd(ip,cmd):
    c = salt.client.LocalClient()
    c.cmd(ip,cmd)

#if __name__=="__main__":
    ips = get_ip()
    print ips
#    for ip in ips:
#        salt_cmd(ip,'yum install salt-minion -y')
