#!/usr/bin/python3
#compare files of two paths according to sha256 and show their differences. 

from pathlib import Path
import sys
import hashlib

def get_weight(file_size):
    if file_size<1024:
        weight=0
    elif file_size<1024**2:
        weight=1
    elif file_size<1024**3:
        weight=2
    elif file_size<1024**4:
        weight=3
    else:
        weight=4
    
    return weight

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
    weight_list=['B','KB','MB','GB','TB']
    hash_funs={
        'md5':hashlib.md5,
        'sh1':hashlib.sha1,
        'sha256':hashlib.sha256,
        'blake2b':hashlib.blake2b,
        'blake2s':hashlib.blake2s,
        }
    hash_use='md5'

    print('start:')
    print('~'*50)

    for item in path_list:
        i=0
        file_size=0
        mqueue.append(item)
        dir_deep=len(item.parts)
        dir_hash={}
        while len(mqueue)!=0:
            file=mqueue.pop(0)
            if file.is_dir() and not file.is_symlink():
                for item2 in file.iterdir():
                    mqueue.append(item2)
            elif file.is_file() and not file.is_symlink():
                i+=1
                msize=file.stat().st_size
                file_size+=msize
                # print('%s %8.2f %8.2f'%(str(file),msize/(1024**2),file_size/(1024**2)))

                with open(file,"rb") as f:
                    hash_current=hash_funs[hash_use]()

                    # Read and update hash string value in blocks of 4K*1024*10(that is 40MB)
                    for byte_block in iter(lambda: f.read(4096*1024*10),b""):
                        hash_current.update(byte_block)

                    hex_str=hash_current.hexdigest() 
                    dir_list=file.resolve().parts[dir_deep:]
                    dir_hash['/'.join(dir_list)]=hex_str
                    # print('%-15s    %s'%('/'.join(dir_list),hex_str))
                if not i%10:
                    weight=get_weight(file_size)
                    print('no.%-8d  %6.3f %s  %s'%(i,file_size/(1024**weight),weight_list[weight],str(file)))
        weight=get_weight(file_size)
        print('sum: %-8d  size: %8.3f %s %s'%(i,file_size/(1024**weight),weight_list[weight],str(item)))
        print('+'*50)
        res.append(dir_hash)

    print('compare result:')
    print('~'*50)

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
    