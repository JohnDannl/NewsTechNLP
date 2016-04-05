#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-16

@author: dannl
'''
import matplotlib.pyplot as plt

def precise_recall2thres():
    pos_samp=[33,201,256,176,116,77,64,40,134]
    pre_samp=[7186,1255,439,225,131,83,69,42,134]
    pres=[]
    recs=[]
    tot_pos=sum(pos_samp)
    mis_pos=0
    for i in xrange(9):
        pres.append(float(pos_samp[i])/pre_samp[i])
        recs.append((tot_pos-mis_pos)/float(tot_pos))
        print '%02d-%02d,p:%.5f,r:%.5f'%(i+1,i+2,pres[i],recs[i])
        mis_pos+=pos_samp[i]
        
    print tot_pos
    plt.figure(1)
    plt.plot([i*0.1 for i in xrange(1,10)],pres,'k',linewidth=1.5)
    plt.title('Precise to different Jaccard coefficient thresholds')
    # plt.title('Precise to different Jaccard coefficient thresholds',y=-0.1,fontsize=20)
    plt.figure(2)
    plt.plot([i*0.1 for i in xrange(1,10)],recs,'k',linewidth=1.5)
    plt.title('Recall to different Jaccard coefficient thresholds')
    # plt.title('Recall to different Jaccard coefficient thresholds',y=-0.1)
    plt.show()

def predict_ratio(n):
#     pre_samp=[14497,7186,1255,439,225,131,83,69,42,134]
    pre_samp=[7186,1255,439,225,131,83,69,42,134]
    tot_cmp=(n-1)*n/2
    tot_pre=sum(pre_samp)
    ratios=[]
    for i in xrange(len(pre_samp)):              
        ratios.append(float(tot_pre)/tot_cmp)
        print '%02d-%02d,r:%.5f'%(i+1,i+2,ratios[i])
        tot_pre-=pre_samp[i]          
        
    plt.figure(1)
    plt.plot([i*0.1 for i in xrange(1,len(pre_samp)+1)],ratios,'k',linewidth=1.5)
    plt.title('Ratio to different Jaccard coefficient thresholds')
    # plt.title('Precise to different Jaccard coefficient thresholds',y=-0.1,fontsize=20)
   
    plt.show()

predict_ratio(5000)