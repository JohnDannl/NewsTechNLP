#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-8-26

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import news_file,dic_file,tfidf_md_file,corpus_lda_file,lda_md_file
import time
oldtime=time.time()

dictionary = corpora.Dictionary.load(dic_file)
class MyCorpus(object):
    def __iter__(self):
        for line in open(news_file):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split()[1:])
  
corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!

def statistic_vacancy():
    for line in open(news_file):
        if len(dictionary.doc2bow(line.split()[1:]))==0:
            print line

########## check if there is empty vector ###########
# for vector in corpus_memory_friendly: # load one vector into memory at a time    
#     print vector
#     for item in vector:
#         print dictionary.get(item[0]),
#         print dictionary.id2token[item[0]],

# statistic_vacancy()

# lda=models.LdaModel(corpus_memory_friendly,num_topics=100,id2word=dictionary,chunksize=10000, passes=1, update_every=1)# initialize an LSI transformation
lda=models.LdaModel.load(lda_md_file)
corpus_lda=lda[corpus_memory_friendly]
corpora.MmCorpus.serialize(corpus_lda_file, corpus_lda) # store to disk, for later use

# lda=models.LdaModel.load(lda_md_file)
# corpus_lda = corpora.MmCorpus(corpus_lda_file)
# lda.print_topics(2) # see what these two latent dimensions stand for
# print corpus_lda[0]

# print sum(x for i,x in corpus_lda[0])

# count=0
# for doc in corpus_lda: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#     count+=1
#     if count>10:
#         break
#     print count,doc
    
# lda.save(lda_md_file) # same for tfidf, lda, ...
# lda = models.LsiModel.load('./tmp/model.lsi')

print 'time cost:%.2f' % (time.time()-oldtime,)