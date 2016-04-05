#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-17

@author: dannl
'''
import matplotlib.pyplot as plt
syntax_path='/home/dannl/tmp/newstech/dedup/syntac_dup_'
err_path='/home/dannl/tmp/newstech/dedup/err_'
dup_path='/home/dannl/tmp/newstech/dedup/dup_'
out_path='/home/dannl/tmp/newstech/expdata/'

def print_precise_recall(pos_file,neg_file,sim_file,thres):
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
    pre_pos,pre_neg=[],[]
    with open(sim_file,'r') as fin:
        for line in fin:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            if sim <thres:
                pre_neg.append(item)
            else:
                pre_pos.append(item)
    true_pos=len(set(pre_pos).intersection(pos_list))
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

def plot_precise_recall(pos_file,neg_file,sim_file):
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
    sim_list=[]
    with open(sim_file,'r') as fin:
        for line in fin:
            sim_list.append(line.strip())
    precises,recalls=[],[]    
    x=[i*0.02 for i in xrange(50)]
    for thres in x:
        pre_pos=[]
        for line in sim_list:
            line=line.split(':')
            item,sim=line[0],float(line[1])
            if sim >=thres:
                pre_pos.append(item)
        true_pos=len(set(pre_pos).intersection(pos_list))
        if len(pre_pos)==0:
            p,r=1.0,0
        else:
            p,r=true_pos/float(len(pre_pos)),true_pos/float(len(pos_list))
        precises.append(p)
        recalls.append(r)
    plt.figure(1)    
    plt.plot(x,precises,'k',linewidth=1.5)
    
#     plt.ylim(0.7,1.0)    
#     plt.plot(x[45],precises[45],'k*')
#     plt.plot((x[45],x[45]),(0,precises[45]),'k--')
#     plt.plot((0,x[45]),(precises[45],precises[45]),'k--')
#     plt.annotate('(0.9,0.82766)', xy=(x[45],precises[45]), xycoords='data',
#                 xytext=(-100, 30), textcoords='offset points',
#                 arrowprops=dict(arrowstyle="->",
#                                 connectionstyle="arc,angleA=0,armA=50,rad=10"),
#                 )
    
    plt.title('Precise to different similarity thresholds',y=-0.1)
    plt.figure(2)
    plt.plot(x,recalls,'k',linewidth=1.5)
    
#     plt.plot(x[45],recalls[45],'k*')
#     plt.plot((x[45],x[45]),(0,recalls[45]),'k--')
#     plt.plot((0,x[45]),(recalls[45],recalls[45]),'k--')
#     plt.annotate('(0.9,0.64833)', xy=(x[45],recalls[45]), xycoords='data',
#                 xytext=(-100, 30), textcoords='offset points',
#                 arrowprops=dict(arrowstyle="->",
#                                 connectionstyle="arc,angleA=0,armA=50,rad=10"),
#                 )
    
    plt.title('Recall to different similarity thresholds',y=-0.1)
    plt.show()
    
suffix='0306'
err_file=err_path+suffix
dup_file=dup_path+suffix
syntax_file=syntax_path+suffix

lsa_out_file=out_path+'lsa_'+suffix
esa_out_file=out_path+'esa_'+suffix
sg_out_file=out_path+'sg_'+suffix
cbow_out_file=out_path+'cbow_'+suffix
glove_out_file=out_path+'glove_'+suffix

pos_file=dup_file
neg_file=err_file

# sim_file=lsa_out_file
# sim_file=esa_out_file
# sim_file=sg_out_file
sim_file=cbow_out_file

print_precise_recall(pos_file,neg_file,sim_file,0.85)
# plot_precise_recall(pos_file,neg_file,sim_file)