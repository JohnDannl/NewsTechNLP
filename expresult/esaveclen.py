#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-2

@author: dannl
'''
import matplotlib.pyplot as plt
from collections import Counter

news_file='/home/dannl/tmp/newstech/data/merge1_title'
veclen_file='/home/dannl/tmp/newstech/expresult/esaveclen.txt'

def get_vec_len(input_file,output_file):
    from newsesa import esa2sim
    vec_lens=[]
    with open(input_file,'r') as fin:
        count=0
        for line in fin:            
            line=line.split()[1:]            
            vec=esa2sim._get_concept_vec_prune(line,prune_at=0.2)
            vec_lens.append(len(vec))
            count+=1
            if count%200==0:
                print count,line
    with open(output_file,'w') as fout:
        for vec_len in vec_lens:
            print >> fout,vec_len
            
def statistic_vec_len(input_file):
    vec_lens=[]
    with open(input_file,'r') as fin:        
        for line in fin:
            vec_lens.append(int(line.strip()))
    cnt=Counter(vec_lens)
    cnt=cnt.iteritems()
    result=sorted(cnt,key=lambda x:x[0])    
    x,y=[],[]
    for item in result:
        x.append(item[0])
        y.append(item[1])
    print min(x),max(x),sum(x)/float(len(x))
    plt.figure(1)    
    plt.bar(x,y)
#     plt.plot(x,y,'k',linewidth=1.5)
    plt.show()
    
# get_vec_len(news_file,veclen_file)
statistic_vec_len(veclen_file)
        