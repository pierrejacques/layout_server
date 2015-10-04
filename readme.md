#ReadMe

### 依赖项

1. python
	- 安装依赖库 pip install [ * ],
		1. jinja2
		2. gevent
		3. gunicorn


2. nginx
	- 配置文件位于conf下nginx.conf.
		1. 启动: nginx -c [path]
		2. 测试: nginx -t [path]
		3. 其他:
	  		- nginx -s stop    [-c path]
	  		- nginx -s quit    [-c path]
	  		- nginx -s reload  [-c path]
	- ssl配置
		1. cd /usr/local/nginx/conf
			- openssl genrsa -des3 -out server.key 1024
			- openssl req -new -key server.key -out server.csr
			- openssl rsa -in server.key -out server_nopwd.key
			- openssl x509 -req -days 365 -in server.csr -signkey server_nopwd.key -out server.crt
		2. 配置nginx的https
			- listen 443 ssl;
			- ssl_certificate   [ path ]/server.crt;
			- ssl_certificate_key  [ path ]/server_nopwd.key;
			- 不要用哪个ssl on，问题多。
	   

3. 运行
	- 使用在mac下，先直接运行./run.sh，再根据帮助信息操作


4. 目录
	- conf 是配置文件
	- doc  是用到的一些模块的说明
	- web  是程序主目录