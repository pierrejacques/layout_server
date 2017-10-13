import numpy as np
import os
import random
from PIL import Image
import csv

random.seed()

#
class DataSet(object):
  def __init__(self, filename=None, sz=None, samplename=None):
    self.labels = []
    self.groups = []
    self.names = []
    self.data = []
    self.samples = []
    self.sz = sz
    if filename is not None:
      self.load(filename, samplename)
    
  def shuffle(self):
    idx = np.argsort([random.random() for i in xrange(len(self.labels))])
    self.data = [self.data[i] for i in idx]
    self.labels = self.labels[idx]
    if len(self.samples)==len(self.labels):
      self.samples = self.samples[idx]
    if len(self.groups) == len(self.labels):
      self.groups = self.groups[idx]

# load single picture
  def load_sample(self, path, name):
    for filename in os.listdir(path):
      _n = filename.replace('.png', '')
      if _n == name:
        im = Image.open(os.path.join(path, filename))
        im = im.convert("L")
        # resize to given size (if given)
        if (self.sz is not None) and isinstance(self.sz, tuple) and (len(self.sz) == 2):
          im = im.resize(self.sz, Image.ANTIALIAS)
        self.data.append(np.asarray(im, dtype=np.uint8))
        self.labels.append(0)
        self.names.append(_n)

#load group pictures
  def load(self, path, samplepath):
    filename_to_samples = None
    if samplepath!=None:
      filename_to_samples = dict(list(csv.reader(open(samplepath, "rb"))))
    for dirname, dirnames, filenames in os.walk(path):
      c = 0
      for subdirname in dirnames:
        if subdirname == 'mid':
          c+=1
          continue
        print subdirname
        subject_path = os.path.join(dirname, subdirname)
        for filename in os.listdir(subject_path):
          _n = filename.replace('_g.png', '')
          #if not block_text.find({'sitename': _n}).count():
          #  continue
          try:
            im = Image.open(os.path.join(subject_path, filename))
            im = im.convert("L")
            # resize to given size (if given)
            if (self.sz is not None) and isinstance(self.sz, tuple) and (len(self.sz) == 2):
              im = im.resize(self.sz, Image.ANTIALIAS)
            self.data.append(np.asarray(im, dtype=np.uint8))
            self.labels.append(c)
            self.names.append(_n)
            if filename_to_samples!=None:
              self.samples.append(int(filename_to_samples[filename]))
          except IOError:
            pass
        c+=1
    self.labels = np.array(self.labels, dtype=np.int)


class DataGroup:
  def __init__(self, data, label, nodes, max_depth):
    self.data = data
    self.label = label
    self.nodes = nodes
    self.max_depth = max_depth

  def img_data(self, node):
   t, l, w, h = node['pos']
   if(self.data[t:t+h, l:l+w].shape==(700, 0)):
     print self.data.shape
     print t, t+h, l, l+w
   return self.data[t:t+h, l:l+w]

  def all_img_data(self):
    data = []
    for node in self.nodes:
      data.append(self.img_data(node))
    return data

  def get_mapping(self):
    mapping = {}
    for node in self.nodes:
      mapping[int(node['id'])] = node
    return mapping

#code for test below

#data = DataSet('C:\\server\\web\\extractor\\groups\\')
#data = DataSet()
#data.load('C:\\server\\web\\extractor\\groups\\','')
#data.load_sample('C:\\server\\web\\extractor\\groups\\','test' )
#print data.labels
#print data.groups
#print data.names