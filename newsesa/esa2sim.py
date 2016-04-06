#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-20

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dic_file,word2docp_mm_file,tfidf_md_file,news_file,full_index_file,\
esa_mm_file

import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time
from six import iteritems
from numpy.linalg import norm
import numpy as np

dictionary = corpora.Dictionary.load(dic_file)
# print corpus # MmCorpus(3026 documents, 8950 features, 22702 non-zero entries)
tfidf=models.TfidfModel.load(tfidf_md_file)
word2doc_mat=corpora.MmCorpus(word2docp_mm_file)    # `mm` document stream now has random access
# word2doc_mat=corpora.MmCorpus(word2docp2_mm_file)    # for the first-order model

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
    if len(dic_tfidf)==0:        
        print 'Document not recruited:',' '.join(wordList)
    limit_low=prune_at*max(dic_tfidf.iteritems(),key=lambda i:i[1])[1]
    concept_vec=[]
    for item in dic_tfidf.iteritems():
        if item[1]>=limit_low:
            concept_vec.append(item)
    return sorted(concept_vec)    

def _get_concept_vec_slope(wordList,slope=0.05):
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
    if len(dic_tfidf)==0:        
        print 'Document not recruited:',' '.join(wordList)        
    pvec=[]
    __window_size=100
    vec=list(dic_tfidf.iteritems())
    if len(vec)>__window_size:                     
        offset=__window_size
        vec= sorted(vec,key=lambda i:i[1],reverse=True)
        #pvec=vec
        gap=slope*vec[0][1]
        while offset<len(vec):
            if (vec[offset-__window_size][1]-vec[offset][1])<gap:
                break
            offset+=1
        pvec=sorted(vec[0:offset])
    else:
        pvec=vec    
    return pvec  

def _get_concept_vec(wordList):
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
    if not len(dic_tfidf):        
        print 'Document not recruited:',' '.join(wordList)    
    return list(dic_tfidf.iteritems())

def _get_dic_vec(wordList):
    dic_tfidf={}
    vec_bow = dictionary.doc2bow(wordList)
    vec_tfidf=tfidf[vec_bow]
#     for wordid,tfidf_v in vec_bow:
    for wordid,tfidf_v in vec_tfidf:    
        for docid,weight in word2doc_mat[wordid]:
            value=dic_tfidf.get(docid,0)
            value+=tfidf_v*weight
            dic_tfidf[docid]=value
    #print 'tfidf:',vec_tfidf
    #print 'bow:',vec_bow
    if len(dic_tfidf)==0:        
        print 'Document not recruited:',' '.join(wordList)
    return dic_tfidf

def _dot_product(dic1,dic2):
    if len(dic1)>len(dic2): # select the shorter one as base
        tmp=dic1
        dic1=dic2
        dic2=tmp 
    dot_product=0
    for docid,value in iteritems(dic1):
        if dic2.has_key(docid):
            dot_product+=value*dic2.get(docid)
    return dot_product

def _sparse_vec_sim(dic1,dic2):
    if dic1.values() and dic2.values():
        return _dot_product(dic1,dic2)/(norm(dic1.values())*norm(dic2.values()))
    else:
        return 0
# rows=tablemerge.getTopRecords(dbconfig.mergetable, 10)
# title=rows[3][2]
# doc=delpunc(' '.join(jieba.cut(title)).lower())
# vec_tfidf = _get_concept_vec_prune(doc.split())# convert the query to concept space
# print vec_tfidf
# sims = index[vec_tfidf] # perform a similarity query against the corpus
# print sims # print (document_number, document_similarity) 2-tuples

# print doc
# doc_list=list(open(news_file))
# for sim in sims:
#     print sim[1],' '.join(doc_list[sim[0]].strip().split()[1:])

def getSimNews(wordList):
    index = similarities.Similarity.load(full_index_file)
#     vec_esa=_get_concept_vec(wordList)
    vec_esa=_get_concept_vec_prune(wordList)
#     vec_esa=_get_concept_vec_slope(wordList)
    return index[vec_esa]

def printSimNews(num):
    index = similarities.Similarity.load(full_index_file)
    corpus_esa=corpora.MmCorpus(esa_mm_file)
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_esa[num]]:
        print sim,corpus[snum],

def printSimNewsByStr(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],

def getSimofNewsPrune(wordList1,wordList2):    
    vec1=_get_concept_vec_prune(wordList1,0.2)
    vec2=_get_concept_vec_prune(wordList2,0.2)
    if len(vec1)>len(vec2):
        tmp=vec1
        vec1=vec2
        vec2=tmp
    if len(vec1)!=len(vec2) and len(vec1)==0:
        return 0        
    dic_vec2={}
    for _id,value in vec2:
        dic_vec2[_id]=value
    dot_product=0
    for _id,value in vec1:
        if dic_vec2.has_key(_id):
            dot_product+=dic_vec2[_id]*value            
    vec1=np.array([i[1] for i in vec1])
    vec2=np.array([i[1] for i in vec2])
    return dot_product/(norm(vec1)*norm(vec2))

def getSimofNews(wordList1,wordList2):    
    dic_v1=_get_dic_vec(wordList1)
    dic_v2=_get_dic_vec(wordList2)
    return _sparse_vec_sim(dic_v1,dic_v2)
    
                
if __name__=='__main__':    
    oldtime=time.time()
#     printSimNews(28)
    news1='在 游戏 开发 上 三大 vr 平台 各自 的 优势 是 什么'.split()
    news2='三大 vr 平台 在 游戏 上 都 做 了 哪些 布局'.split()
#     wordList=delpunc(' '.join(jieba.cut(news1.lower()))).split();    
    printSimNewsByStr(news1)
    print getSimofNewsPrune(news1,news2)
    print 'time cost:%s' % str(time.time()-oldtime)