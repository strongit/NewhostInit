#!/usr/bin/env python 
def cpu_stat(): 
    cpu = [] 
    cpuinfo = {} 
    f = open("/proc/cpuinfo") 
    lines = f.readlines() 
    f.close() 
    for line in lines: 
        if line == 'n': 
            cpu.append(cpuinfo) 
            cpuinfo = {} 
        if len(line) < 2: continue 
        name = line.split(':')[0].rstrip() 
        var = line.split(':')[1] 
        cpuinfo[name] = var 
    return cpuinfo
if __name__ == '__main__':
    cpuinfo = cpu_stat()
    print cpuinfo
    print cpuinfo['cpu cores']
    print cpuinfo['model name']
    for processor in cpuinfo.keys():
        print('cpuinfo ={0}'.format(cpuinfo[processor]))
