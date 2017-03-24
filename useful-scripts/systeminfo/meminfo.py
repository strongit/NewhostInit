#!/usr/bin/env python 
import sys, os
reload(sys)
def memory_stat(): 
    mem = {} 
    f = open("/proc/meminfo") 
    lines = f.readlines() 
    f.close() 
    for line in lines: 
        if len(line) < 2: continue 
        name = line.split(':')[0] 
        var = line.split(':')[1].split()[0] 
        mem[name] = long(var) * 1024.0 
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached'] 
    return mem
if __name__ == '__main__':
    meminfo = memory_stat()
    print("Total Used:{0}".format(meminfo['MemUsed']/1024/1024))
