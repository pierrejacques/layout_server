1  开始
	pip工具安装：下载https://bootstrap.pypa.io/get-pip.py，并运行
	预先安装必须的python库，如jinja2. 可根据运行提示安装
		下载源文件解压，python setup.py install
		使用pip工具，pip install jinja2

	python库列表
		https://pypi.python.org/pypi/pip/

	一些使python运行更高效的库在windows上不支持如gunicorn，gevent


2  配置
	使用nginx作为web服务器，下载http://nginx.org
	windows中
		nginx配置文件在conf文件夹中：nginx.conf
		server的conf文件夹下有已经配置好的文件，去掉windows后缀替换
			需要注意修改配置文件中的几处 root后面的路径
			根据python代码存放不同可修改
	*nix
		配置文件位置各有不同
		mac 


3   运行
	*nix
		nginx &
		切到wsgiapp.py目录下
		/usr/local/bin/gunicorn --bind 127.0.0.1:9000 --workers 1 --worker-class gevent wsgiapp:application
		必要时加前缀路径

	windows
		运行nginx
		python wsgiapp:application即可


4	目录
	conf是配置文件的备份
	doc是用到的一些模块的说明
	wed是程序主目录