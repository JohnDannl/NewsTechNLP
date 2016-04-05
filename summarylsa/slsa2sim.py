#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
import logging
from Crypto.Util.RFC1751 import wordlist
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import news_file,summary_file,dic_file,tfidf_md_file,lsa_mm_file,lsa_md_file,index_file,index_prefix
import time
import jieba
import copy
from common.punckit import delpunc

dictionary = corpora.Dictionary.load(dic_file)
tfidf = models.TfidfModel.load(tfidf_md_file) # step 1 -- initialize a model
lsi=models.LsiModel.load(lsa_md_file)
corpus_lsi= corpora.MmCorpus(lsa_mm_file)
index=similarities.Similarity.load(index_file)

def getSimNews(lineno):
    #vec_tfidf=tfidf[dictionary.doc2bow(wordList)]
    #vec_lsi=lsi[vec_tfidf]
    vec_lsi=corpus_lsi[lineno]
    return index[vec_lsi]

def printSimNews(lineno):
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_lsi[lineno]]:
        print sim,corpus[snum],

def printSimSummary(lineno):    
    corpus=list(open(summary_file,'r'))
    for snum,sim in getSimNews(lineno):
        print sim,corpus[snum],

if __name__=='__main__':
    oldtime=time.time()
    lineno=1766
    printSimNews(lineno)
#     print index[corpus_lsi[0]]
#     newStr='最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'
#     wordList=jieba.cut(delpunc(newStr.lower()));    
#     printSimSummary(lineno)
    print 'time cost:%s' % str(time.time()-oldtime)


