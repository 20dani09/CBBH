# Requests a través de Burp Suite

Las claves del diccionario de proxies son http y https. El método pertenece al módulo requests o a la sesión. El argumento arg.url debe existir en el programa que utiliza el fragmento.

```python
import requests

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}
s = requests.Session()
s.proxies = proxies
```

Para la llamada ya presente en las notas:

```python
requests.get(arg.url, proxies=proxies, verify=False)
```

verify=False desactiva la comprobación del certificado TLS; se documenta aquí porque formaba parte del ejemplo de un proxy local.

[Documentación oficial de Requests](https://requests.readthedocs.io/en/stable/user/advanced/#proxies)
