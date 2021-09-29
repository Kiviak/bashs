#!/usr/bin/python3
'''if input is one file,then get its hash value;
   if input is two files,then compare them.'''


import hashlib
import pathlib
import sys

if __name__=='__main__':
    
    argc=len(sys.argv) 
    if argc<2 or argc>3:
        exit(1)
 
    file_list=sys.argv[1:]

    hash_list=['md5','sh1','sha256']
    hash_funs={
        'md5':hashlib.md5,
        'sh1':hashlib.sha1,
        'sha256':hashlib.sha256,
        'blake2b':hashlib.blake2b,
        'blake2s':hashlib.blake2s,
        }
    
    print('start:')
    print('~'*50)

    data_list=[]
    for filename in file_list:
        data=[]
        file_size=0
        filename=pathlib.Path(filename)
        msize=filename.stat().st_size
        print('size:%8.3f MB  %s\n'%(msize/(1024**2),str(filename.resolve())))

        with open(filename,"rb") as f:
            hash_obj={}
            for key in hash_list:
                hash_obj[key]=hash_funs[key]()

            # Read and update hash string value in blocks of 4K*1024*10(that is 40MB)
            block_size=4096*1024*10
            i=0
            for byte_block in iter(lambda: f.read(block_size),b""):
                file_size+=block_size
                i+=1
                if not i%5:
                    print('%4.2f%%'%(file_size*100/msize))
                for key in hash_obj:
                    hash_obj[key].update(byte_block)

            print('-'*50)
            print(str(filename.resolve()),'\n')
            for key in hash_obj:
                hex_str=hash_obj[key].hexdigest()
                print('%-15s    %s'%(key,hex_str))
                data.append(hex_str)
            data_list.append(data)
            print('-'*50)

    if len(file_list)==2:
        if data_list[0]==data_list[1]:
            print('YES')
        else:
            print('NO')