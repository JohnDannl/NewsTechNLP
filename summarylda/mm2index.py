#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-8-26

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import news_file,summary_file,dict_file,tfidf_md_file,corpus_lda_file,lda_md_file,index_file,index_prefix
import time
oldtime=time.time()

corpus_lda = corpora.MmCorpus(corpus_lda_file)
lda = models.LdaModel.load(lda_md_file)

index=similarities.Similarity(index_prefix,corpus_lda,num_features=lda.num_topics,num_best=10)
index.save(index_file)
print 'time cost:%s' % str(time.time()-oldtime)