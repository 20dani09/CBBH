____

https://crt.sh/

```
https://crt.sh/?cn=%.paypal.com
```

```
https://crt.sh/?O=Paypal
```

```bash
curl -s https://crt.sh/\?cn\=%.$1\&output=json | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u
```


