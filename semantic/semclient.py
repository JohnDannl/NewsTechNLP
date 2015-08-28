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
from config import news_file,rep_file,rmdup_file,sim_news_file,rep_file_test,rmdup_file_test,\
                    dup_id_file,rmdup_id_file,rmdup_idlsa_file,rmdup_idesa_file,rmdup_idw2v_file,\
                    rmdup_idlda_file

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
    for alg in ['lsa','lda','esa','w2v']:
        print alg,':'
        for indx,sim in sims[alg]:
            print indx,sim,corpus[indx],    

def getRelatedNewsBatch():
    corpus=list(open(news_file,'r'))
    fout=open(sim_news_file,'w')
    with open(rep_file,'r') as fin:
        for line in fin:
            newStr=''.join(line.split()[4:])
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
            sims=_getRelatedNews(wordStr)
            if not sims:
                print 'sims is none'
                continue
            for alg in ['lsa','lda','esa','w2v']:
                print >>fout,alg,':'
                for indx,sim in sims[alg]:
                    print >>fout,sim,corpus[indx],            
    fout.close()

def _vote2remove(sims):
    thres={'lsa':0.85,'lda':0.85,'esa':0.7,'w2v':0.8}
    sim_dic={}
    for alg in ['lsa','lda','esa','w2v']:
        for indx,sim in sims[alg]:
            if sim<thres[alg]:
                continue
            if indx in sim_dic:
                sim_dic[indx][alg]=sim
            else:
                _dic={}
                _dic[alg]=sim
                sim_dic[indx]=_dic    
    return sim_dic

def _getDictStr(dic):
    dic_str=''
    for alg,sim in dic.iteritems():
        dic_str='%s,%s:%f'%(dic_str,alg,sim)    
    return dic_str

def removeDuplication(in_file,out_file):
    # in_file:the file with news to be detected,out_file:the duplication result
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
                if len(_dic)>=2 and  'w2v' in _dic:
                #if len(_dic)>=2:
                    print >> fout,'    ',_getDictStr(_dic),corpus[indx],
    fout.close()
    
def removeDuplicationId(in_file):
    corpus=list(open(news_file,'r'))
    fout_lsa=open(rmdup_idlsa_file,'w')
    fout_lda=open(rmdup_idlda_file,'w')
    fout_esa=open(rmdup_idesa_file,'w')
    fout_w2v=open(rmdup_idw2v_file,'w')
    fout=open(rmdup_id_file,'w')
    with open(in_file,'r') as fin:
        for line in fin:
            line=line.split()
            newStr=' '.join(line[4:])
            #print >> fout,line[1],newStr
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
            #print >> fout,line[1],wordStr
            sims=_getRelatedNews(wordStr)
            if not sims:
                print 'sims is none',wordStr
                continue
            sim_dic=_vote2remove(sims)            
            for indx,_dic in sim_dic.iteritems():
                line_mtid=corpus[indx].split()[0]
                if line_mtid==line[1]: # skip the news itself
                    continue
                if len(_dic)>=2 and  'w2v' in _dic:
                #if len(_dic)>=2:
                    print >> fout,line[1],line_mtid
                if 'lsa' in _dic:
                    print >> fout_lsa,line[1],line_mtid
                if 'lda' in _dic:
                    print >> fout_lda,line[1],line_mtid
                if 'esa' in _dic:
                    print >> fout_esa,line[1],line_mtid
                if 'w2v' in _dic:
                    print >> fout_w2v,line[1],line_mtid
    fout.close()        
    fout_lsa.close() 
    fout_lda.close()
    fout_esa.close()     
    fout_w2v.close()   
def _get_precise_recall_f1score(fin_md,dup_id):
    md_cnt,mdcom_cnt=0.0,0.0
    for line in fin_md:
        (id1,id2)=line.split()
        if (id1,id2) in dup_id:
            mdcom_cnt+=1
        md_cnt+=1
    len_all=len(dup_id)    
    p,r=mdcom_cnt/md_cnt,mdcom_cnt/len_all
    #print mdcom_cnt,md_cnt,len_all
    return p,r,2*p*r/(p+r)

def accuracy_recall_f1score():
    fin_dup=open(dup_id_file,'r')
    fin_lsa=open(rmdup_idlsa_file,'r')
    fin_lda=open(rmdup_idlda_file,'r')
    fin_esa=open(rmdup_idesa_file,'r')
    fin_w2v=open(rmdup_idw2v_file,'r')
    fin_id=open(rmdup_id_file,'r')
    dup_id=set()
    for line in fin_dup:
        ids=list(line.split())
        for _id1 in ids:
            for _id2 in ids:
                if _id1==_id2:
                    continue
                dup_id.add((_id1,_id2))     
    p,r,f1s=_get_precise_recall_f1score(fin_lsa, dup_id)
    print 'lsa:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_lda, dup_id)
    print 'lda:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_esa, dup_id)
    print 'esa:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_w2v, dup_id)
    print 'w2v:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_id, dup_id)
    print 'mg3:%.4f, %.4f, %.4f'%(p,r,f1s)
    fin_dup.close()
    fin_lsa.close()
    fin_lda.close()
    fin_esa.close()
    fin_w2v.close()
    
if __name__=='__main__':
    oldtime=time.time()
    newStr='有卵用  亚马逊 让 你 用 耳朵 解锁 手机'
    wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
    print 'wordStr:',wordStr 
    getRelatedNews(wordStr)
#     getRelatedNewsBatch()

#     removeDuplication(in_file=rep_file_test,out_file=rmdup_file_test)
#     removeDuplication(in_file=rep_file,out_file=rmdup_file)
    removeDuplicationId(in_file=rep_file)
    accuracy_recall_f1score()
    print 'time cost: %f'%(time.time()-oldtime,)