'''
Created on 2015-7-28

@author: dannl
'''
import jieba
from common.punckit import delpunc
from newsw2v import w2vword2sim
from config import news_file,rep_file,rmdup_file,sim_news_file,rep_file_test,rmdup_file_test,sim_file_test,\
                    dup_id_file,rmdup_id_file,rmdup_idlsa_file,rmdup_idesa_file,rmdup_idw2v_file
import time
oldtime=time.time()  
                  
def getRelatedNewsBat(in_file,out_file):
    corpus=list(open(news_file,'r'))
    fout=open(out_file,'w')    
    with open(in_file,'r') as fin:
        for line in fin:
            line=line.split()
            newStr=' '.join(line[4:])
            #print >> fout,line[1],newStr
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')            
            wl1=wordStr.split()
            sims=[]
            for i in xrange(len(corpus)):
                news=corpus[i].split()
                wl2=news[1:]
                (_sq,sim)=i,w2vword2sim.getSimofWordList(wl1, wl2)
                sims.append((_sq,sim))
            sims=sorted(sims,key=lambda x:x[1],reverse=True)  
            print >> fout,line[1],wordStr                  
            for indx,sim in sims[:11]:
                line_mtid=corpus[indx].split()[0]
                if line_mtid==line[1]: # skip the news itself
                    continue
                #if len(_dic)>=2 and  'w2v' in _dic:                
                print >> fout,'    %.4f,%s'%(sim,corpus[indx]),
    fout.close()
    
def removeDuplicationId(in_file):
    corpus=list(open(news_file,'r'))    
    fout_w2v=open(rmdup_idw2v_file,'w')
    with open(in_file,'r') as fin:
        for line in fin:            
            line=line.split()
            newStr=' '.join(line[4:])
            print line[1],newStr
            #print >> fout,line[1],newStr
            wordStr=delpunc(' '.join(jieba.cut(newStr)).lower()).encode('utf-8')
            wl1=wordStr.split()
            sims=[]
            for i in xrange(len(corpus)):
                news=corpus[i].split()
                wl2=news[1:]
                (_sq,sim)=i,w2vword2sim.getSimofWordList(wl1, wl2)
                sims.append((_sq,sim))
            sims=sorted(sims,key=lambda x:x[1],reverse=True) 
            for indx,sim in sims[:11]:
                line_mtid=corpus[indx].split()[0]
                if sim<0.7:
                    break
                if line_mtid==line[1]: # skip the news itself
                    continue  
                print >> fout_w2v,line[1],line_mtid    
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
    p,r,f1s=_get_precise_recall_f1score(fin_esa, dup_id)
    print 'esa:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_w2v, dup_id)
    print 'w2v:%.4f, %.4f, %.4f'%(p,r,f1s)
    p,r,f1s=_get_precise_recall_f1score(fin_id, dup_id)
    print 'mg3:%.4f, %.4f, %.4f'%(p,r,f1s)
    fin_dup.close()
    fin_lsa.close()
    fin_esa.close()
    fin_w2v.close()
    
if __name__=='__main__':
#     getRelatedNewsBat(rep_file_test,sim_file_test)
#     removeDuplicationId(rep_file)
    accuracy_recall_f1score()
    print 'time cost: %f'%(time.time()-oldtime,)