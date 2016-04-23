#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016-4-22

@author: dannl
'''
from common.common import postHtml

def getSemDepParse(text,pattern='sdp'):
    get_url='http://api.ltp-cloud.com/analysis/?'
    post_url='http://api.ltp-cloud.com/analysis/'
    #pattern='sdp'   # ws(分词)，pos(词性标注)，ner(命名实体识别)，dp(依存句法分析)，
                    # sdp(语义依存分析)，srl(语义角色标注),all(全部任务)
    rformat='json'
    api_key = 'z6E3r5X4PrPwwK2cwsFl0QCzIZsBGLqasDMSqh7m'
    data={'api_key':api_key,
          'pattern':pattern,
          'format':rformat,
          'text':text
          }
    content=postHtml(post_url, data)
    return content

if __name__=='__main__':
#     text = '最高法：网购快递被冒领应由销售者赔偿 快递公司不担责'   
#     text = '我在餐厅用勺子喝玉米汤'   
#     text = '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制'    
    text = '网购快递被冒领怎么办？最高法：卖家全赔'
    result=getSemDepParse(text)        
    print result
    
    