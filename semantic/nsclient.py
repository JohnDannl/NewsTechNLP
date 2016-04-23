#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-5

@author: dannl
'''
import socket
# from config import host,port
import json

host='222.195.78.189'
port=8893

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
#     news1='这次 是 真的 日媒 称鸿海 或 3 月 9 日 宣布 收购 夏普'
#     news2='一波三折 鸿海 或 3 月 9 日 宣布 收购 夏普'
    news1=''
    news2=''
    newstr=';;'.join([news1,news2])
    print getSimofNews(newstr)