#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import news_file,dic_file,tfidf_md_file,lsa_mm_file,lsa_md_file,index_file,index_prefix
import time
import jieba
import copy
from common.punckit import delpunc
from six import iteritems
from numpy.linalg import norm
import numpy as np

dictionary = corpora.Dictionary.load(dic_file)
tfidf = models.TfidfModel.load(tfidf_md_file) # step 1 -- initialize a model
lsi=models.LsiModel.load(lsa_md_file)
corpus_lsi= corpora.MmCorpus(lsa_mm_file)
index=similarities.Similarity.load(index_file)

def getSimNews(wordList):
    vec_tfidf=tfidf[dictionary.doc2bow(wordList)]
    vec_lsi=lsi[vec_tfidf]
    return index[vec_lsi]

def printSimNews(num):
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_lsi[num]]:
        print sim,corpus[snum],

def printSimNewsByStr(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],

def getSimofNews(wordList1,wordList2):    
    vec_tfidf1=tfidf[dictionary.doc2bow(wordList1)]
    vec_lsi1=lsi[vec_tfidf1]
    vec_tfidf2=tfidf[dictionary.doc2bow(wordList2)]
    vec_lsi2=lsi[vec_tfidf2]
    if len(vec_lsi1)>len(vec_lsi2):
        tmp=vec_lsi1
        vec_lsi1=vec_lsi2
        vec_lsi2=tmp
    if len(vec_lsi1)!=len(vec_lsi2) and len(vec_lsi1)==0:
        return 0        
    dic_vec2={}
    for _id,value in vec_lsi2:
        dic_vec2[_id]=value
    dot_product=0
    for _id,value in vec_lsi1:
        if dic_vec2.has_key(_id):
            dot_product+=dic_vec2[_id]*value            
    vec1=np.array([i[1] for i in vec_lsi1])
    vec2=np.array([i[1] for i in vec_lsi2])
    return dot_product/(norm(vec1)*norm(vec2))
    
if __name__=='__main__':
    oldtime=time.time()
#     printSimNews(28)
#     print index[corpus_lsi[0]]
    news1='这次 是 真的 日媒 称鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
    news2='一波三折 鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
#     wordList=jieba.cut(delpunc(newStr.lower()));    
    printSimNewsByStr(news1)   
#     for i in xrange(5000): 
#         getSimofNews(news1,news2)    
    print getSimofNews(news1,news2)    
    print 'time cost:%s' % str(time.time()-oldtime)


