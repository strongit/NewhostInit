#!/usr/bin/env python 
def uptime_stat(): 
    uptime = {} 
    f = open("/proc/uptime") 
    con = f.read().split() 
    f.close() 
    all_sec = float(con[0]) 
    MINUTE,HOUR,DAY = 60,3600,86400 
    uptime['day'] = int(all_sec / DAY ) 
    uptime['hour'] = int((all_sec % DAY) / HOUR) 
    uptime['minute'] = int((all_sec % HOUR) / MINUTE) 
    uptime['second'] = int(all_sec % MINUTE) 
    uptime['Free rate'] = float(con[1]) / float(con[0]) 
    return uptime

if __name__ == '__main__':
    uptime = uptime_stat()
    print uptime
