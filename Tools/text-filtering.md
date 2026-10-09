# Filtros de texto con expresiones regulares

```bash
grep -E '^[[:alnum:]]{12}$' rockyou.txt | grep -E '[0-9]' | grep -E '[a-z]' | grep -E '[A-Z]' > wordlist.txt
```
