#ReadMe
如何使用？

	- 将server文件夹放在系统/目录下
	- cd到server目录下  sudo ./run.sh  根据提示操作
	- 其他的都不用配置了。。。
	- 

<hr>
<br>

## 1. python
	- jinja2
	- gevent
	- gunicorn
## 2. nginx
    - 安装
    	1. Mac
    		- brew install nginx
    		- 找配置文件， find /usr -name nginx.conf
    	2. Windows
		3. Linux
	- 运行
		1. 自用配置文件位于conf下nginx.conf.不同操作系统不混用
		2. 启动: nginx -c [path]
		3. 测试: nginx -t [path]
		4. 其他:
	  		- nginx -s stop    [-c path]
	  		- nginx -s quit    [-c path]
	  		- nginx -s reload  [-c path]
	- SSL
		1. cd 到存储证书等文件的目录
			- openssl genrsa -des3 -out server.key 1024
			- openssl req -new -key server.key -out server.csr
			- openssl rsa -in server.key -out server_nopwd.key
			- openssl x509 -req -days 365 -in server.csr -signkey server_nopwd.key -out server.crt
		2. 配置nginx的https
			- listen 443 ssl;
			- ssl_certificate   [ path ]/server.crt;
			- ssl_certificate_key  [ path ]/server_nopwd.key;
			- 不要用那个ssl on，问题多。
## 3. 运行
	- 使用在mac下，先直接运行./run.sh，再根据帮助信息操作
	- windows下，暂时不支持。

## 4. 目录
	- conf 是配置文件
	- doc  是用到的一些模块的说明
	- web  是程序主目录
	- *猴子的插件在 web/static/js/plugin.js
	
	🍺  /usr/local/Cellar/opencv/2.4.12: 225 files, 36M
	
	/Users/zoe/.local/lib/python2.7/site-packages
	/usr/local/lib/python2.7/site-packages
	
