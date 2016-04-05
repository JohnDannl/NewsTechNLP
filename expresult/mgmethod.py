#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-18

@author: dannl
'''
import matplotlib.pyplot as plt
syntax_path='/home/dannl/tmp/newstech/dedup/syntac_dup_'
err_path='/home/dannl/tmp/newstech/dedup/err_'
dup_path='/home/dannl/tmp/newstech/dedup/dup_'
out_path='/home/dannl/tmp/newstech/expdata/'

suffix='0306'
err_file=err_path+suffix
dup_file=dup_path+suffix

lsa_out_file=out_path+'lsa_'+suffix
esa_out_file=out_path+'esa_'+suffix
sg_out_file=out_path+'sg_'+suffix
cbow_out_file=out_path+'cbow_'+suffix

def print_precise_recall(pos_file,neg_file,lsa_thres=0.9,esa_thres=0.85,sg_thres=0.9,cbow_thres=0.85):
    pos_list=[]
    with open(pos_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            b=fin.readline().split()
            item='%s --> %s'%(a[0],b[0])
            pos_list.append(item)
    neg_list=[]
    with open(neg_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            b=fin.readline().split()
            item='%s --> %s'%(a[0],b[0])
            neg_list.append(item)    
    lsa_pre={}
    with open(lsa_out_file,'r') as fin:
        for line in fin:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            lsa_pre[line[0]]=sim
    esa_pre={}
    with open(esa_out_file,'r') as fin:
        for line in fin:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            esa_pre[line[0]]=sim
    sg_pre={}
    with open(sg_out_file,'r') as fin:
        for line in fin:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            sg_pre[line[0]]=sim
    cbow_pre={}
    items=[]
    with open(cbow_out_file,'r') as fin:
        for line in fin:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            cbow_pre[line[0]]=sim
            items.append(item)
    pre_pos,pre_neg=[],[]
    for item in items:
        if lsa_pre[item]>=lsa_thres and \
            esa_pre[item]>=esa_thres and \
            sg_pre[item]>=sg_thres and \
            cbow_pre[item]>=cbow_thres:
            pre_pos.append(item)
        else:
            pre_neg.append(item)
#     for item in set(pre_pos).intersection(pos_list):
#         print item
    for item in set(pre_pos)-set(pre_pos).intersection(pos_list):
        print item
    true_pos=len(set(pre_pos).intersection(pos_list))
    print true_pos
    true_neg=len(set(pre_neg).intersection(neg_list))
    ran_msg='ran_p:%.5f'%(len(pos_list)/float(len(pos_list)+len(neg_list)))    
    pos_msg='pre:%d,pos:%d,p:%.5f,r:%.5f'%(len(pre_pos),len(pos_list),
                                           true_pos/float(len(pre_pos)),
                                           true_pos/float(len(pos_list)))
    
    neg_msg='pre:%d,neg:%d,p:%.5f,r:%.5f'%(len(pre_neg),len(neg_list),
                                           true_neg/float(len(pre_neg)),
                                           true_neg/float(len(neg_list)))
    
    tot_msg='p:%.5f,r:%.5f'%((true_pos+true_neg)/float(len(pre_pos)+len(pre_neg)),
                             (true_pos+true_neg)/float(len(pos_list)+len(neg_list)))
    print ran_msg
    print pos_msg
    print neg_msg
    print tot_msg


pos_file=dup_file
neg_file=err_file
# print_precise_recall(pos_file,neg_file,lsa_thres=0.79,esa_thres=0.69,sg_thres=0.90,cbow_thres=0.84)
print_precise_recall(pos_file,neg_file,lsa_thres=0.79,esa_thres=0.69,sg_thres=0.9,cbow_thres=0.84)