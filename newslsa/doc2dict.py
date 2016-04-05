#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models,similarities
from config import corpus_file,dic_file,tfidf_md_file
import time

oldtime=time.time()
def getDocuments(file_name):
    for line in open(file_name):
        yield line.split()[1:]
corpus=getDocuments(corpus_file)
# for i in corpus:
#     print ''.join(i)
dictionary = corpora.Dictionary(corpus,prune_at=4000000)# collect statistics about all tokens
ori_len=len(dictionary)

dictionary.filter_extremes(no_below=2, no_above=1.0, keep_n=4000000)# filter out words whose document frequence <no_below and compact
dictionary.save(dic_file)  # store the dictionary, for future reference
# print dictionary.num_docs
# print dictionary.num_nnz
print 'dict keeps %s/%s words'%(len(dictionary),ori_len)

tfidf = models.TfidfModel(corpus,id2word=dictionary,dictionary=dictionary) # step 1 -- initialize a model
tfidf.save(tfidf_md_file)
print 'time cost:%s' % str(time.time()-oldtime)