#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-12

@author: dannl
'''
from glove import Glove
from glove import Corpus
import time

cooc_file='/home/dannl/tmp/newstech/glove/word.cooc'
model_file='/home/dannl/tmp/newstech/glove/glove.model'

oldtime=time.time()
# get a cooccurrence matrix
corpus_cooc = Corpus.load(cooc_file)

# get a model
glove = Glove(no_components=100, learning_rate=0.05)
glove.fit(corpus_cooc.matrix, epochs=5,no_threads=4, verbose=True)
glove.add_dictionary(corpus_cooc.dictionary)
glove.save(model_file)

# count=0
# for word,wid in corpus_cooc.dictionary.items():
#     count+=1
#     if count>100:
#         break
#     print word,wid
    
print('Dict size: %s' % len(corpus_cooc.dictionary))
print('Collocations: %s' % corpus_cooc.matrix.nnz)

print 'time cost:%.2f'%(time.time()-oldtime)
