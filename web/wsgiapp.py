#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)

import os, time
from datetime import datetime

import urls
from transwarp.web import WSGIApplication


class TemplateEngine(object):
    def __call__(self, path, model):
        return '<!-- override this method to render template -->'
class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        if not 'autoescape' in kw:
            kw['autoescape'] = True
        self._env = Environment(loader=FileSystemLoader(templ_dir), **kw)
    def add_filter(self, name, fn_filter):
        self._env.filters[name] = fn_filter
    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')

# init wsgi app:
wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))
template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
wsgi.template_engine = template_engine
wsgi.add_module(urls)#把url中的路径-函数，打包成映射关系，路径:route，route是从原python函数


if __name__ == '__main__':
    wsgi.run(9000, host='0.0.0.0')#自己运行，使用内置的web服务器
else:
    application = wsgi.get_wsgi_application()#传递给其他模块
