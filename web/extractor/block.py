from ghost import Ghost
from utils import decode
import os
import traceback
import time

path = os.path.join(os.path.dirname(__file__), 'screenshot')


def get_sitename(url):
  url = url.replace("http://", "").replace("https://", "").strip()
  return url.replace('.', '_').replace('/', '+').strip() 

#save png from url
def render_notext(url):
  sitename = get_sitename(url)
  ghost = Ghost()
  ghost.open(url, headers={
    "Accept":"image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    })
 
  ghost.wait_for_page_loaded()
  #time.sleep(10)
  ghost.capture_to(os.path.join(path,sitename +'.png'),(0,0,1280,700))
  return sitename
  print "success"


if __name__ == '__main__':
  t = "http://www.baidu.com/"
  try:
    render_notext(t)
  except Exception,e :
    sitename = get_sitename(t) + '.png'
    print e
    if(os.path.isfile(os.path.join(path, sitename))):
     os.unlink(os.path.join(path, sitename))
    
    traceback.print_exc()

