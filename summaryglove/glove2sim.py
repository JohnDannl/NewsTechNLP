#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-12

@author: dannl
'''
from glove import Glove
from glove import Corpus
import scipy
import numpy as np

model_file='/home/dannl/tmp/newstech/glove/glove.model'
cooc_file='/home/dannl/tmp/newstech/glove/word.cooc'

# corpus_coocc=Corpus.load(cooc_file)
model = Glove.load(model_file)

def _get_wl_vec(wordList):
    # wordList is a list of word:[word1,word2,...,wordn]
    total_vec=scipy.zeros(model.no_components)
    wordStr=' '.join(wordList)
    if isinstance(wordStr,unicode): # make sure word is utf-8 str type
        wordList=wordStr.encode('utf-8').split()
    for word in wordList:
        # make sure the word2vec model contain key 'word'        
        if model.dictionary.has_key(word):
            total_vec+=model.word_vectors[model.dictionary[word]]
    return total_vec

def getSimofNews(wordList1,wordList2):
    vec1=_get_wl_vec(wordList1)
    vec2=_get_wl_vec(wordList2)
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

if __name__=='__main__':
#     news1='这次 是 真的 日媒 称鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
#     news2='一波三折 鸿海 或 3 月 9 日 宣布 收购 夏普'.split()
    news1='小米'.split()
    news2='华为'.split()
    print getSimofNews(news1, news2)
    query='小米'
#     print model.word_vectors[model.dictionary[query]]
#     for word,sim in model.most_similar(query, number=10):
#         print word,sim