____
# HTTP Basic Auth

```bash
curl -u admin:admin http://<SERVER_IP>:<PORT>/
```

```bash
curl http://admin:admin@<SERVER_IP>:<PORT>/
```

# HTTP Authorization Header

```bash
curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' http://<SERVER_IP>:<PORT>/
```

# GET Parameters

```bash
curl 'http://<SERVER_IP>:<PORT>/search.php?search=le' -H 'Authorization: Basic YWRtaW46YWRtaW4='
```

```bash
curl 'http://83.136.253.59:44745/search.php?search=flag' -H 'Authorization: Basic YWRtaW46YWRtaW4='
```

