#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2015-1-19

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,tfidf_md_file,word2docp_mm_file,word2docp2_mm_file,news_file,esa_mm_file
from six import iteritems
from numpy.linalg import norm
import time
oldtime=time.time()

dictionary = corpora.Dictionary.load(dict_file)
tfidf =models.TfidfModel.load(tfidf_md_file)
word2doc_mat=corpora.MmCorpus(word2docp_mm_file)  
# word2doc_mat=corpora.MmCorpus(word2docp2_mm_file)  

def _get_tfidf_dic(doc):
    dic_tfidf={}
    vec_bow = dictionary.doc2bow(doc.lower().split())
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
        print 'Document not recruited:',doc
    return dic_tfidf

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
    if not dic_tfidf.values():        
        print 'Document not recruited:',' '.join(wordList)    
    return dic_tfidf.iteritems()

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
    if not dic_tfidf.values():        
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

class MyCorpus(object):
    def __init__(self,file_name):
        self.__file_name=file_name
    def __iter__(self):
        for line in open(self.__file_name):
            line=line.split()     
            #yield _get_concept_vec(line[1:])
            yield _get_concept_vec_slope(line[1:])
            #yield _get_concept_vec_prune(line[1:])
        
corpora.MmCorpus.serialize(esa_mm_file, MyCorpus(news_file)) # store to disk, for later use

print 'time cost:%s' % str(time.time()-oldtime)
############# Test accuracy of pruned vectors  ############
# bow='香港  占 中'
# v_all=list(_get_tfidf_dic(bow).iteritems())
# v_sp=_get_concept_vec_slope(bow.split())
# v_pr=_get_concept_vec_prune(bow.split())
# print v_all
# print v_sp
# print v_pr
# w1=sum(i[1] for i in v_all)
# w2=sum(i[1] for i in v_sp)
# w3=sum(i[1] for i in v_pr)
# print len(v_all),w1
# print len(v_sp),w2,w2/w1
# print len(v_pr),w3,w3/w1
    
