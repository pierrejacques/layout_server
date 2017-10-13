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
    return {'users':'12'}

@api
@get('/api/admininfo')
def ALLusers():
    print ctx.request.para
    return {'id': '000','name': 'cairuyuan'}

@api
@post('/api/json')
def compute():
    print ctx.request.para['addr']
    url=ctx.request.para['addr']
    urls = urlparse.urlparse(url)
    host = urls.netloc
    print host
    b = get_score(url)
    c= string.atof(b[0:5])
    score= round(c*100)
    path = '/extractor/screenshot/'+host.replace('.','_')+'+.png'
    print path
    return {'res': score, 'path':path }
