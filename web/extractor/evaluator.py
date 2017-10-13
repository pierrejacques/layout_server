#_*_ coding: utf-8 _*_

from block import render_notext, path
from experiment_global import features
#from experiment_global import data as ed
from dataset import DataSet
import json
from pymatbridge import Matlab
mlab = Matlab(executable='matlab')
mlab.start()

#extract features from the website.png
def get_feature(url):
  if url:
    sitename=render_notext(url)
    print sitename
    data = DataSet()
    data.load_sample(path, sitename)

    f2 = features.extract(data.data[0])
    dstr = '[%s]' %(','.join(map(str, list(f2))),)
#dstr is a matrix of array
    return dstr
    
#send features to matlab and return score
def matlab(d):
    if not d:
      return 'err'
    else:
      data = json.loads(d)
      res = mlab.run_func('C:/server/web/matlab/evaluator/api_full.m', {'feature': data})
      return str(res["result"])

#use this func to get score
def get_score(url):
    d=get_feature(url)
    score=matlab(d)
    return score
    mlab.stop()
 
#main func for test below
#if __name__ == '__main__':
#  print 'started'
#  t="http://www.baidu.com/"
#  score=get_score(t)
#  print score
