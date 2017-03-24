#!/usr/bin/env python 
def disk_stat(): 
    import os 
    hd={} 
    disk = os.statvfs("/") 
    hd['available'] = disk.f_bsize * disk.f_bavail 
    hd['capacity'] = disk.f_bsize * disk.f_blocks 
    hd['used'] = disk.f_bsize * disk.f_bfree 
    return hd

if __name__=='__main__':
    diskinfo = disk_stat()
    print diskinfo
