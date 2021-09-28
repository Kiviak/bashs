#!/usr/bin/python3
#compare files of two paths according to sha256 and show their differences. 

from pathlib import Path
import sys
import hashlib

if __name__=='__main__':
    
    argc=len(sys.argv) 
    if argc!=3:
        exit(1)

    path_list=[Path(item).resolve() for item in sys.argv[1:]]
    for item in path_list:
        if not item.is_dir():
            exit(2)
    
    mqueue=[]
    res=[]
    for item in path_list:
        mqueue.append(item)
        dir_deep=len(item.parts)
        dir_hash={}
        while len(mqueue)!=0:
            file=mqueue.pop(0)
            if file.is_dir() and not file.is_symlink():
                for item in file.iterdir():
                    mqueue.append(item)
            elif file.is_file() and not file.is_symlink():
                with open(file,"rb") as f:
                    hash_256=hashlib.sha256()

                    # Read and update hash string value in blocks of 4K*1024*10(that is 40MB)
                    for byte_block in iter(lambda: f.read(4096*1024*10),b""):
                        hash_256.update(byte_block)

                    hex_str=hash_256.hexdigest() 
                    dir_list=file.resolve().parts[dir_deep-1:]
                    dir_hash['/'.join(dir_list)]=hex_str
                    # print('%-15s    %s'%('/'.join(dir_list),hex_str))
        res.append(dir_hash)

    # print('compare result:')
    print(str(path_list[0]),':\n')
    dir1,dir2=res[0],res[-1]
    i=0
    for key in dir1:
        if key in dir2 and dir1[key]==dir2[key]:
            continue
        else:
            i+=1
            print('%-10d %s'%(i,key))
            # print('%-15s    %s'%(key,dir1[key]))

    print('-'*50)
    print('-'*50)

    i=0
    print(str(path_list[-1]),':\n')
    for key in dir2:
        if key in dir1:
            continue
        else:
            i+=1
            print('%-10d %s'%(i,key))
            # print('%-15s    %s'%(key,dir2[key]))
    