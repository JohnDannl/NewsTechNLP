#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-3-17

@author: dannl
'''

syntax_path='/home/dannl/tmp/newstech/dedup/syntac_dup_'
err_path='/home/dannl/tmp/newstech/dedup/err_'
dup_path='/home/dannl/tmp/newstech/dedup/dup_'
out_path='/home/dannl/tmp/newstech/expdata/'

def printLSASim(input_file,output_file=None):
    from newslsa import lsa2sim
    fout=None
    if output_file:
        fout=open(output_file,'w')
    with open(input_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            a_id,a_wl=a[0],a[1:]
            b=fin.readline().split()
            b_id,b_wl=b[0],b[1:]
            msg='%s --> %s:%.5f'%(a_id,b_id,lsa2sim.getSimofNews(a_wl, b_wl))
            print msg
            if fout:
                fout.write(msg+'\n')

def printESASim(input_file,output_file=None):
    from newsesa import esa2sim
    fout=None
    if output_file:
        fout=open(output_file,'w')
    with open(input_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            a_id,a_wl=a[0],a[1:]
            b=fin.readline().split()
            b_id,b_wl=b[0],b[1:]
            msg='%s --> %s:%.5f'%(a_id,b_id,esa2sim.getSimofNewsPrune(a_wl, b_wl))
            print msg
            if fout:
                fout.write(msg+'\n')
def printSGSim(input_file,output_file=None):
    from newsw2v import sg2sim
    fout=None
    if output_file:
        fout=open(output_file,'w')
    with open(input_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            a_id,a_wl=a[0],a[1:]
            b=fin.readline().split()
            b_id,b_wl=b[0],b[1:]
            msg='%s --> %s:%.5f'%(a_id,b_id,sg2sim.getSimofNews(a_wl, b_wl))
            print msg
            if fout:
                fout.write(msg+'\n')
                
def printCBOWSim(input_file,output_file=None):
    from newsw2v import cbow2sim
    fout=None
    if output_file:
        fout=open(output_file,'w')
    with open(input_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            a_id,a_wl=a[0],a[1:]
            b=fin.readline().split()
            b_id,b_wl=b[0],b[1:]
            msg='%s --> %s:%.5f'%(a_id,b_id,cbow2sim.getSimofNews(a_wl, b_wl))
            print msg
            if fout:
                fout.write(msg+'\n')
                
def printGloveSim(input_file,output_file=None):
    from summaryglove import glove2sim
    fout=None
    if output_file:
        fout=open(output_file,'w')
    with open(input_file,'r') as fin:
        while True:
            line=fin.readline()
            if not line:
                break
            a=fin.readline().split()
            a_id,a_wl=a[0],a[1:]
            b=fin.readline().split()
            b_id,b_wl=b[0],b[1:]
            msg='%s --> %s:%.5f'%(a_id,b_id,glove2sim.getSimofNews(a_wl, b_wl))
            print msg
            if fout:
                fout.write(msg+'\n')
suffix='0306'
err_file=err_path+suffix
dup_file=dup_path+suffix
syntax_file=syntax_path+suffix

lsa_out_file=out_path+'lsa_'+suffix
esa_out_file=out_path+'esa_'+suffix
sg_out_file=out_path+'sg_'+suffix
cbow_out_file=out_path+'cbow_'+suffix
glove_out_file=out_path+'glove_'+suffix
# printGloveSim(syntax_file,glove_out_file)

printLSASim(syntax_file,lsa_out_file)
printESASim(syntax_file,esa_out_file)
printSGSim(syntax_file,sg_out_file)
printCBOWSim(syntax_file,cbow_out_file)

exam_file='/home/dannl/tmp/newstech/expresult/example'
# input_file=exam_file

input_file=dup_file
# input_file=err_file
# printLSASim(input_file)
# printESASim(input_file)
# printSGSim(input_file)
# printCBOWSim(input_file)