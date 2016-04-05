#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-12

@author: dannl
'''
from glove import Glove
from glove import Corpus
from gensim import corpora
import time

dic_file=r'/home/dannl/tmp/newstech/glove/news.dic'
corpus_file='/home/dannl/tmp/newstech/news.txt'
cooc_file='/home/dannl/tmp/newstech/glove/word.cooc'

def read_corpus(filename):
    with open(filename, 'r') as datafile:
        for line in datafile:
            yield line.split()[1:]

# get a cooccurrence matrix
oldtime=time.time()
dictionary = corpora.Dictionary.load(dic_file)

# corpus_cooc = Corpus()
# corpus_cooc.fit(read_corpus(corpus_file), window=10)

corpus_cooc = Corpus(dictionary=dictionary.token2id)
corpus_cooc.fit(read_corpus(corpus_file), window=10,ignore_missing=True)
corpus_cooc.save(cooc_file)

print('Dict size: %s' % len(corpus_cooc.dictionary))
print('Collocations: %s' % corpus_cooc.matrix.nnz)

print 'time cost:%.2f'%(time.time()-oldtime,)
