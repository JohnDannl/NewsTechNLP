#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-1-23

@author: JohnDannl
'''

####### For semantic server ###########
host='localhost'               # Symbolic name meaning all available interfaces
port = 8898              # Arbitrary non-privileged port

####### For removing duplicates #############
rep_file='/home/dannl/tmp/newstech/db1/title_rep'
dup_id_file='/home/dannl/tmp/newstech/db1/title_rep_id'
news_file='/home/dannl/tmp/newstech/news.txt'
sim_news_file='/home/dannl/tmp/newstech/rmdup/sim_news'
rmdup_file='/home/dannl/tmp/newstech/rmdup/rmdup_news'

rmdup_idlsa_file='/home/dannl/tmp/newstech/rmdup/rmdup_idlsa'
rmdup_idesa_file='/home/dannl/tmp/newstech/rmdup/rmdup_idesa'
rmdup_idw2v_file='/home/dannl/tmp/newstech/rmdup/rmdup_idw2v'
rmdup_id_file='/home/dannl/tmp/newstech/rmdup/rmdup_id'

######## For test #########################
rep_file_test='/home/dannl/tmp/newstech/db1/title_rep_test'
rmdup_file_test='/home/dannl/tmp/newstech/rmdup/rmdup_test'
sim_file_test='/home/dannl/tmp/newstech/rmdup/sim_news_test'
