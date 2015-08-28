#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-8-27

@author: dannl
'''
from gensim.models.word2vec import Word2Vec

import logging
from numpy.linalg.linalg import norm
import numpy as np
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
import scipy
import jieba
import time
from common.punckit import delpunc
from config import news_file

w2v_wiki='/home/dannl/tmp/wiki/w2v/w2v.md'
w2v_news='/home/dannl/tmp/news/w2v/w2v.md'
wiki_miss_file='/home/dannl/tmp/newstech/vocab/wiki_miss.txt'
news_miss_file='/home/dannl/tmp/newstech/vocab/news_miss.txt'
common_miss_file='/home/dannl/tmp/newstech/vocab/common_miss.txt'

def statistic_vocabulary(model,out_file): 
    set_miss=set([])
    for line in open(news_file,'r'):
        line=line.split()[1:]  
        for word in line: 
            if word not in model.vocab:
                set_miss.add(word)
    with open(out_file,'w') as fout:
        for word in set_miss:
            fout.write(word+'\n')
    print 'total miss:%d'%(len(set_miss))
    return set_miss

if __name__=='__main__':
    oldtime=time.time()
    model = Word2Vec.load(w2v_wiki)
    model.init_sims(replace=True) # To load a static model to save memory
    wiki_miss=statistic_vocabulary(model,wiki_miss_file)
    model = Word2Vec.load(w2v_news)
    model.init_sims(replace=True) # To load a static model to save memory
    news_miss=statistic_vocabulary(model,news_miss_file)
#     set_miss=set([])
#     for word in news_miss:
#         if word in wiki_miss:
#             set_miss.add(word)
#     with open(common_miss_file,'w') as fout:
#         for word in set_miss:
#             print >> fout,word
#     print 'common miss:%d'%(len(set_miss))
    print 'time cost:%.2f'%(time.time()-oldtime,)
    
    