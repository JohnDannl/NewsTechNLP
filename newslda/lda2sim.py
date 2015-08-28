#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-8-26

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import news_file,dict_file,tfidf_md_file,corpus_lda_file,lda_md_file,index_file,index_prefix
import time
import jieba
import copy
from common.punckit import delpunc

dictionary = corpora.Dictionary.load(dict_file)
lda=models.LdaModel.load(lda_md_file)
corpus_lda= corpora.MmCorpus(corpus_lda_file)
index=similarities.Similarity.load(index_file)

def getSimNews(wordList):
    vec_bow=dictionary.doc2bow(wordList)
    vec_lda=lda[vec_bow]
    return index[vec_lda]

def printSimNews(num):
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_lda[num]]:
        print sim,corpus[snum],

def printSimNewsByStr(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],

if __name__=='__main__':
    oldtime=time.time()
    printSimNews(27)
#     print index[corpus_lsi[0]]
#     newStr='最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'
#     wordList=jieba.cut(delpunc(newStr.lower()));    
#     printSimNewsByStr(wordList)
    print 'time cost:%s' % str(time.time()-oldtime)
