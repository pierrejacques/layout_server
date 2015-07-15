1  开始

	使用www目录下的wsgiapp.py作为主文件运行

	需要安装的python库主要有jinja2

	一些使系统更加高效得库在windows下不能应用，gunicorn等

2  配置

	使用nginx作为web服务器，动态请求代理到web框架中。

	nginx的配置文件在conf中，里面的root路径根据操作系统不同，存放位置不同，具体修改

	nginx的具体使用，在Doc中