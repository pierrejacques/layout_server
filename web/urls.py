#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, time, base64, hashlib
import markdown2
from transwarp.web import ctx
from transwarp.web_append import seeother, notfound, get, post,view
from transwarp.apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
import urlparse
from extractor.evaluator import get_score
import string
@view('index.html')#view类型的返回字典，用来渲染模板
@get('/index')
def signin():
    print ctx.request.para
    return dict()

@api
@get('/api/users')
def getuser():
    print ctx.request.para
    # callback = ctx.request.para['callback']
    # res = '{0}({1})'.format(callback, {'a':1, 'b':2})
    resp = {"users":"12"}
    return resp

@api
@get('/api/admininfo')
def ALLusers():
    print ctx.request.para
    return {'id': '000','name': 'cairuyuan'}

@api
@post('/api/json')
def compute():
    #print (123)
    print ctx.request.para#包含了{'name': u'cairuyuan', 'addr': u'www.sjtu.edu.cn'}这一句的输出
    url = ctx.request.para['addr']
    #print (123)
    print url
    urls = url.replace("http://","").replace("https://","").strip()
    b=get_score(url)
    c=string.atof(b[0:5])
    score=round(c*100)
    host=urls
    print host
    path='/extractor/screenshot/'+urls.replace('.','_').replace('/','+').strip()+'.png'
    print path
    return {'res':score,'path':path}