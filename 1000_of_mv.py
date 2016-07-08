# -*- coding: utf-8 -*- 
import os 
import shutil
def Test1(rootDir): 
    list_dirs = os.walk(rootDir) 
    count=0
    for root, dirs, files in list_dirs: 
        for d in dirs: 
            print os.path.join(root, d)      
        if os.listdir("/data/file/S10032666/"):
            print "目录非空，请清空文件。"
            return 0
        else:
            for f in files: 
                if count < 1000:
                    count=count +1
                    f = os.path.join(root, f)
                    shutil.move(f,"/data/file/S10032666/")
                    print os.path.join(root, f) 
                else:
                    return 0

Test1("/data/S10032666_bak/")
