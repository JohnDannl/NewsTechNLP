#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-5

@author: dannl
'''
import socket
from config import host,port
import json

def getSimofNews(wordStr): 
    # wordStr is a string joined by ';;' with two word list split with space,encoded in utf-8 or unicode
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

if __name__=='__main__':
    news1='在 游戏 开发 上 三大 vr 平台 各自 的 优势 是 什么'
    news2='三大 vr 平台 在 游戏 上 都 做 了 哪些 布局'
    newstr=';;'.join([news1,news2])
    print getSimofNews(newstr)