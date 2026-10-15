_____

`ifconfig` shows an IP of 172.19.0.2 on eth0.

There’s a `.dockerenv` file in the filesystem root

## Ping sweep

```bash
for i in {1..254}; do (ping -c 1 172.19.0.${i} | grep "bytes from" | grep -v "Unreachable" &); done;
```

# Port scan

```bash
for port in {1..65535}; do echo > /dev/tcp/172.19.0.1/$port && echo "$port open"; done 2>/dev/null          
```


# docker toolbox
https://stackoverflow.com/questions/32646952/docker-machine-boot2docker-root-password

```bash
ssh docker@72.17.0.1
password: tcuser
```
