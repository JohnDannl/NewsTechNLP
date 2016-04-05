#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-16

@author: dannl
'''
import database.tablemerge as tablemerge
from database import table,dbconfig,tablemerge2
from database import dbconfig
import jieba
from common.punckit import delpunc
import re,time

merge1_title_file='/home/dannl/tmp/newstech/data/merge1_title'
merge1_title_file_ori='/home/dannl/tmp/newstech/data/merge1_title_ori'
merge1_summary_file='/home/dannl/tmp/newstech/data/merge1_summary'
merge2_title_file='/home/dannl/tmp/newstech/data/merge2_title'
merge2_summary_file='/home/dannl/tmp/newstech/data/merge2_summary'
news_file='/home/dannl/tmp/newstech/data/news.txt'
summary_file='/home/dannl/tmp/newstech/summary.txt'

def getMergeTitle():
    rows=tablemerge.getTitles(dbconfig.mergetable, limit=5000)
    if rows !=-1:
        f_title_ori=open(merge1_title_file_ori,'w')
        with open(merge1_title_file,'w') as fout:
            for row in rows:
                # id,title,summary,ctime,source
                mtid,title,summary,ctime=row[0],row[1].strip(),re.sub('\s+','',row[2]),row[3]
                msg_t_ori='%s %s'%(mtid,title)
                title=delpunc(' '.join(jieba.cut(title)).lower()).encode('utf-8')                
                msg_t='%s %s'%(mtid,title)                
                print msg_t_ori
                fout.write(msg_t+'\n')     
                f_title_ori.write(msg_t_ori+'\n')
        f_title_ori.close()
        
def getTimeSpan():
    rows=tablemerge.getTitles(dbconfig.mergetable, limit=5000)
    min_time,max_time=long(time.time()),0
    if rows !=-1:
        for row in rows:
            # id,title,summary,ctime,source
            mtid,title,summary,ctime=row[0],row[1].strip(),re.sub('\s+','',row[2]),row[3]
            if ctime > max_time:
                max_time=ctime
            if ctime < min_time:
                min_time=ctime
    print time.time()
    print min_time
    print max_time
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(min_time)),'~',\
    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(max_time))
               
        
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
                if len(summary)<len(title):
                    summary=title
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
    
def getText(infile,outfile):
    fout=open(outfile,'w')
    with open(infile,'r') as fin:
        for line in fin:
            line=line.strip().split()
            msg_t='%s %s'%(line[1],' '.join(line[3:]))
            fout.write(msg_t+'\n')
    fout.close()

def getMergeNews():
    print tablemerge.getAllCount(dbconfig.mergetable);
    rows=tablemerge.getTitleSummary(dbconfig.mergetable)
    if rows !=-1:
        with open(news_file,'w') as fout:
            count=0
            for row in rows:
                # id,title,summary,ctime,source
                count+=1
                mtid,title,summary,ctime=row[0],row[1].strip(),re.sub('\s+','',row[2]),row[3]
                title=delpunc(' '.join(jieba.cut(title)).lower()).encode('utf-8')
                summary=delpunc(' '.join(jieba.cut(summary)).lower()).encode('utf-8')
                #timeStr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ctime))
                msg_ts='%s %s %s'%(count,title,summary)                
                fout.write(msg_ts+'\n')   
                
if __name__=='__main__':
    getTimeSpan()
#     getMergeNews()
#     getMergeTitle()
#     getMerge2Title()
#     getText(merge2_title_file,news_file)    # extract title
#     getText(merge2_summary_file,summary_file)   # extract summary
    