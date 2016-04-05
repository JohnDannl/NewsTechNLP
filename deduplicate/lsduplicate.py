#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-15

@author: dannl
'''
import logging
from collections import Counter
import getdoc
import time

oldtime=time.time()

class Depository(object):
    ''' usage example:
            depos=Depository(0.8,1.0) # 0.8/1.0 is a similarity threshold
                                        # will list the news whose similarity >=low_thres and 
                                        # <= up_thres
            docs=getdoc.get_records_dayago(30) 
            for doc_id,summary in docs.iteritems(): # summary should be a word list
                depos.add_doc(doc_id,summary)
            new_docs=getdoc.get_new_records(web)
            for doc_id,summary in new_docs.iteritems():
                isnew,exist_doc =depos.add_doc(doc_id,summary)
                if isnew:
                    tablemerge.insert(records(doc_id))
            #after 24 hours ...
            ctime=time.time()-24*3600
            depos.remove_doc_before(ctime)
    '''
    def __init__(self,low_thres=0.8,up_thres=1.0,rmd_file=None):
        self.forindex={}
        self.invindex={}
        self.low_thres=low_thres
        self.up_thres=up_thres
        if rmd_file:
            self.fout=open(rmd_file,'w')
        else:
            self.fout=None
        self.count=0
    def __add_doc(self,doc,summary):
        # add doc to forward index
        self.forindex[doc]=summary
        # add doc to inverse index
        for word in summary:            
            if word in self.invindex:
                self.invindex[word].add(doc)
            else:
                self.invindex[word]=set([doc,])
    def add_doc(self,doc,summary):
        simdocs=[]
        setsum=set(summary)
        for word in setsum:        
            if word in self.invindex:
                simdocs+=self.invindex[word]
        cnt=Counter(simdocs)
        maxsim=cnt.most_common()        
        #print maxsim
        if maxsim:  # maxsim maybe empty []
            len_sum=len(setsum)
            setsim=set(self.forindex[maxsim[0][0]])
            len_sim=len(setsim)
            
#             len_min,len_max=len_sum,len_sim            
#             if len_sum>len_sim:
#                 len_min,len_max=len_sim,len_sum
#         if maxsim and (maxsim[0][1]>=self.low_thres*len(setsum) or \
#                        maxsim[0][1]>=self.low_thres*len(setsim)) and \
#                        (len_max-len_min)<0.2*len_min:

#  instead,we can use a Jaccard similarity coefficient as a evaluation
        if maxsim and maxsim[0][1]>=self.low_thres*(len_sum+len_sim-maxsim[0][1]):
            ##################### print duplicated result
            for i in xrange(len(maxsim)):
                len_sim=len(set(self.forindex[maxsim[i][0]]))
                if maxsim[i][1]>=self.low_thres*(len_sum+len_sim-maxsim[i][1]) \
                    and maxsim[i][1]<=self.up_thres*(len_sum+len_sim-maxsim[i][1]):                    
                    if self.fout:
                        maxdoc,maxnum=maxsim[i]            
                        self.count+=1
                        msg='%s duplicates with %s-->%.3f,%s/(%s,%s)'%(doc.uid,maxdoc.uid,
                            float(maxnum)/(len_sim+len_sum-maxnum),maxnum,len_sum,len_sim)
                        msg1='%s %s'%(self.count,msg)
                        msg2='%s %s'%(doc.uid,' '.join(summary))
                        msg3='%s %s'%(maxdoc.uid,' '.join(self.forindex[maxdoc]))
                        print msg1
                        print msg2
                        print msg3
                        self.fout.write(msg1+'\n')
                        self.fout.write(msg2+'\n')
                        self.fout.write(msg3+'\n')
                else :
                    break   # end loop
            ####################### print duplicated result
            return False,maxsim[0][0]
        else:
            self.__add_doc(doc, summary)
            return True,None
    def __remove_doc(self,doc):
        # remove from the inverse index
        if doc in self.forindex:
            _summary=self.forindex[doc]
            for word in _summary:
                if word in self.invindex and doc in self.invindex[word]:
                    self.invindex[word].remove(doc) 
            # remove from the forward index
            self.forindex.pop(doc)
    def remove_doc_before(self,ctime):
        rms=[]
        for doc in self.forindex:
            if doc.ctime<ctime:
                rms.append(doc)
        for doc in rms:
            self.__remove_doc(doc)
        msg='remove:%s,left:%s'%(len(rms),len(self.forindex))
        print msg
        logging.info(msg)        
    
if __name__=='__main__':        
    news_file='/home/dannl/tmp/newstech/data/merge1_title'
    dup_file='/home/dannl/tmp/newstech/dedup/syntac_dup_0001'
    depos=Depository(0.0,0.1,dup_file)   
    docs=getdoc.get_file_records(news_file)
    for doc,summary in docs.iteritems():
        isnew,dup_doc=depos.add_doc(doc, summary)
        if isnew:
            pass
    print 'time costs:%.2f (s)'%(time.time()-oldtime,)