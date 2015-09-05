#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-27

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
from config import w2v_md_file,news_file,tfidf_md_file,dict_file,word_sim_dict_file
import json

model = Word2Vec.load(w2v_md_file)
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

def getSimofWordListVec(wl1,wl2):   
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

def getSimofWords(w1,w2,userDict=False):
    # words must be in utf-8 code
    if isinstance(w1, unicode):
        w1=w1.encode('utf-8')
    if isinstance(w2, unicode):
        w2=w2.encode('utf-8')
    if w1==w2:
        return 1.0    
    if userDict and word_sim_dic.has_vocab(w1,w2):
        return word_sim_dic.similarity(w1,w2)
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
    while 0 not in np.shape(asim):
        i,j=np.unravel_index(asim.argmax(), asim.shape)
        sim_sum+=asim[i][j]
#         print asim
#         print asim[i][j],asim.shape,i,j,wl1[i],wl2[j]        
#         del wl1[i],wl2[j]    # this will change the parent wl1's value 
        asim=np.delete(asim, i, 0)
        asim=np.delete(asim, j, 1)
    minlen=len1 if len1<=len2 else len2
    return sim_sum/minlen

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
threshold=0.801
delta=0.001
class WordSimDict():
    def __init__(self,dict_file):
        self._file=dict_file
        self.dict={}
        self.__load_dict()
    def __load_dict(self):
        try:
            dic_file=open(self._file,'r')
            self.dict=json.load(dic_file,encoding='utf-8')
            dic_file.close()
            print 'dict length:',self.__len__()
        except:
            print 'word_sim_dict file does not exist and will be created...'
            self.dict={}            
    def __len__(self):
        return len(self.dict)    
    def __getitem__(self, word_pair):
        if not isinstance(word_pair, unicode):
            word_pair=word_pair.decode('utf-8')
        return self.dict[word_pair]        
    def has_vocab(self,word1,word2):
        word_pair='%s::%s'%(word1,word2)
        if not isinstance(word_pair, unicode):
            word_pair=word_pair.decode('utf-8')
        return word_pair in self.dict
    def similarity(self,word1,word2):
        word_pair='%s::%s'%(word1,word2)
        return self.__getitem__(word_pair)    
    def update_dict(self,sim_ave,entries):
        entry_set=set(entries)
        len_ori=len(set(entries))        
        count=0
        discard=[]
        for entry in entry_set:
            if entry.sim<0.01 or entry.sim >=1.0:
                count+=1
                discard.append(entry)
        for entry in discard:
            entry_set.discard(entry)
        len_new=len(entry_set)
        print 'old:%d,new:%d'%(len_ori,len_new)
        percent=(threshold-sim_ave)*len_ori/(sim_ave*len_new)         
        for entry in entry_set:
            new_sim=entry.sim*(1+percent)
            if new_sim>1.0:
                new_sim=1.0
            new_sim=round(new_sim,7)
            key1=('%s::%s'%(entry.w1,entry.w2)).decode('utf-8')
            key2=('%s::%s'%(entry.w2,entry.w1)).decode('utf-8')
            if key1 in self.dict and self.dict[key1]>new_sim:
                continue
            if key2 in self.dict and self.dict[key2]>new_sim:
                continue
            self.dict[key1]=new_sim
            self.dict[key2]=new_sim            
    def save_dict(self):
        with open(self._file,'w') as fout:
            json.dump(self.dict,fout,encoding='utf-8',ensure_ascii=True)
        print 'dict length:',self.__len__()               
    def print_dict(self,top=10):
        count=0
        for w_pair,sim in self.dict.iteritems():
            count+=1
            if count>top:
                break
            print '%d %s %.3f'%(count,w_pair,sim)
            
word_sim_dic=WordSimDict(word_sim_dict_file)

