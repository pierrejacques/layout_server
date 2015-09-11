#_*_ coding: utf-8 _*_

from block import render_notext, path
from experiment_global import features
#from experiment_global import data as ed
from dataset import DataSet
import json
from pymatbridge import Matlab
import string
mlab = Matlab(executable='matlab')
mlab.start()

#class ExtractHandler(tornado.web.RequestHandler):
def get_feature(url):
    #d = self.get_argument('url', None)
   # id = self.get_argument('id', None)
  if url:
    sitename=render_notext(url)
    print sitename
    data = DataSet()
    data.load_sample(path, sitename)
    #data.load_dom(5)
     
#extract features from the website.png
    f2 = features.extract(data.data[0])
    dstr = '[%s]' %(','.join(map(str, list(f2))),)
    return dstr
    #print type(dstr)
   # print dstr
#      conn = urllib2.urlopen('http://192.168.1.113:8001/lr?data='+dstr)
#      score = conn.read()
#      conn.close()
#      self.set_header("Access-Control-Allow-Origin", "*")
#      self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
#      self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")
#      self.set_header("Access-Control-Allow-Credentials", "true")
#      self.finish({
#        'score': score,
#        'img': sitename + '.png',
#        'id': id
#      })
#      return
#    self.finish('error')
def matlab(d):
    print d
    if not d:
      return 'err'
    else:
      data = json.loads(d) 
      res = mlab.run_func('C:/server/web/matlab/evaluator/api_full.m', {'feature': data})
      return str(res["result"])
'''class FindHanlder(tornado.web.RequestHandler):
  def get(self):
    d = self.get_argument('sitename', None)
    for i, en in enumerate(ed.names):
      if en.startswith(d):
        data = {
          'id': i+1,
          'feature': list(ffs[i]),
        }
        self.finish(data)
        return
    self.finish('not found')


application = tornado.web.Application([
  (r'^/e$', ExtractHandler),
  (r'^/f$', FindHanlder),
])
'''
def get_score(url):
    d=get_feature(url)
    score=matlab(d)
    return score
    mlab.stop()
#if __name__ == '__main__':
# # application.listen(7009)
#  print 'started'
#  t="http://www.acfun.tv/"
#  score=get_score(t)
#  print type(string.atof(score))
#  print string.atof(score)