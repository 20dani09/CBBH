___

# Vhost enum

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u 'http://inlanefreight.local' -H 'Host: FUZZ.inlanefreight.local' -fs 15189
```

```bash
whatweb blog.inlanefreight.local

WordPress[5.1.6]
```
# Wordpress

```bash
wpscan --url http://blog.inlanefreight.local --enumerate --api-token 5L1iakB9rnC4xBx5MHL1Tt42iwkbdFJsWDs3pd0ZjUY
```


WordPress theme in use: twentynineteen

Upload directory has listing enabled: http://blog.inlanefreight.local/wp-content/uploads/

Plugin(s) Identified:    
- email-subscribers
- site-editor
- the-events-calendar

User(s) Identified:  
- erika  
- admin  
- Charlie Wiggins
