#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-21

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import summary_file,dict_file,tfidf_md_file,lsa_mm_file,lsa_md_file,index_file,index_prefix
import time
oldtime=time.time()

corpus_lsi = corpora.MmCorpus(lsa_mm_file)
lsi = models.LsiModel.load(lsa_md_file)

index=similarities.Similarity(index_prefix,corpus_lsi,num_features=lsi.num_topics,num_best=20)
index.save(index_file)
print 'time cost:%s' % str(time.time()-oldtime)