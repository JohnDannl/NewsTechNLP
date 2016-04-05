#!/usr/bin/env python 
#-*- coding:utf-8 -*_
'''
Created on 2015-9-12

@author: dannl
'''
rep_id_file='/home/dannl/tmp/newstech/db1/title_rep_id'
w2v_simtid_file='/home/dannl/tmp/newstech/w2v/sim_mtid'
esa_simtid_file='/home/dannl/tmp/newstech/esa_sw/sim_mtid'
lsa_simtid_file='/home/dannl/tmp/newstech/lsa/sim_mtid'
usrdic_simtid_file='/home/dannl/tmp/newstech/usrdic/sim_mtid'

def _get_precise_recall_f1score(stand_set,comp_set):
    _cnt,com_cnt=0.0,0.0
    for item in stand_set:
        if item in comp_set:
            com_cnt+=1
        _cnt+=1
    len_all=len(comp_set)    
    p,r=com_cnt/len_all,com_cnt/_cnt
    #print com_cnt,_cnt,len_all
    return p,r,2*p*r/(p+r)

def get_precise_recall_f1score(stand_file,comp_files):
    stand_set=set([])
    comp_set=set([])
    for line in open(stand_file):
        line=line.split()
        for _id1 in line:
            for _id2 in line:
                if _id1==_id2:
                    continue
                stand_set.add((_id1,_id2))    
    for comp_file in comp_files:
        for line in open(comp_file):
            line=line.split()
            for _mtid in line[1:]:
                comp_set.add((line[0],_mtid))
                comp_set.add((_mtid,line[0]))
    return _get_precise_recall_f1score(stand_set,comp_set)

print get_precise_recall_f1score(rep_id_file,[lsa_simtid_file,])
print get_precise_recall_f1score(rep_id_file,[esa_simtid_file,])
print get_precise_recall_f1score(rep_id_file,[w2v_simtid_file,])
print get_precise_recall_f1score(rep_id_file,[usrdic_simtid_file,])
print get_precise_recall_f1score(rep_id_file,[lsa_simtid_file,esa_simtid_file])
print get_precise_recall_f1score(rep_id_file,[lsa_simtid_file,w2v_simtid_file])
print get_precise_recall_f1score(rep_id_file,[esa_simtid_file,w2v_simtid_file])
print get_precise_recall_f1score(rep_id_file,[w2v_simtid_file,lsa_simtid_file,esa_simtid_file])

        