#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-3-16

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models
from config import dic_file,esa_mm_file,tfidf_md_file,esa_pca_mm_file,esa_pca_md_file
import time
oldtime=time.time()

dictionary = corpora.Dictionary.load(dic_file)
corpus_esa = corpora.MmCorpus(esa_mm_file)
# tfidf =models.TfidfModel.load(tfidf_md_file)
# corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_esa, num_topics=100) # initialize an LSI transformation
lsi.save(esa_pca_md_file) # same for tfidf, lda, ...
# lsi = models.LsiModel.load('./tmp/model.lsi')
# lsi.print_topics(2) # see what these two latent dimensions stand for

corpus_lsi = lsi[corpus_esa] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
corpora.MmCorpus.serialize(esa_pca_mm_file,corpus_lsi)
# for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#     print doc
