#coding: utf-8
import subprocess
import time
import os
import threading
#file_out = subprocess.Popen('sh /data/shell/test.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#重新构建继承列表的类,报错：AttributeError: 'NoneType' object has no attribute 'append'
class MyList(list):
    def append(self, value):
        super(MyList, self).append(value)
        return self

def sub_out(script):
#    monitime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) + 1)
    file_out = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print file_out
    global moni
    while True:
        if con.acquire():
            thistime = time.time()
            print "sub_out thistime is %s" %thistime
            if moni is None:
                con.notify()
            else:
                con.wait(1)
            con.release()
            time.sleep(10)
    return file_out
#            line = MyList()
#            while True:
#                out = file_out.stdout.readline().strip()
#                line = line.append(out)
#                if subprocess.Popen.poll(file_out)==0:
#                    break
#            return line

def follow(thefile):
#    monitime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) + 10)
    global moni
#    thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open(thefile, 'r', 0) as fh:
        while True:
            if con.acquire():
                line = fh.readline().strip()
                thistime = time.time()
                print "follow thistime is %s" %thistime
                if moni is not None:
                    print line
                    con.notify()
                else:
                    con.wait(1)
                con.release()
                time.sleep(10)
    return line

moni = None
con = threading.Condition()
threads = []
t1 = threading.Thread(target=follow,args=('/data/shell/autodeploy.log',))
threads.append(t1)
t2 = threading.Thread(target=sub_out,args=('sh /data/shell/autodeploy.sh | tee /data/shell/autodeploy.log',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
#         t.setDaemon(True)
         t.start()
#         t.join()
#    os.system('cat /dev/null > /data/shell/autodeploy.log')
    print "Finished %s" %time.ctime()

