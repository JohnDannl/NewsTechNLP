#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-3-22

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,esa_pca_mm_file,index_prefix,index_file
import time

oldtime=time.time()
dictionary = corpora.Dictionary.load(dict_file)
corpus=corpora.MmCorpus(esa_pca_mm_file) # now corpus has random access
index=similarities.Similarity(index_prefix,corpus,num_features=dictionary.num_docs,num_best=10)
index.save(index_file)

print 'time cost:%s' % str(time.time()-oldtime)