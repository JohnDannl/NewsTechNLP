#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-13

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gvdictionary import GvDictionary
import time

doc_file='/home/dannl/tmp/newstech/news.txt'
dic_file='/home/dannl/tmp/newstech/glove/news.dic'

oldtime=time.time()

def getDocuments(file_name):
    for line in open(file_name):
        yield line.split()[1:]

dictionary = GvDictionary(getDocuments(doc_file),prune_at=4000000)
dictionary.filter_extremes(no_below=2, no_above=1.0, keep_n=400000)
# dictionary=GvDictionary.load(dic_file)
# print dictionary.token2id['中国']
dictionary.save(dic_file) # store the dictionary, for future reference

print 'dictionary size: %s'%(len(dictionary),)
print 'dictionary collocations: %s'%(dictionary.num_nnz)
print 'time cost:%s' % str(time.time()-oldtime)