def getSimofWordListPairMod(wl1,wl2,modify=False):
    # two word lists should better be utf-8
    entries=[]
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    len1,len2=len(wl1),len(wl2)     
    asim=np.zeros((len1,len2))
    for i in xrange(len1):
        for j in xrange(len2):
            asim[i][j]=getSimofWords(wl1[i], wl2[j],modify) 
    sim_sum=0.0    
    while 0 not in np.shape(asim):
        i,j=np.unravel_index(asim.argmax(), asim.shape)
        sim_sum+=asim[i][j]        
        entries.append(Entry(wl1[i],wl2[j],asim[i][j]))  
        del wl1[i],wl2[j]    # this will change the parent wl1's value 
#         print asim
#         print asim[i][j],asim.shape,i,j,wl1[i],wl2[j]        
        asim=np.delete(asim, i, 0)
        asim=np.delete(asim, j, 1)          
#     for entry in entries:
#         print entry.w1,entry.w2,entry.sim
    minlen=len1 if len1<=len2 else len2
    sim_ave=sim_sum/minlen
    if modify and sim_ave<threshold-delta:
        word_sim_dic.update_dict(sim_ave, entries)
    return sim_ave

def getSimofWordListTopMod(wl1,wl2,modify=False):
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
            sim_cur=getSimofWords(wl1[i], wl2[j],modify) 
            sim_arr[i][j]=sim_cur            
            if sim_cur>sim_max:
                sim_max=sim_cur
                max_j=j            
        sim_sum+=sim_max            
        entries.append(Entry(wl1[i],wl2[max_j],sim_max))
    for j in xrange(len2):
        sim_max,max_i=0.0,0
        for i in xrange(len1):
            if sim_arr[i][j]>sim_max:
                sim_max=sim_arr[i][j]
                max_i=i
        sim_sum+=sim_max        
        entries.append(Entry(wl1[max_i],wl2[j],sim_max))    
#     for entry in entries:
#         print entry.w1,entry.w2,entry.sim
    sim_ave=sim_sum/(len1+len2)
    if modify and sim_ave<threshold-delta:
        word_sim_dic.update_dict(sim_ave, entries)
    return sim_ave

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
    if len(tfidf_vec1)<len(tfidf_vec2):
        vec_s,vec_l=tfidf_vec1,tfidf_vec2
    else:        
        vec_s,vec_l=tfidf_vec2,tfidf_vec1    
    sim_sum=0.0       
    for wdi,weight_i in vec_s:
        sim_max=0.0
        for wdj,weight_j in vec_l:
            sim_cur=getSimofWords(dictionary[wdi], dictionary[wdj]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=weight_i**2*sim_max   
    return sim_sum

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
            
def getSimofSens(s1,s2,modify=False):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split()# make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()# make sure is a utf-8 str
    printSimofWordList(wl1,wl2)
    #getSimofWordListTopWeight(wl1, wl2)
    sim1=getSimofWordListTopMod(wl1,wl2,modify) 
    sim2=getSimofWordListPairMod(wl1,wl2,modify)
    sim3=getSimofWordListVec(wl1,wl2)
    print 'sim1:%.3f,sim2:%.3f,sim3:%.3f'%(sim1,sim2,sim3)
    return sim2

if __name__ =='__main__':       
    #print len(model.vocab)
#     sim=model.similarity('男人', '女人')
#     print sim
#     print getSimofWords('男人', '女人')
#     sim=model.similarity('乔布斯', '苹果公司')
#     print sim
#     results=model.most_similar(positive=['哈佛大学', '中国'], negative=['美国'])
#     for word,sim in results:
#         print word,sim
#     print model['中国']
#     vec0=scipy.zeros(model.layer1_size)
#     vec0+=model['中国']
    #print vec0
#     print norm(vec0)
    news1='最高法：包裹冒领应由网店赔偿'
#     news2='最高法：包裹冒领应由网店赔偿 | 爱范早读'
    news2='网购快递被冒领怎么办？最高法：卖家全赔'    
    getSimofSens(news1,news2,True) 
    getSimofSens(news1,news1,True) 
    word_sim_dic.save_dict()    
#     print word_sim_dic.similarity('卖家', '网店')
#     print word_sim_dic.has_vocab('卖家', '网店')
#     print dictionary.dfs[dictionary.token2id[u'包裹']]
        