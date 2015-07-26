#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
from config import merge1_title_file,merge1_summary_file,merge2_title_file,merge2_summary_file,news_file
import database.tablemerge as tablemerge
from database import table,dbconfig,tablemerge2
from database import dbconfig
import jieba
from common.punckit import delpunc
import re

def getMergeTitle():
    rows=tablemerge.getTitleSummary(dbconfig.mergetable)
    if rows !=-1:
        f_summary=open(merge1_summary_file,'w')
        with open(merge1_title_file,'w') as fout:
            count=0
            for row in rows:
                # title,summary,ctime,source
                count+=1
                mtid,title,summary,ctime=row[0],row[1].strip(),re.sub('\s+','',row[2]),row[3]
                title=delpunc(' '.join(jieba.cut(title)).lower()).encode('utf-8')
                summary=delpunc(' '.join(jieba.cut(summary)).lower()).encode('utf-8')
                #timeStr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ctime))
                msg_t='%s %s %s %s'%(count,mtid,ctime,title)
                msg_s='%s %s %s %s'%(count,mtid,ctime,summary)
                print msg_t
                print msg_s
                fout.write(msg_t+'\n')                
                f_summary.write(msg_s+'\n')
        f_summary.close()
        
def getMerge2Title():
    rows=tablemerge2.getTitleSummary(dbconfig.mergetable2)
    if rows !=-1:
        f_summary=open(merge2_summary_file,'w')
        with open(merge2_title_file,'w') as fout:
            count=0
            for row in rows:
                # title,summary,ctime,source
                count+=1
                mtid,title,summary,ctime=row[0],row[1].strip(),re.sub('\s+','',row[2]),row[3]               
                title=delpunc(' '.join(jieba.cut(title)).lower()).encode('utf-8')
                summary=delpunc(' '.join(jieba.cut(summary)).lower()).encode('utf-8')
                #timeStr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ctime))
                msg_t='%s %s %s %s'%(count,mtid,ctime,title)
                msg_s='%s %s %s %s'%(count,mtid,ctime,summary)
                print msg_t
                print msg_s
                fout.write(msg_t+'\n')                
                f_summary.write(msg_s+'\n')
        f_summary.close()
def getNews():
    fout=open(news_file,'w')
    with open(merge2_title_file,'r') as fin:
        for line in fin:
            line=line.strip().split()
            msg_t='%s %s'%(line[1],' '.join(line[3:]))
            fout.write(msg_t+'\n')
    fout.close()
if __name__=='__main__':
#     getMergeTitle()
#     getMerge2Title()
    getNews()