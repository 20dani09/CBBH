___

One very useful tool in Linux is [proxychains](https://github.com/haad/proxychains), which routes all traffic coming from any command-line tool to any proxy we specify. `Proxychains` adds a proxy to any command-line tool and is hence the simplest and easiest method to route web traffic of command-line tools through our web proxies.

To use `proxychains`, we first have to edit `/etc/proxychains.conf`, comment out the final line and add the following line at the end of it:


```bash
#socks4         127.0.0.1 9050
http 127.0.0.1 8080
```

```bash
proxychains curl http://SERVER_IP:PORT
```

```bash
nmap --proxies http://127.0.0.1:8080 SERVER_IP -pPORT -Pn -sC
```

```bash
msf6> set PROXIES HTTP:127.0.0.1:8080
```



