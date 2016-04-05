#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-16

@author: dannl
'''
syntac_dup_path='/home/dannl/tmp/newstech/dedup/syntac_dup_'
err_path='/home/dannl/tmp/newstech/dedup/err_'
dup_path='/home/dannl/tmp/newstech/dedup/dup_'

class SimPair(object):
    def __init__(self,head,a,b):
        self.head=head
        self.a=a
        self.b=b
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.head == other.head
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)
    
def extract_err(i):    
    pre_list=[]
    dup_list=[]
    suf_str='%02d%02d'%(i,i+1)
    with open(syntac_dup_path+suf_str,'r') as fin:
        while True:
            head=fin.readline() # ignore the first line
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            pre_list.append(SimPair(head,a,b))        
    with open(dup_path+suf_str,'r') as fin:
        while True:
            head=fin.readline() # ignore the first line
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            dup_list.append(SimPair(head,a,b))  
#         print len(pre_list),len(dup_list)      
    for dup_one in dup_list:
        if dup_one not in pre_list:
            print dup_one.head
        else:
            pre_list.remove(dup_one)
    with open(err_path+suf_str,'w') as fout:
        for err_one in pre_list:
            fout.write(err_one.head)
            fout.write(err_one.a)
            fout.write(err_one.b)
                        
def extract_dup(i):
    pre_list=[]
    err_list=[]
    suf_str='%02d%02d'%(i,i+1)
    with open(syntac_dup_path+suf_str,'r') as fin:
        while True:
            head=fin.readline() # ignore the first line
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            pre_list.append(SimPair(head,a,b))        
    with open(err_path+suf_str,'r') as fin:
        while True:
            head=fin.readline() # ignore the first line
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            err_list.append(SimPair(head,a,b))  
#         print len(pre_list),len(err_list)      
    for err_one in err_list:
        if err_one not in pre_list:
            print err_one.head
        else:
            pre_list.remove(err_one)
    with open(dup_path+suf_str,'w') as fout:
        for dup_one in pre_list:
            fout.write(dup_one.head)
            fout.write(dup_one.a)
            fout.write(dup_one.b)


if __name__=='__main__':    
    extract_err(2) # 2,3 or 4
#     extract_dup(6) # 5 or 6
