#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-27

@author: dannl
'''
from gensim.models.word2vec import Word2Vec

import logging
from numpy.linalg.linalg import norm
import numpy as np
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
import scipy
import jieba
from common.punckit import delpunc
from config import w2v_md_file,news_file
model = Word2Vec.load(w2v_md_file)
model.init_sims(replace=True) # To load a static model to save memory
def getSimofWords(w1,w2):
    # words must be in utf-8 code
    if w1==w2:
        return 1.0    
    if w1 in model.vocab and w2 in model.vocab:
        return model.similarity(w1,w2)    
    return 0.0  # a specified value for any word not in vocab
def getSimofWordList(wl1,wl2):
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

def getSimofWordListTop(wl1,wl2):
    # two word lists should better be utf-8
    wordStr=' '.join(wl1)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl1=wordStr.encode('utf-8').split()
    wordStr=' '.join(wl2)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wl2=wordStr.encode('utf-8').split()      
    len1,len2=len(wl1),len(wl2)   
    print ' '.join(wl1)
    print ' '.join(wl2) 
    print len1,len2
    sim_sum=0.0       
    for i in xrange(len1):
        sim_max=0.0
        for j in xrange(len2):
            sim_cur=getSimofWords(wl1[i], wl2[j]) 
            if sim_cur>sim_max:
                sim_max=sim_cur
        sim_sum+=sim_max    
    minlen=len1 if len1<=len2 else len2
    return sim_sum/minlen

def getSimofSens(s1,s2):
    wl1=delpunc(' '.join(jieba.cut(s1.lower()))).split()# make sure is a utf-8 str  
    wl2=delpunc(' '.join(jieba.cut(s2.lower()))).split()# make sure is a utf-8 str  
    return getSimofWordListTop(wl1, wl2)

if __name__ =='__main__':       
    print len(model.vocab)
    sim=model.similarity('男人', '女人')
    print sim
    print getSimofWords('男人', '女人')
#     vec1=model['男人']
#     vec2= model['女人']
#     sim1=scipy.dot(vec1.T,vec2)
#     print sim1
    sim=model.similarity('乔布斯', '苹果公司')
    print sim
#     results=model.most_similar(positive=['哈佛大学', '中国'], negative=['美国'])
#     for word,sim in results:
#         print word,sim
#     print model['中国']
#     vec0=scipy.zeros(model.layer1_size)
#     vec0+=model['中国']
    #print vec0
#     print norm(vec0)
    news1='最高法：包裹冒领应由网店赔偿 | 爱范早读'
#     news2='最高法：包裹冒领应由网店赔偿 | 爱范早读'
    news2='网购快递被冒领怎么办？最高法：卖家全赔'    
    print 'news sim:',getSimofSens(news1,news2) 

    