# coding:utf-8
import urllib2,cookielib,urllib
#定义登录地址
login_url = 'http://192.168.2.223/zabbix/index.php'
#定义登录所需要用的信息，如用户名、密码等，详见下图，使用urllib进行编码
login_data = urllib.urlencode({
                        "name": 'Admin',
                        "password": 'fcpwd1305',
                        "autologin": 1,
                        "enter": "Sign in"})
values={'width': 1269, 'height': 376, 'graphid': '2875', 'stime': '20161014102150', 'period': 3600}
url = "http://192.168.2.223/zabbix/charts.php"
#filename = 'cookie.txt'
#cookie = cookielib.MozillaCookieJar(filename)
cookie = cookielib.MozillaCookieJar()
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
req = urllib2.Request(url,urllib.urlencode(values))
print req
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
#cj = cookielib.CookieJar() #获取Cookiejar对象（存在本机的cookie消息）
#handler = urllib2.HTTPCookieProcessor(cookie)
#opener = urllib2.build_opener(handler)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req).read()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) #自定义opener,并将opener跟CookieJar对象绑定
#urllib2.install_opener(opener) #安装opener,此后调用urlopen()时都会使用安装过的opener对象
#response=opener.open(login_url,login_data).read() #访问登录页，自动带着cookie信息
#cookie.save(ignore_discard=True, ignore_expires=True)
#data = urllib.urlencode(values)
#request = urllib2.Request(url,data)
#response=opener.open(request).read() #访问特定页面，自动带着cookie信息
print response #返回登陆后的页面源代码
