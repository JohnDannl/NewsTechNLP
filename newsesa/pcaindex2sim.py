#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-3-22

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,word2docp_mm_file,word2docp2_mm_file,tfidf_md_file,news_file,index_file,esa_pca_md_file

import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time

dictionary = corpora.Dictionary.load(dict_file)
# print corpus # MmCorpus(3026 documents, 8950 features, 22702 non-zero entries)
tfidf=models.TfidfModel.load(tfidf_md_file)
# word2doc_mat=corpora.MmCorpus(word2docp_mm_file)    # `mm` document stream now has random access
word2doc_mat=corpora.MmCorpus(word2docp2_mm_file)    # for the first-order model
index = similarities.Similarity.load(index_file)
esa_pca=models.LsiModel.load(esa_pca_md_file)
# index = similarities.Similarity.load(part_index_file)

def _get_concept_vec_prune(wordList,prune_at=0.2):
    dic_tfidf={}
    vec_bow = dictionary.doc2bow(wordList)
    if not vec_bow:
        return []
    vec_tfidf=tfidf[vec_bow]
#     for wordid,tfidf_v in vec_bow:
    for wordid,tfidf_v in vec_tfidf:    
        for docid,weight in word2doc_mat[wordid]:
            value=dic_tfidf.get(docid,0)
            value+=tfidf_v*weight
            dic_tfidf[docid]=value
    #print 'tfidf:',vec_tfidf
    #print 'bow:',vec_bow
    if not dic_tfidf.values():        
        print 'Document not recruited:',' '.join(wordList)
    limit_low=prune_at*max(dic_tfidf.iteritems(),key=lambda i:i[1])[1]
    concept_vec=[]
    for item in dic_tfidf.iteritems():
        if item[1]>=limit_low:
            concept_vec.append(item)
    return sorted(concept_vec)    

oldtime=time.time()
rows=tablemerge.getTopRecords(dbconfig.mergetable, 10)
title=rows[3][2]
doc=delpunc(' '.join(jieba.cut(title)).lower())
vec_tfidf = _get_concept_vec_prune(doc.split())# convert the query to concept space
vec_pca=esa_pca[vec_tfidf]
# print vec_pca
sims = index[vec_pca] # perform a similarity query against the corpus
# print sims # print (document_number, document_similarity) 2-tuples

print doc
doc_list=list(open(news_file))
for sim in sims:
    print sim[1],' '.join(doc_list[sim[0]].strip().split()[1:])

print 'time cost:%s' % str(time.time()-oldtime)