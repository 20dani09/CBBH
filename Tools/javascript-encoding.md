# Javascript deobfuscation

## Commands

|**Command**|**Description**|
|---|---|
|`curl http://SERVER_IP:PORT/`|cURL GET request|
|`curl -s http://SERVER_IP:PORT/ -X POST`|cURL POST request|
|`curl -s http://SERVER_IP:PORT/ -X POST -d "param1=sample"`|cURL POST request with data|
|`echo hackthebox \| base64`|base64 encode|
|`echo ENCODED_B64 \| base64 -d`|base64 decode|
|`echo hackthebox \| xxd -p`|hex encode|
|`echo ENCODED_HEX \| xxd -p -r`|hex decode|
|`echo hackthebox \| tr 'A-Za-z' 'N-ZA-Mn-za-m'`|rot13 encode|
|`echo ENCODED_ROT13 \| tr 'A-Za-z' 'N-ZA-Mn-za-m'`|rot13 decode|

## Deobfuscation Websites

|**Website**|
|---|
|[JS Console](https://jsconsole.com)|
|[Prettier](https://prettier.io/playground/)|
|[Beautifier](https://beautifier.io/)|
|[JSNice](http://www.jsnice.org/)|

## Misc

|**Command**|**Description**|
|---|---|
|`ctrl+u`|Show HTML source code in Firefox|

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| pentestNotes | Web/Javascript deobfuscation.md | ea46064dea8893ed6d54216151ae1bb0ef3661ba |

[Índice de categoría](README.md) · [Inicio](../README.md)
