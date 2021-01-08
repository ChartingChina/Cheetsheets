# Win10 CMD常用命令



## 设置代理

参见[给 Windows 的终端配置代理](https://zcdll.github.io/2018/01/27/proxy-on-windows-terminal/)

```
set http_proxy=http://ip:port

set https_proxy=http://ip:port
```

可以直接添加至用户环境变量



## curl

GET request

```
curl {url}
```

 返回http header

```
curl -i {url}
```

POST request

```
curl -d {data} {url}
```

登录

```
curl -u {username:password} {url}
```

下载文件

```
curl -o {filename} {url}
```

