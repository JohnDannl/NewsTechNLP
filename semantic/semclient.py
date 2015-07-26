#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-20

@author: dannl
'''
import socket
from config import host,port
import time
import jieba
from common.punckit import delpunc
import json
from config import news_file,dup_file,rmdup_file,sim_news_file,dup_file_test,rmdup_file_test

def _getRelatedNews(wordStr): 
    # wordStr is a string of word split with space,utf-8 or unicode
    rec_buffer=[]    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))    
        if isinstance(wordStr, unicode):
            wordStr=wordStr.encode('utf-8')
        s.sendall(wordStr)
        while True:
            data = s.recv(1024)
            if not data:
                break
            rec_buffer.append(data)
        s.close()
    except:
        s.close()
        print 'client socket error'
    #print 'Received', repr(''.join(rec_buffer))
    resultStr=''.join(rec_buffer)
    sims=json.loads(resultStr) if resultStr else None
    return sims

def getRelatedNews(wordStr):
    # wordStr is a string of word split with space,utf-8 or unicode
    corpus=list(open(news_file,'r'))
    sims=_getRelatedNews(wordStr)
    if not sims:
        print 'sims is none'
        return
    print 'lsa:'
    for indx,sim in sims['lsa']:
        print indx,sim,corpus[indx],
    print 'esa:'
    for indx,sim in sims['esa']:
        print indx,sim,corpus[indx],
    print 'w2v:'
    for indx,sim in sims['w2v']:
        print indx,sim,corpus[indx],

def getRelatedNewsBatch():
    corpus=list(open(news_file,'r'))
    fout=open(sim_news_file,'w')
    with open(dup_file,'r') as fin:
        for line in fin:
            newStr=''.join(line.split()[4:])
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
            sims=_getRelatedNews(wordStr)
            if not sims:
                print 'sims is none'
                continue
            print >>fout,'lsa:'
            for indx,sim in sims['lsa']:
                print >>fout,sim,corpus[indx],
            print >>fout,'esa:'
            for indx,sim in sims['esa']:
                print >>fout,sim,corpus[indx],
            print >>fout,'w2v:'
            for indx,sim in sims['w2v']:
                print >> fout,sim,corpus[indx],
    fout.close()

def _vote2remove(sims):
    t_lsa,t_esa,t_w2v=0.8,0.7,0.8
    sim_dic={}
    for indx,sim in sims['lsa']:
        if sim<t_lsa:
            continue
        if indx in sim_dic:
            sim_dic[indx]['lsa']=sim
        else:
            _dic={}
            _dic['lsa']=sim
            sim_dic[indx]=_dic
    for indx,sim in sims['esa']:
        if sim<t_esa:
            continue
        if indx in sim_dic:
            sim_dic[indx]['esa']=sim
        else:
            _dic={}
            _dic['esa']=sim
            sim_dic[indx]=_dic
    for indx,sim in sims['w2v']:
        if sim<t_w2v:
            continue
        if indx in sim_dic:
            sim_dic[indx]['w2v']=sim
        else:
            _dic={}
            _dic['w2v']=sim
            sim_dic[indx]=_dic
    return sim_dic

def _getDictStr(dic):
    dic_str=''
    if 'lsa' in dic:
        dic_str='lsa:%f'%(dic['lsa'],)
    if 'esa' in dic:
        dic_str='%s,esa:%f'%(dic_str,dic['esa'])
    if 'w2v' in dic:
        dic_str='%s,w2v:%f'%(dic_str,dic['w2v'])
    return dic_str

def removeDuplication(in_file,out_file):
    corpus=list(open(news_file,'r'))
    fout=open(out_file,'w')
    with open(in_file,'r') as fin:
        for line in fin:
            line=line.split()
            newStr=' '.join(line[4:])
            #print >> fout,line[1],newStr
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
            print >> fout,line[1],wordStr
            sims=_getRelatedNews(wordStr)
            if not sims:
                print 'sims is none'
                continue
            sim_dic=_vote2remove(sims)            
            for indx,_dic in sim_dic.iteritems():
                line_mtid=corpus[indx].split()[0]
                if line_mtid==line[1]: # skip the news itself
                    continue
                #if len(_dic)>=2 and  'w2v' in _dic:
                if len(_dic)>=2:
                    print >> fout,'    ',_getDictStr(_dic),corpus[indx],
    fout.close()
                    
            
if __name__=='__main__':
    oldtime=time.time()
#     newStr='最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'
#     wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
#     print 'wordStr:',wordStr 
#     sims=_getRelatedNews(wordStr)
#     sim_dic=_vote2remove(sims)
#     print sim_dic
#     getRelatedNews(wordStr)
    getRelatedNewsBatch()
#     removeDuplication(in_file=dup_file_test,out_file=rmdup_file_test)
#     removeDuplication(in_file=dup_file,out_file=rmdup_file)
    print 'time cost: %f'%(time.time()-oldtime,)