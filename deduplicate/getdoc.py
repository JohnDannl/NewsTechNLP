#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-16

@author: dannl
'''
import jieba
from database import table,dbconfig,tablemerge
from common.punckit import delpunc
import time

oldtime=time.time()
news_file='/home/dannl/tmp/newstech/data/merge1_title'

class Doc(object):
    def __init__(self,uid,ctime=None,source=None):
        self.uid=uid
        self.ctime=ctime        
        self.source=source

def get_file_records(filename):
    with open(filename,'r') as fin:
        docs={}
        for line in fin:
            line=line.split()
            docs[Doc(line[0],None,None)]=line[1:]
        return docs
        
if __name__=='__main__':
#     docs=get_records_dayago(dbconfig.tableName['sohu'])
    docs=get_file_records(news_file)
    for doc,summary in docs.items():
        print doc.uid,' '.join(summary)
        