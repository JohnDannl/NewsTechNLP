#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-9-5

@author: dannl
'''
import sys
sys.path.append('..')
sys.path.append('../common')
from config import news_test_file,news_file,sim_news_file,news_rep_file,news_rep_test_pre_file,\
                   news_rep_pre_file,rep_id_file,rep_id_file,rep_sim_file,err_sim_file
import w2vword2sim
import jieba
from common.punckit import delpunc
import numpy as np
import time
oldtime=time.time()

def getSimNewsCorpus(news_file,sim_news_file):
    corpus=list(open(news_file,'r'))
    corpus_len=len(corpus)
    fout=open(sim_news_file,'w')
    sim_arr=np.zeros((corpus_len,corpus_len))
    for i in xrange(len(corpus)):    
        wl1=corpus[i].split()[1:]        
        for j in xrange(i+1,len(corpus)):            
            wl2=corpus[j].split()[1:]
            sim=w2vword2sim.getSimofWordListPairMod(wl1, wl2, False,False)
            sim_arr[i][j]=sim_arr[j][i]=sim
        sim_list=[(j,sim_arr[i][j]) for j in xrange(corpus_len) ]
        sim_list=sorted(sim_list,key=lambda x:x[1],reverse=True)
        print >> fout,corpus[i].strip()
        for num,sim in sim_list[:10]:
            print >> fout,'    %.4f %s'%(sim,corpus[num].strip())

def dealRepFile(rep_pre_file,rep_file):
    with open(rep_file,'w') as fout:
        for line in open(rep_pre_file):
            line= line.split()
            title=delpunc(' '.join(jieba.cut(' '.join(line[4:]).lower()))).encode('utf-8')
            line='%s %s'%(line[1],title)
            print >> fout,line
def getSimNewsRep(rep_file,news_file,sim_news_file):
    corpus=list(open(news_file,'r'))
    corpus_len=len(corpus)
    rep=list(open(rep_file,'r'))
    rep_len=len(rep)
    fout=open(sim_news_file,'w')
    for i in xrange(rep_len):           
        sim_list=[]
        line=rep[i].split()
        mtid,wl1=line[0],line[1:]   # note this wl1 will be deleted in the getSimofWordListPairMod(wl1,wl2)
        for j in xrange(corpus_len):            
            wl2=corpus[j].split()[1:]
            sim=w2vword2sim.getSimofWordListPairMod(wl1, wl2, modify=False,usrDict=True)
            sim_list.append((j,sim))
        sim_list=sorted(sim_list,key=lambda x:x[1],reverse=True)
        print >> fout,rep[i].strip()
        for num,sim in sim_list[:11]:
            if corpus[num].split()[0]==mtid:   #skip the news itself
                continue
            print >> fout,'    %.4f %s'%(sim,corpus[num].strip())

def getSimErrofRepNews(rep_file,rep_id_file,rep_sim_file,err_sim_file):
    rep_corpus={}
    fout=open(rep_sim_file,'w')
    ferr=open(err_sim_file,'w')
    for line in open(rep_file):
        line=line.split()
        rep_corpus[line[0]]=line[1:]
    for line in open(rep_id_file):
        line=line.split()
        for mtid_i in line:
            print >> fout,'%s %s'%(mtid_i,' '.join(rep_corpus[mtid_i]))
            for mtid_j in line:
                if mtid_i==mtid_j:  #skip itself
                    continue
                sim=w2vword2sim.getSimofWordListPairMod(rep_corpus[mtid_i], rep_corpus[mtid_j], modify=False,usrDict=True)
                print >> fout,'    %.4f %s %s'%(sim,mtid_j,' '.join(rep_corpus[mtid_j]))
                if sim<0.78:
                    print >> ferr,'%s %s'%(mtid_i,' '.join(rep_corpus[mtid_i]))
                    print >> ferr,'%s %s'%(mtid_j,' '.join(rep_corpus[mtid_j]))
                    print >> ferr,sim

def trainSimofUsrDict(err_sim_file):
    err_corpus=open(err_sim_file,'r')
    line1=err_corpus.readline()
    while line1:
        line2=err_corpus.readline()
        err_corpus.readline()   # skip the empty line
        line1=line1.split()[1:]
        line2=line2.split()[1:]
        w2vword2sim.getSimofWordListPairMod(line1,line2,modify=True,usrDict=True)
        line1=err_corpus.readline()
    w2vword2sim.word_sim_dic.save_dict()
        
# getSimNewsCorpus(news_test_file,sim_news_file)
# dealRepFile(news_rep_pre_file,news_rep_file)

# getSimNewsRep(news_rep_file,news_file,sim_news_file)
getSimErrofRepNews(news_rep_file,rep_id_file,rep_sim_file,err_sim_file)
# trainSimofUsrDict(err_sim_file)
print 'time cost:%.4f'%(time.time()-oldtime)