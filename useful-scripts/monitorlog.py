#!/usr/bin/python
# encoding=utf-8
# Filename: monitorLog.py
import os
import signal
import subprocess
import time
 
 
logFile1 = "test1.log"
logFile2 = 'test2.log'
 
#日志文件一般是按天产生，则通过在程序中判断文件的产生日期与当前时间，更换监控的日志文件
#程序只是简单的示例一下，监控test1.log 10秒，转向监控test2.log
def monitorLog(logFile):
    print '监控的日志文件 是%s' % logFile
    # 程序运行10秒，监控另一个日志
    stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 10))
    popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, <a href="http://www.ttlsa.com/shell/" title="shell"target="_blank">shell</a>=True)
    pid = popen.pid
    print('Popen.pid:' + str(pid))
    while True:
        line = popen.stdout.readline().strip()
        # 判断内容是否为空
        if line:
            print(line)
        # 当前时间
        thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if thistime >= stoptime:
            # 终止子进程
            popen.kill()
            print '杀死subprocess'
            break
    time.sleep(2)
    monitorLog(logFile2)
 
if __name__ == '__main__':
    monitorLog(logFile1)
