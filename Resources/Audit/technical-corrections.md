# Correcciones verificadas y límites

| Fuente | Hallazgo | Cambio | Referencia primaria |
| --- | --- | --- | --- |
| Métodos HTTP de CBBH | HEAD confundía cuerpo de petición y de respuesta; PUT se describía solo como creación. | Corregida la explicación; comandos originales preservados. | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) |
| Bases de datos de CBBH | NoSQL se describía como ausencia universal de esquemas y relaciones. | Aclarado que depende del modelo y del producto. | [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/) |
| Frameworks y APIs de CBBH | Nombre de SOAP y descripción de REST demasiado restrictiva. | Aclaración editorial; no se cambia el XML ni la petición original. | [REST de Roy Fielding](https://www-dev.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) |
| Python de Burp en pentestNotes | Diccionario inválido y request.get sin módulo correcto. | Fragmento corregido con Requests y validado por AST, sin realizar peticiones. | [Requests: Proxies](https://requests.readthedocs.io/en/stable/user/advanced/#proxies) |
| Opciones de Nmap en notes | -Pn no equivale simplemente a desactivar ICMP; -A incluye scripts. | Explicación del extracto corregida. | [Manual Nmap](https://nmap.org/book/man.html) |
| nmap.md de notes | -V se confundía con detección de versiones. | Hallazgo registrado; documento operativo no importado. -sV detecta versiones y -V muestra la versión de Nmap. | [Detección de versiones](https://nmap.org/book/man-version-detection.html) |
| Android emulator de pentestNotes | Instalación de Anbox presentada sin contexto histórico. | Marcado como proyecto archivado desde 2024-02-13. | [Repositorio oficial](https://github.com/anbox/anbox) |
| Javascript deobfuscation de pentestNotes | Falta una barra en el esquema de URL de cURL. | Corrección de sintaxis, sin modificar el resto de argumentos. | [Manual de cURL](https://curl.se/docs/manpage.html) |

No se han corregido ni probado exploits para hacerlos operativos. Los cambios de parámetros por redacción de secretos están registrados por separado. No hay una garantía de exactitud técnica del resto de las 548 notas.
