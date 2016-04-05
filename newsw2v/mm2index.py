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
from config import cbow_md_file,cbow_mm_file,cbow_index_prefix,cbow_index_file
import time

oldtime=time.time()
model = Word2Vec.load(cbow_md_file)
model.init_sims(replace=True)
corpus=corpora.MmCorpus(cbow_mm_file) # now corpus has random access
index=similarities.Similarity(cbow_index_prefix,corpus,num_features=model.layer1_size,num_best=10)
index.save(cbow_index_file)

# corpus1=corpora.MmCorpus(part1_mm_file) # now corpus has random access
# index=similarities.Similarity(part_index_path,corpus1,num_features=dictionary.num_docs,num_best=10)
# index.save(part_index_file)

# corpus2=corpora.MmCorpus(part2_mm_file) # now corpus has random access
# index = similarities.Similarity.load(part_index_file)
# index.add_documents(corpus2)
# index.save(part_index_file)

print 'time cost:%s' % str(time.time()-oldtime)