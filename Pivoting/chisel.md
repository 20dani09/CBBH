# Chisel

***

[Tunneling with Chisel and SSF](https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html)

[video](https://www.youtube.com/watch?v=Yp4oxoQIBAM\&t=1469s)

## Running chisel Server on our Attack Host

```bash
sudo ./chisel server --reverse -v -p 1234 --socks5
```

### proxychains.conf

```bash
tail -f /etc/proxychains.conf 

...
socks5 127.0.0.1 1080
```

## Connect the chisel client to our Attack Host

```bash
./chisel client -v 10.10.14.17:1234 R:socks
```
