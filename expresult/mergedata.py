#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-18

@author: dannl
'''
syntax_path='/home/dannl/tmp/newstech/dedup/syntac_dup_'
err_path='/home/dannl/tmp/newstech/dedup/err_'
dup_path='/home/dannl/tmp/newstech/dedup/dup_'

class Entry(object):
    def __init__(self,head,a,b):
        self.head=head
        self.a=a
        self.b=b
        
def merge_data(file_path):
    item_dic={}
    for i in xrange(3,6):
        suffix='%02d%02d'%(i,i+1)
        print suffix
        with open(file_path+suffix,'r') as fin:
            while True:
                head=fin.readline()
                if not head:
                    break
                a=fin.readline()
                b=fin.readline()
                a_id=a.split()[0]
                b_id=b.split()[0]
                e_key='%s --> %s'%(a_id,b_id)
                if e_key not in item_dic:
                    item_dic[e_key]=Entry(head,a,b)
                else:
                    print e_key
    output_file=file_path+'0306'
    with open(output_file,'w') as fout:
        for item in item_dic.values():
            print >> fout,item.head,
            print >> fout,item.a,
            print >> fout,item.b,
            
def check_merge():
    suffix='0306'
    syntax_file=syntax_path+suffix
    err_file=err_path+suffix
    dup_file=dup_path+suffix
    dup_dic={}    
    with open(dup_file,'r') as fin:
        while True:
            head=fin.readline()
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            a_id=a.split()[0]
            b_id=b.split()[0]
            e_key='%s --> %s'%(a_id,b_id)
            if e_key not in dup_dic:
                dup_dic[e_key]=Entry(head,a,b)
            else:
                print e_key
    err_dic={}    
    with open(err_file,'r') as fin:
        while True:
            head=fin.readline()
            if not head:
                break
            a=fin.readline()
            b=fin.readline()
            a_id=a.split()[0]
            b_id=b.split()[0]
            e_key='%s --> %s'%(a_id,b_id)
            if e_key not in err_dic:
                err_dic[e_key]=Entry(head,a,b)
            else:
                print e_key
    for item in err_dic:
        if item in dup_dic:
            print item
# merge_data(syntax_path)
# merge_data(dup_path)
# merge_data(err_path)
check_merge()