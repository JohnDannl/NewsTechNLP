#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import summary_file,dict_file,tfidf_md_file,lsa_mm_file,lsa_md_file,index_file,index_prefix
import time
oldtime=time.time()

dictionary = corpora.Dictionary.load(dict_file)
class MyCorpus(object):
    def __iter__(self):
        for line in open(summary_file):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split()[1:])
  
corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!

def statistic_vacancy():
    for line in open(summary_file):
        if len(dictionary.doc2bow(line.split()[1:]))==0:
            print line

########## check if there is empty vector ###########
# for vector in corpus_memory_friendly: # load one vector into memory at a time    
#     print vector
#     for item in vector:
#         print dictionary.get(item[0]),
#         print dictionary.id2token[item[0]],

# statistic_vacancy()

tfidf=models.TfidfModel.load(tfidf_md_file)
corpus_tfidf=tfidf[corpus_memory_friendly]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100) # initialize an LSI transformation
lsi.save(lsa_md_file)
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
# lsi=models.LsiModel.load(lsa_md_file)
# corpus_lsi=lsi[tfidf[corpus_memory_friendly]]
corpora.MmCorpus.serialize(lsa_mm_file, corpus_lsi) # store to disk, for later use

# corpus_lsi = corpora.MmCorpus(corpus_lsi_file)
# lsi.print_topics(2) # see what these two latent dimensions stand for
# print corpus_lsi[0]
# count=0
# for doc in corpus_memory_friendly: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#     count+=1
#     if count>10:
#         break
#     print count,doc
#     print count,tfidf[doc]    

# lsi.save(lsi_file) # same for tfidf, lda, ...
# lsi = models.LsiModel.load('./tmp/model.lsi')

print 'time cost:%s' % str(time.time()-oldtime)