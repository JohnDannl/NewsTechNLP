#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-12-28

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from gensim.models.word2vec import Word2Vec
from config import w2v_mm_file,w2v_md_file,news_file
import time
import scipy
import numpy as np
oldtime=time.time()

model = Word2Vec.load(w2v_md_file)
model.init_sims(replace=True)

def statistic_vacancy():
    for line in open(news_file):
        empty=True
        for word in line.split()[1:]:
            if model.vocab.has_key(word):
                empty=False
            if not empty:
                break
        if empty:
            print line
   
def _get_concept_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.layer1_size)
    for word in wordList:
        # make sure the word2vec model contain key 'word'
        if model.vocab.has_key(word):
            total_vec+=model[word]
    return [(i,total_vec[i]) for i in xrange(model.layer1_size) if total_vec[i] !=0]
    

class MyCorpus(object):
    def __init__(self,file_name):
        self.__file_name=file_name
    def __iter__(self):
        for line in open(self.__file_name):
            line=line.split()     
#             yield _get_concept_vec_slope(line[1:])
            yield _get_concept_vec(line[1:])

# statistic_vacancy()        
corpora.MmCorpus.serialize(w2v_mm_file, MyCorpus(news_file)) # store to disk, for later use
print _get_concept_vec(['中国'])
print np.linalg.norm(model['中国'])

print 'time cost:%s' % str(time.time()-oldtime)