____

https://crt.sh/

```
https://crt.sh/?cn=%.paypal.com
```

```
https://crt.sh/?o=Paypal
```

```bash
curl -s 'https://crt.sh/?cn=paypal.com&output=json' | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u
```

```bash
curl -s 'https://crt.sh/?o=paypal&output=json' | jq -r '.[].common_name' | sed 's/\*\.//g' | sort -u > paypal.txt
```

```bash
cat paypal.txt | rev | cut -d "." -f 1,2 | rev | sort -u
```