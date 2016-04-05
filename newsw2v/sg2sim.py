#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-20

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from gensim.models.word2vec import Word2Vec
from config import sg_md_file,news_file,sg_index_file,sg_mm_file
import scipy
import numpy as np
import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time

model = Word2Vec.load(sg_md_file)
model.init_sims(replace=True)   # To save memory
index = similarities.Similarity.load(sg_index_file)

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

# rows=tablemerge.getTopRecords(dbconfig.mergetable, 10)
# title=rows[3][2]
# doc=delpunc(' '.join(jieba.cut(title)).lower())
# vec_concept = _get_concept_vec_prune(doc.split())# convert the query to concept space
# print vec_concept
# sims = index[vec_concept] # perform a similarity query against the corpus
# print sims # print (document_number, document_similarity) 2-tuples
# print doc
# doc_list=list(open(news_file))
# for sim in sims:
#     print sim[1],' '.join(doc_list[sim[0]].strip().split()[1:])

corpus_w2v=corpora.MmCorpus(sg_mm_file)

def getSimNews(wordList):
    vec_w2v=_get_concept_vec(wordList)
    return index[vec_w2v]

def printSimNews(num):
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
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
    
          
if __name__=='__main__':
    oldtime=time.time()
    wl1='这次 是 真的 日媒 称鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
    wl2='一波三折 鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
#     wordList=delpunc(' '.join(jieba.cut(wl1.lower()))).split()# make sure is a utf-8 str  
    printSimNewsByWL(wl1)
    print getSimofNews(wl1,wl2)
    print 'time cost:%s' % str(time.time()-oldtime)