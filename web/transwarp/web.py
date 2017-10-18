#!/usr/bin/env python
# -*- coding: utf-8 -*-
import types, os, re, cgi, sys, time, datetime,  mimetypes, threading, logging, urllib, traceback
from web_append import RESPONSE_HEADER_DICT, HttpError, RedirectError, Template
from web_append import badrequest, unauthorized, forbidden, notfound, conflict, redirect, found, seeother

from urlparse import parse_qs
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

ctx = threading.local()
fdict = dict() #fdict在启动前配置，启动后不会再修改，无竞争

class Request(object):
    def __init__(self, environ):
        self.environ = environ
        self.request_method = environ['REQUEST_METHOD']
        self.path_info = urllib.unquote(environ.get('PATH_INFO', ''))#请求目录部分
        self.query_str = urllib.unquote(environ.get('QUERY_STRING', ''))#问号后面的部分
        self.para = dict()
        if self.request_method == 'POST':
            fs = cgi.FieldStorage(fp=self.environ['wsgi.input'], environ=self.environ, keep_blank_values=True)
            for key in fs:
                if isinstance(fs[key],list):
                    self.para[key] = [i.value.decode('utf-8') for i in fs[key]]
                else:
                    self.para[key] = fs[key].value.decode('utf-8')
        elif self.request_method == 'GET':
            d = parse_qs(self.query_str)
            for key in d:
                self.para[key] = d[key][0]

class Response(object):
    def __init__(self):
        self.status = '200 OK'
        self.header = {'CONTENT-TYPE': 'text/html; charset=utf-8'}

    @property
    def headers(self):
        return [(RESPONSE_HEADER_DICT.get(k, k), v) for k, v in self.header.iteritems()]

class WSGIApplication(object):
    def __init__(self, document_root=None, **kw):
        self._document_root = document_root
        self.template_engine = None

    def add_module(self, mod):
        for name in dir(mod):
            fn = getattr(mod, name)
            if callable(fn) and hasattr(fn, '__web_route__') and hasattr(fn, '__web_method__'):
                if fdict.get(fn.__web_route__) is None:
                    fdict[fn.__web_route__] = {fn.__web_method__:fn}
                else:
                    fdict[fn.__web_route__][fn.__web_method__] = fn
                logging.info('Add function: %s' % fn.__name__)

    def run(self, port=9000, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        logging.info('application (%s) will start at %s:%s...' % (self._document_root, host, port))
        server = make_server(host, port, self.get_wsgi_application(debug=True))
        server.serve_forever()

    def get_wsgi_application(self, debug=False):#返回的是另外一个函数，wsgi，一个wsgi标准的函数
        def wsgi(env, start_response):
            ctx.request  = Request(env)
            ctx.response = Response()
            method = ctx.request.request_method
            path = ctx.request.path_info
            try:
                d = fdict.get(path,None)
                if d is None:raise badrequest()
                if d[method] is None:raise notfound();
                r = d[method]()             #在fn内部，传递的参数从ctx环境中获取
                if isinstance(r, Template):r = self.template_engine(r.template_name, r.model)#渲染
                if isinstance(r, unicode ):r = r.encode('utf-8')
                if r is None:r = []
                start_response(ctx.response.status, ctx.response.headers)#先发还头部
                return r
            except RedirectError, e:
                start_response(e.status, ctx.response.headers)
                return []
            except HttpError, e:
                start_response(e.status, ctx.response.headers)
                return ['<html><body><h1>', e.status, '</h1></body></html>']
            except Exception, e:
                start_response('500 Internal Server Error', [])
                return ['<html><body><h1>500 Internal Server Error</h1></body></html>']
            finally:
                del ctx.request
                del ctx.response
        return wsgi