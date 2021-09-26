#!/usr/bin/python3
'''if input is one file,then get its hash value;
   if input is two files,then compare them.'''


import hashlib
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
    
    data_list=[]
    for filename in file_list:
        data=[]
        with open(filename,"rb") as f:
            hash_obj={}
            for key in hash_list:
                hash_obj[key]=hash_funs[key]()

            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                for key in hash_obj:
                    hash_obj[key].update(byte_block)
            print(filename)

            for key in hash_obj:
                hex_str=hash_obj[key].hexdigest()
                print('%-15s    %s'%(key,hex_str))
                data.append(hex_str)
            data_list.append(data)
            print('-'*25)

    if len(file_list)==2:
        if data_list[0]==data_list[1]:
            print('YES')
        else:
            print('NO')