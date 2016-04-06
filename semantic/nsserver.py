#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-5

@author: dannl
'''
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
import sys
sys.path.append('..')
import socket
from config import host,port
import threading
import time
import json
from newsesa import esa2sim
from newsw2v import sg2sim,cbow2sim

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
    news1,news2=data.split(';;')
    wordlist1=news1.split()
    wordlist2=news2.split()
    esa_sim=esa2sim.getSimofNews(wordlist1,wordlist2)
    sg_sim=sg2sim.getSimofNews(wordlist1,wordlist2)
    cbow_sim=cbow2sim.getSimofNews(wordlist1,wordlist2)    
    sims={'esa':esa_sim,'sg':sg_sim,'cbow':cbow_sim}
    resultStr= json.dumps(sims)    
    #print 'reply:',resultStr
    sock.sendall(resultStr)
    sock.close()
    #print 'cost time:',time.time()-oldtime

if __name__=='__main__':   
#     threading.Thread(target=update).start()
    server_listen()