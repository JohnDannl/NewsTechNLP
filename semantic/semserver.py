#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-7-20

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
import socket
from config import host,port
import os
import threading
import time
import json

from newslsa import lsa2sim
from newslda import lda2sim
from newsesa import esa2sim
from newsw2v import w2v2sim

# from newslsa.lsa2sim import *
# from newsesa.esa2sim import *
# from newsw2v.w2v2sim import *

# def update():
#     while True:
#         oldtime=time.time()
#         global index
#         if addNewCorpus() or not index: # add new corpus or index does not exist
#             reindex()
#             reloadmodel()
#         print "reindex at time:",time.asctime(),'time cost (s):',str(time.time()-oldtime)
#         time.sleep(120)
    
def server_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    print 'Server begins to listen on port: %s'%(port,)
    while True:
        sock, addr = s.accept()
        print 'Connection from', addr
        threading.Thread(target=process_query, args=(sock,addr)).start()

def process_query(sock,addr):
    #oldtime=time.time()
    data = sock.recv(4096)
    print 'receive:',data
#     global index,mvids
#     if not index:
#         print 'index is none'
#         sock.sendall('')
#         sock.close()
#         return
    wordList=data.split()
    lsa_sim=lsa2sim.getSimNews(wordList)
    lda_sim=lda2sim.getSimNews(wordList)
    esa_sim=esa2sim.getSimNews(wordList)
    w2v_sim=w2v2sim.getSimNews(wordList)
    sims={}
    lsa_list=[]
    for indx,sim in lsa_sim:
        lsa_list.append((int(indx),sim))
    lda_list=[]
    for indx,sim in lda_sim:
        lda_list.append((int(indx),sim))
    esa_list=[]
    for indx,sim in esa_sim:
        esa_list.append((int(indx),sim))
    w2v_list=[]
    for indx,sim in w2v_sim:
        w2v_list.append((int(indx),sim))
    sims={'lsa':lsa_list,'lda':lda_list,'esa':esa_list,'w2v':w2v_list}
    resultStr= json.dumps(sims)    
    #print 'reply:',resultStr
    sock.sendall(resultStr)
    sock.close()
    #print 'cost time:',time.time()-oldtime

if __name__=='__main__':   
#     threading.Thread(target=update).start()
    server_listen()