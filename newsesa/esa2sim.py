#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-1-20

@author: JohnDannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
from gensim import corpora,models,similarities
from config import dict_file,word2docp_mm_file,tfidf_md_file,news_file,full_index_file,\
esa_mm_file

import jieba
from database import tablemerge,dbconfig
from common.punckit import delpunc
import time

dictionary = corpora.Dictionary.load(dict_file)
# print corpus # MmCorpus(3026 documents, 8950 features, 22702 non-zero entries)
tfidf=models.TfidfModel.load(tfidf_md_file)
word2doc_mat=corpora.MmCorpus(word2docp_mm_file)    # `mm` document stream now has random access
# word2doc_mat=corpora.MmCorpus(word2docp2_mm_file)    # for the first-order model
index = similarities.Similarity.load(full_index_file)

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
    return list(dic_tfidf.iteritems())

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

corpus_esa=corpora.MmCorpus(esa_mm_file)

def getSimNews(wordList):
    vec_esa=_get_concept_vec(wordList)
#     vec_esa=_get_concept_vec_prune(wordList)
#     vec_esa=_get_concept_vec_slope(wordList)
    return index[vec_esa]

def printSimNews(num):
    corpus=list(open(news_file,'r'))
    for snum,sim in index[corpus_esa[num]]:
        print sim,corpus[snum],

def printSimNewsByStr(wordList):    
    corpus=list(open(news_file,'r'))
    for snum,sim in getSimNews(wordList):
        print sim,corpus[snum],
        
def getSimNewsId():
    news_rep_pre_file='/home/dannl/tmp/newstech/db1/title_rep'
    sim_mtid_file='/home/dannl/tmp/newstech/esa_sw/sim_mtid'
    corpus=list(open(news_file,'r'))
    rep_title=open(news_rep_pre_file,'r')
    fout=open(sim_mtid_file,'w')
    for line in rep_title:
        lineno=int(line.split()[0])-1
        for snum,sim in index[corpus_esa[lineno]]:
            print >> fout,corpus[snum].split()[0],
        print >>fout  
        
if __name__=='__main__':    
    oldtime=time.time()
#     printSimNews(28)
    newStr='最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'
    wordList=delpunc(' '.join(jieba.cut(newStr.lower()))).split();    
    printSimNewsByStr(wordList)
#     wordList='揭秘 王卫 顺丰 快递 员 为啥 拼命 给 他 打天下'.decode('utf-8').split()
#     for word in wordList:
#         print word,dictionary.token2id[word],len(word2doc_mat[dictionary.token2id[word]])
    getSimNewsId()
    print 'time cost:%s' % str(time.time()-oldtime)