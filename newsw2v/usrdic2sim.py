#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-9-5

@author: dannl
'''
from config import news_test_file,news_file,sim_news_test_file,sim_news_file,news_rep_file,\
                    news_rep_test_file
from newsw2v import w2vword2sim
import jieba
from common.punckit import delpunc
import numpy as np

def getSimNewsCorpus(news_file,sim_news_file):
    corpus=list(open(news_file,'r'))
    corpus_len=len(corpus)
    fout=open(sim_news_file,'w')
    sim_arr=np.zeros((corpus_len,corpus_len))
    for i in xrange(len(corpus)):           
        for j in xrange(i+1,len(corpus)):            
            wl1=corpus[i].split()[1:]   # note this wl1 will be deleted in the getSimofWordListPairMod(wl1,wl2)
            wl2=corpus[j].split()[1:]
            sim=w2vword2sim.getSimofWordListPairMod(wl1, wl2, False)
            sim_arr[i][j]=sim_arr[j][i]=sim
        sim_list=[(j,sim_arr[i][j]) for j in xrange(corpus_len) ]
        sim_list=sorted(sim_list,key=lambda x:x[1],reverse=True)
        print >> fout,corpus[i].strip()
        for num,sim in sim_list[:10]:
            print >> fout,'    %.4f %s'%(sim,corpus[num].strip())
            
def getSimNewsRep(rep_file,news_file,sim_news_file):
    corpus=list(open(news_file,'r'))
    corpus_len=len(corpus)
    fout=open(sim_news_file,'w')
    sim_arr=np.zeros((corpus_len,corpus_len))
    for i in xrange(len(corpus)):           
        for j in xrange(i+1,len(corpus)):            
            wl1=corpus[i].split()[1:]   # note this wl1 will be deleted in the getSimofWordListPairMod(wl1,wl2)
            wl2=corpus[j].split()[1:]
            sim=w2vword2sim.getSimofWordListPairMod(wl1, wl2, False)
            sim_arr[i][j]=sim_arr[j][i]=sim
        sim_list=[(j,sim_arr[i][j]) for j in xrange(corpus_len) ]
        sim_list=sorted(sim_list,key=lambda x:x[1],reverse=True)
        print >> fout,corpus[i].strip()
        for num,sim in sim_list[:10]:
            print >> fout,'    %.4f %s'%(sim,corpus[num].strip())
            
getSimNewsCorpus(news_test_file,sim_news_test_file)