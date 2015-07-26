#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-20

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,esa_mm_file,full_index_prefix,full_index_file
import time

oldtime=time.time()
dictionary = corpora.Dictionary.load(dict_file)
corpus=corpora.MmCorpus(esa_mm_file) # now corpus has random access
index=similarities.Similarity(full_index_prefix,corpus,num_features=dictionary.num_docs,num_best=10)
index.save(full_index_file)

# corpus1=corpora.MmCorpus(part1_mm_file) # now corpus has random access
# index=similarities.Similarity(part_index_path,corpus1,num_features=dictionary.num_docs,num_best=10)
# index.save(part_index_file)

# corpus2=corpora.MmCorpus(part2_mm_file) # now corpus has random access
# index = similarities.Similarity.load(part_index_file)
# index.add_documents(corpus2)
# index.save(part_index_file)

print 'time cost:%s' % str(time.time()-oldtime)