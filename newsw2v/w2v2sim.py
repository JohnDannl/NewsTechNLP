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
from config import w2v_md_file,news_file,index_file,w2v_mm_file
import scipy

import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time

model = Word2Vec.load(w2v_md_file)
model.init_sims(replace=True)   # To save memory
index = similarities.Similarity.load(index_file)

def _get_concept_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.layer1_size)
    wordStr=' '.join(wordList)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wordList=wordStr.encode('utf-8').split()
    for word in wordList:
        # make sure the word2vec model contain key 'word'        
        if model.vocab.has_key(word):
            total_vec+=model[word]
    return [(i,total_vec[i]) for i in xrange(model.layer1_size) if total_vec[i] !=0]

# rows=tablemerge.getTopRecords(dbconfig.mergetable, 10)
# title=rows[3][2]
# doc=delpunc(' '.join(jieba.cut(title)).lower())
# vec_concept = _get_concept_vec_prune(doc.split())# convert the query to concept space
# print vec_concept
# sims = index[vec_concept] # perform a similarity query against the corpus
# print sims # print (document_number, document_similarity) 2-tuples
# print doc
# doc_list=list(open(news_file))
# for sim in sims:
#     print sim[1],' '.join(doc_list[sim[0]].strip().split()[1:])

corpus_w2v=corpora.MmCorpus(w2v_mm_file)

def getSimNews(wordList):
    vec_w2v=_get_concept_vec(wordList)
    return index[vec_w2v]

def printSimNews(num):
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_w2v[num]]:
        print sim,corpus[snum],

def printSimNewsByWL(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],

def getSimNewsId():
    news_rep_pre_file='/home/dannl/tmp/newstech/db1/title_rep'
    sim_mtid_file='/home/dannl/tmp/newstech/w2v/sim_mtid'
    corpus=list(open(news_file,'r'))
    rep_title=open(news_rep_pre_file,'r')
    fout=open(sim_mtid_file,'w')
    for line in rep_title:
        lineno=int(line.split()[0])-1
        for snum,sim in index[corpus_w2v[lineno]][:10]:
            print >> fout,corpus[snum].split()[0],
        print >>fout  
          
if __name__=='__main__':
    oldtime=time.time()
#     printSimNews(28)
    newStr='最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'
    wordList=delpunc(' '.join(jieba.cut(newStr.lower()))).split()# make sure is a utf-8 str  
    printSimNewsByWL(wordList)
    getSimNewsId()
    print 'time cost:%s' % str(time.time()-oldtime)