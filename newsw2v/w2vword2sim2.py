#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-22

@author: dannl
'''
from gensim.models.word2vec import Word2Vec
from gensim import corpora,models,similarities

import logging
from numpy.linalg.linalg import norm
import numpy as np
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
import scipy
import jieba
from common.punckit import delpunc
from config import sg_md_file,news_file,tfidf_md_file,dict_file
import json
import math,copy

model = Word2Vec.load(sg_md_file)
model.init_sims(replace=True) # To load a static model to save memory
tfidf=models.TfidfModel.load(tfidf_md_file)
# model,tfidf=None,None
dictionary=corpora.Dictionary.load(dict_file)

def _get_concept_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.layer1_size)
    for word in wordList:
        # make sure the word2vec model contain key 'word'
        if model.vocab.has_key(word):
            total_vec+=model[word]
    #return [(i,total_vec[i]) for i in xrange(model.layer1_size) if total_vec[i] !=0]
    return total_vec

def getSimofWordListVecSum(wl1,wl2):   
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()  
    vec1=_get_concept_vec(wl1)
    vec2=_get_concept_vec(wl2)
    #print 'ori:',scipy.dot(vec1.T,vec2)
    return scipy.dot(vec1.T,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

def getSimofWords(w1,w2):
    # words must be in utf-8 code
    if isinstance(w1, unicode):
        w1=w1.encode('utf-8')
    if isinstance(w2, unicode):
        w2=w2.encode('utf-8')
    if w1==w2:
        return 1.0    
    if w1 in model.vocab and w2 in model.vocab:
        return model.similarity(w1,w2)    
    return 0.0  # a specified value for any word not in vocab

def getSimofWordListPair(wl1,wl2):
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()  
#     print ' '.join(wl1)
#     print ' '.join(wl2) 
    len1,len2=len(wl1),len(wl2)    
    asim=np.zeros((len1,len2))
    for i in xrange(len1):
        for j in xrange(len2):
            asim[i][j]=getSimofWords(wl1[i], wl2[j]) 
    sim_sum=0.0    
    len_pair=0
    while 0 not in np.shape(asim):
        i,j=np.unravel_index(asim.argmax(), asim.shape)
        if asim[i][j]!=0:
            len_pair+=1
            sim_sum+=asim[i][j]        
#         print asim
#         print asim[i][j],asim.shape,i,j,wl1[i],wl2[j]        
#         del wl1[i],wl2[j]    # this will change the parent wl1's value 
        asim=np.delete(asim, i, 0)
        asim=np.delete(asim, j, 1)
    minlen=len1 if len1<=len2 else len2
    print 'pair:',minlen,len_pair
    if len_pair!=0:
        return sim_sum/len_pair
    else:
        return -1

class Entry(object):
    def __init__(self,w1,w2,sim):
        self.w1=w1
        self.w2=w2
        self.sim=sim
    def __repr__(self):
        return '%s::%s'%(self.w1,self.w2)
    def __eq__(self, other):
        if isinstance(other, Entry):
            return ((self.w1 == other.w1) and (self.w2 == other.w2))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())

def getSimofWordListPairMatch(wordList1,wordList2):
    # two word lists should better be utf-8
    entries=[]
    wordStr=' '.join(wordList1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    else:
        wl1=wordStr.split()
    wordStr=' '.join(wordList2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    else:
        wl2=wordStr.split()
    len1,len2=len(wl1),len(wl2)  
    asim=np.zeros((len1,len2))
    for i in xrange(len1):
        for j in xrange(len2):
            asim[i][j]=getSimofWords(wl1[i], wl2[j]) 
    sim_sum=0.0    
    while 0 not in np.shape(asim):
        i,j=np.unravel_index(asim.argmax(), asim.shape)
        if asim[i][j]!=0:   # ignore the zero item
            sim_sum+=asim[i][j]        
            entries.append(Entry(wl1[i],wl2[j],asim[i][j]))  
        del wl1[i],wl2[j]    # this will change the parent wl1's value 
#         print asim
#         print asim[i][j],asim.shape,i,j,wl1[i],wl2[j]        
        asim=np.delete(asim, i, 0)
        asim=np.delete(asim, j, 1)          
#     for entry in entries:
#         print entry.w1,entry.w2,entry.sim
#     minlen=len1 if len1<=len2 else len2 
#     print 'pair:',minlen,len(entries) 
    if len(entries) !=0:  
        sim_ave=sim_sum/len(entries)    
        return sim_ave
    else:
        return -1

def getSimofWordListTopAve(wl1,wl2):
    # two word lists should better be utf-8
    entries=[]
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    len1,len2=len(wl1),len(wl2)   
    sim_arr=np.zeros((len1,len2))
    sim_sum=0.0       
    for i in xrange(len1):
        sim_max,max_j=0.0,0
        for j in xrange(len2):
            sim_cur=getSimofWords(wl1[i], wl2[j]) 
            sim_arr[i][j]=sim_cur            
            if sim_cur>sim_max:
                sim_max=sim_cur
                max_j=j              
        if sim_max!=0:     
            sim_sum+=sim_max       
            entries.append(Entry(wl1[i],wl2[max_j],sim_max))
    for j in xrange(len2):
        sim_max,max_i=0.0,0
        for i in xrange(len1):
            if sim_arr[i][j]>sim_max:
                sim_max=sim_arr[i][j]
                max_i=i
        if sim_max!=0:
            sim_sum+=sim_max        
            entries.append(Entry(wl1[max_i],wl2[j],sim_max))    
#     for entry in entries:
#         print entry.w1,entry.w2,entry.sim
#     print 'top:',len1+len2,len(entries)
    if len(entries)!=0:
        sim_ave=sim_sum/len(entries)    #sim_sum/(len1+len2)    
        return sim_ave
    else:
        return -1

def getSimofWordListTopWeight(wl1,wl2):
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    tfidf_vec1=tfidf[dictionary.doc2bow(wl1)]
    tfidf_vec2=tfidf[dictionary.doc2bow(wl2)]    
    tfidf_str1,tfidf_str2=[],[]
    for i,w in tfidf_vec1:
        tfidf_str1.append(dictionary[i]+'/'+'%.3f'%w)
    for i,w in tfidf_vec2:
        tfidf_str2.append(dictionary[i]+'/'+'%.3f'%w)
    print 'tfidf1:',','.join(tfidf_str1)
    print 'tfidf2:',','.join(tfidf_str2)  
#     tfidf_sum=0
    sim_sum=0.0       
    for wdi,weight_i in tfidf_vec1:
        sim_max=0.0
        for wdj,weight_j in tfidf_vec2:
            sim_cur=getSimofWords(dictionary[wdi], dictionary[wdj]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=weight_i**2*sim_max   
#         tfidf_sum+=weight_i**2
#     print 'tfidf_sum_1:',tfidf_sum,'sim_sum_1:',sim_sum
#     tfidf_sum=0
#     sim_sum=0
    for wdi,weight_i in tfidf_vec2:
        sim_max=0.0
        for wdj,weight_j in tfidf_vec1:
            sim_cur=getSimofWords(dictionary[wdi], dictionary[wdj]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=weight_i**2*sim_max   
#         tfidf_sum+=weight_i**2
#     print 'tfidf_sum_1:',tfidf_sum,'sim_sum_2:',sim_sum
    return sim_sum/2

def getSimofWordListTopWeight(wl1,wl2):
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    tfidf_vec1=tfidf[dictionary.doc2bow(wl1)]
    tfidf_vec2=tfidf[dictionary.doc2bow(wl2)]    
    tfidf_str1,tfidf_str2=[],[]
    for i,w in tfidf_vec1:
        tfidf_str1.append(dictionary[i]+'/'+'%.3f'%w)
    for i,w in tfidf_vec2:
        tfidf_str2.append(dictionary[i]+'/'+'%.3f'%w)
    print 'tfidf1:',','.join(tfidf_str1)
    print 'tfidf2:',','.join(tfidf_str2)  
#     tfidf_sum=0
    sim_sum=0.0       
    for wdi,weight_i in tfidf_vec1:
        sim_max=0.0
        for wdj,weight_j in tfidf_vec2:
            sim_cur=getSimofWords(dictionary[wdi], dictionary[wdj]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=weight_i**2*sim_max   
#         tfidf_sum+=weight_i**2
#     print 'tfidf_sum_1:',tfidf_sum,'sim_sum_1:',sim_sum
#     tfidf_sum=0
#     sim_sum=0
    for wdi,weight_i in tfidf_vec2:
        sim_max=0.0
        for wdj,weight_j in tfidf_vec1:
            sim_cur=getSimofWords(dictionary[wdi], dictionary[wdj]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=weight_i**2*sim_max   
#         tfidf_sum+=weight_i**2
#     print 'tfidf_sum_1:',tfidf_sum,'sim_sum_2:',sim_sum
    return sim_sum/2

def _getRelativityWordList(wl1,withWeight=False):
    # wl1 should be a list of words encoded in utf-8
    lenw=len(wl1)
    arrsim=np.zeros((lenw,lenw))
    for i in xrange(lenw):
        arrsim[i][i]=0
        for j in xrange(i+1,lenw):
            arrsim[i][j]=arrsim[j][i]=getSimofWords(wl1[i], wl1[j]) 
    weights=[]
    for i in xrange(lenw):
        wti=0
        for j in xrange(lenw):
            wti+=math.fabs(arrsim[i][j])
        weights.append((i,wti))
    weights=sorted(weights,key=lambda x:x[1],reverse=True)
    for item in weights:
        print wl1[item[0]],'%.3f'%(item[1]),
    print ''
    if withWeight:
        return [(wl1[item[0]],item[1]) for item in weights]
    else:
        return [wl1[item[0]] for item in weights]

def _getDistanceofVec(vec1,vec2):
    return np.linalg.norm(vec1-vec2)

def _getCenterDistanceWordList(wl1,withWeight=False):
    # wl1 should be a list of words encoded in utf-8
    lenw=0
    total_vec=scipy.zeros(model.layer1_size)
    for word in wl1:
        # make sure the word2vec model contain key 'word'
        if model.vocab.has_key(word):
            total_vec+=model[word]
            lenw+=1
    if lenw==0:
        centerVec=total_vec
    else:
        centerVec=total_vec/lenw
    print np.linalg.norm(total_vec),total_vec
    print np.linalg.norm(centerVec),centerVec
    distances=[]
    for word in wl1:
        if model.vocab.has_key(word):
            distance=_getDistanceofVec(model[word], centerVec)
#             distances.append((word,1/(distance+0.001)))
            distances.append((word,distance))
    distances=sorted(distances,key=lambda x:x[1])  
    if withWeight:  
        return distances
    else:
        return [item[0] for item in distances]

def _getTfIdfWordList(wl1):
    # wl1 should be a list of words encoded in utf-8
    count_dic={}
    bow=dictionary.doc2bow(wl1)
    for wid,count in bow:
        count_dic[wid]=count
    tfidf_vec1=tfidf[bow]
    tfidf_vec1=sorted(tfidf_vec1,key=lambda x:x[1],reverse=True)    
    for item in tfidf_vec1:
        print dictionary[item[0]],'%.3f'%(item[1]),
    print ''
#     wl=[]
#     for item in tfidf_vec1:
#         for i in xrange(count_dic[item[0]]):
#             wl.append(dictionary[item[0]])     # note that the second loop comes at beginning rather than the end 
    wl=[dictionary[item[0]] for item in tfidf_vec1 for i in xrange(count_dic[item[0]])]
    return wl

def getSimTfIdfFilter(s1,s2,top_num=5):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split()# make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()   
    wl1=_getTfIdfWordList(wl1)[:top_num]  
    wl2=_getTfIdfWordList(wl2)[:top_num] 
    sim0=getSimofWordListTopWeight(wl1, wl2)
    sim1=getSimofWordListTopAve(wl1,wl2) 
    sim2=getSimofWordListPairMatch(wl1,wl2)
    sim3=getSimofWordListVecSum(wl1,wl2)
    print 'TfIdf weight:%.3f,top:%.3f,pair:%.3f,vec:%.3f'%(sim0,sim1,sim2,sim3)

def getSimRelativityFilter(s1,s2,top_num=5):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split() # make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()   
    wl1_f=_getRelativityWordList(wl1)[:top_num]  
    wl2_f=_getRelativityWordList(wl2)[:top_num]          
    sim0=getSimofWordListTopWeight(wl1_f, wl2_f)
    sim1=getSimofWordListTopAve(wl1_f,wl2_f) 
    sim2=getSimofWordListPairMatch(wl1_f,wl2_f)
    sim3=getSimofWordListVecSum(wl1_f,wl2_f)
    wl1_fw=_getRelativityWordList(wl1,withWeight=True)[:top_num]  
    wl2_fw=_getRelativityWordList(wl2,withWeight=True)[:top_num] 
    sim4=getSimofWordListPair(wl1, wl2)
    print 'Self weight:%.3f,top:%.3f,pair:%.3f,vec:%.3f'%(sim0,sim1,sim2,sim3)

def getSimCenterFilter(s1,s2,top_num=5):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split()# make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()   
    wl1=_getCenterDistanceWordList(wl1)[:top_num]  
    wl2=_getCenterDistanceWordList(wl2)[:top_num]          
    sim0=getSimofWordListTopWeight(wl1, wl2)
    sim1=getSimofWordListTopAve(wl1,wl2) 
    sim2=getSimofWordListPairMatch(wl1,wl2)
    sim3=getSimofWordListVecSum(wl1,wl2)
    sim4=getSimofWordListPair(wl1, wl2)
    print 'Self weight:%.3f,top:%.3f,pair:%.3f,vec:%.3f'%(sim0,sim1,sim2,sim3)

def printSimofWordList(wl1,wl2):
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()          
    len1,len2=len(wl1),len(wl2)
    arrsim=np.zeros((len1,len2))
    for i in xrange(len1):
        for j in xrange(len2):
            arrsim[i][j]=getSimofWords(wl1[i], wl2[j])           
    for j in xrange(len2):
        print '\t',wl2[j],     
    for i in xrange(len1):
        print '' 
        print wl1[i],'\t',
        for j in xrange(len2):
            print '%.3f\t'%(arrsim[i][j],),
    print ''
    weights=[]
    for i in xrange(len1):
        wi=0
        for j in xrange(len2):
            wi+=math.fabs(arrsim[i][j])
        weights.append((wi,i))
    weights=sorted(weights,reverse=True)
    for item in weights:
        print wl1[item[1]],'%.3f'%(item[0]-1),
    print ''
        
def getSimofSens(s1,s2,modify=False):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split()# make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()# make sure is a utf-8 str
    printSimofWordList(wl1,wl2)
    sim0=getSimofWordListTopWeight(wl1, wl2)
    sim1=getSimofWordListTopAve(wl1,wl2) 
    sim2=getSimofWordListPairMatch(wl1,wl2)
    sim3=getSimofWordListVecSum(wl1,wl2)
    print 'weight:%.3f,top:%.3f,pair:%.3f,vec:%.3f'%(sim0,sim1,sim2,sim3)
    return sim2

if __name__ =='__main__':       
    #print len(model.vocab)
#     sim=model.similarity('男人', '女人')
#     print sim
#     print getSimofWords('男人', '女人')

#     news1='最高法：包裹冒领应由网店赔偿 | 爱范早读'
    news1='最高法：包裹冒领应由网店赔偿'
#     news2='最高法：包裹冒领应由网店赔偿 | 爱范早读'
    news2='网购快递被冒领怎么办？最高法：卖家全赔'    
#     news2='三星手机被曝存安全漏洞 波及全球超6亿用户'
    getSimofSens(news1,news2) 
    getSimRelativityFilter(news1,news2)
    getSimTfIdfFilter(news1,news2)
#     print getSimofWords('乐逗', '陌陌')
#     print word_sim_dic.similarity('卖家', '网店')
#     print word_sim_dic.has_vocab('卖家', '网店')
#     print dictionary.dfs[dictionary.token2id[u'包裹']]
        