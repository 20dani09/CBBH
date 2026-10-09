# Servidores HTTP locales

### Servidores HTTP locales



```bash
python3 -m http.server
```

#### Python 2.7: compatibilidad histórica

```bash
python2.7 -m SimpleHTTPServer
```

#### PHP

```bash
php -S 0.0.0.0:8000
```

#### Ruby

```bash
ruby -run -ehttpd . -p8000
```

## Relacionado

- [Peticiones HTTP con cURL](curl.md)

## Servidor de archivos del cliente Python

| Comando | Descripción |
| --- | --- |
| `sudo python3 -m http.server 8001`                                                                                       | Starts a python web server for quick hosting of files. Performed from a Linux-basd host.             |
