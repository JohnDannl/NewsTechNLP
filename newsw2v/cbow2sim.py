#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-17

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from gensim.models.word2vec import Word2Vec
from config import cbow_md_file,news_file,cbow_index_file,cbow_mm_file
import scipy
import numpy as np
import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time

model = Word2Vec.load(cbow_md_file)
model.init_sims(replace=True)   # To save memory

def _get_concept_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.layer1_size)
    wordStr=' '.join(wordList)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wordList=wordStr.encode('utf-8').split()
    for word in wordList:
        # make sure the word2vec model contain key 'word'        
        if model.vocab.has_key(word):
            total_vec+=model[word]
    return [(i,total_vec[i]) for i in xrange(model.layer1_size) if total_vec[i] !=0]

def _get_wl_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.layer1_size)
    wordStr=' '.join(wordList)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wordList=wordStr.encode('utf-8').split()
    for word in wordList:
        # make sure the word2vec model contain key 'word'        
        if model.vocab.has_key(word):
            total_vec+=model[word]
    return total_vec

def getSimNews(wordList):
    index = similarities.Similarity.load(cbow_index_file)
    vec_w2v=_get_concept_vec(wordList)
    return index[vec_w2v]

def printSimNews(num):
    index = similarities.Similarity.load(cbow_index_file)
    corpus_w2v=corpora.MmCorpus(cbow_mm_file)
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_w2v[num]]:
        print sim,corpus[snum],

def printSimNewsByWL(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],

def getSimofNews(wordList1,wordList2):    
    vec1=_get_wl_vec(wordList1)
    vec2=_get_wl_vec(wordList2)
    nv1=np.linalg.norm(vec1)
    nv2=np.linalg.norm(vec2)
    if nv1!=0 and nv2!=0:
        return np.dot(vec1,vec2)/(nv1*nv2)
    else:
        return 0
          
if __name__=='__main__':
    oldtime=time.time()
    news1='这次 是 真的 日媒 称鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
    news2='一波三折 鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
    printSimNewsByWL(news1)
    print getSimofNews(news1,news2)
    print 'time cost:%s' % str(time.time()-oldtime)