#!/usr/bin/python3

import hashlib
import pathlib
import argparse

if __name__=='__main__':
    
    description='''Compute hash value:
    if input is one file,then compute its hash value;
    if input is two files,then compare them.'''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file',nargs='+',type=str)
    args=parser.parse_args()
    if len(args.file)>2:
        exit(1)
 
    hash_list=['md5','sh1','sha256']
    hash_funs={
        'md5':hashlib.md5,
        'sh1':hashlib.sha1,
        'sha256':hashlib.sha256,
        'blake2b':hashlib.blake2b,
        'blake2s':hashlib.blake2s,
        }
    
    print('start:')
    print('-'*50)

    data_list=[]
    for filename in args.file:
        data=[]
        file_size=0
        filename=pathlib.Path(filename)
        msize=filename.stat().st_size
        print('%s    %20.3f MB\n'%(str(filename.resolve()),msize/(1024**2)))

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

            for key in hash_obj:
                hex_str=hash_obj[key].hexdigest()
                print('%-15s    %s'%(key,hex_str))
                data.append(hex_str)
            data_list.append(data)
            print('-'*50)

    if len(args.file)==2:
        if data_list[0]==data_list[1]:
            print('\nresult:%10s\n'%('YES'))
        else:
            print('\nresult:%10s\n'%('NO'))