# HTTP: consulta rápida

[Peticiones, cabeceras, métodos, códigos y todos los ejemplos de cURL](../../Tools/curl.md)

HEAD obtiene metadatos sin el contenido de respuesta. PUT crea o reemplaza la representación; PATCH modifica parcialmente el recurso. Los códigos 1xx son informativos, 2xx indican éxito, 3xx redirección o tratamiento condicional, 4xx errores atribuibles a la petición y 5xx errores del servidor.

[HTTP Semantics: RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)

[Índice web](../README.md)

## Terminadores de línea CRLF

Carriage Return (CR) and Line Feed (LF), collectively known as CRLF, are special character sequences used in the HTTP protocol to denote the end of a line or the start of a new one. Web servers and browsers use CRLF to distinguish between HTTP headers and the body of a response. These characters are universally employed in HTTP/1.1 communications across various web server types, such as Apache and Microsoft IIS.
