# Duplicados y decisiones de fusión

La igualdad exacta se determina por SHA-256 del contenido. La búsqueda de parecidos utilizó el texto completo con TF-IDF y similitud coseno; los nombres no deciden equivalencias. Los candidatos de textos muy cortos o con separadores comunes no se han fusionado automáticamente.

## Duplicados exactos

| Grupo | Archivos originales | Decisión |
| --- | --- | --- |
| 1 | CBBH/.obsidian/community-plugins.json<br>pentestNotes/.obsidian/community-plugins.json<br>web/.obsidian/community-plugins.json | Excluir estado de editor y dependencias, registrando todas las procedencias. |
| 2 | CBBH/.obsidian/core-plugins-migration.json<br>pentestNotes/.obsidian/core-plugins-migration.json<br>web/.obsidian/core-plugins-migration.json | Excluir estado de editor y dependencias, registrando todas las procedencias. |
| 3 | CBBH/.obsidian/graph.json<br>web/.obsidian/graph.json | Excluir estado de editor y dependencias, registrando todas las procedencias. |
| 4 | CBBH/.obsidian/plugins/obsidian-git/data.json<br>pentestNotes/.obsidian/plugins/obsidian-git/data.json | Excluir estado de editor y dependencias, registrando todas las procedencias. |
| 5 | CBBH/11- File Upload/2 - File Upload.md<br>web/CBBH/File Upload.md | Utilizar el documento existente de CBBH; no importar una segunda copia. |
| 6 | CBBH/images/Pasted image 20240924132345.png<br>CBBH/images/Pasted image 20240924165759.png | Compartir un recurso por contenido cuando se importa; los recursos externos solo se inventarían. |
| 7 | CBBH/images/Pasted image 20241216124958.png<br>CBBH/images/Pasted image 20241216125006.png | Compartir un recurso por contenido cuando se importa; los recursos externos solo se inventarían. |
| 8 | pentestNotes/.obsidian/core-plugins.json<br>web/.obsidian/core-plugins.json | Excluir estado de editor y dependencias, registrando todas las procedencias. |
| 9 | notes/.gitbook/assets/Pasted image 20231022130312 (1).png<br>notes/.gitbook/assets/Pasted image 20231022130312.png | Compartir un recurso por contenido cuando se importa; los recursos externos solo se inventarían. |
| 10 | notes/active-directory/README.md<br>notes/import.md | Conservar ambos registros: texto mínimo de índice, sin convertirlo en una técnica. |

Son 10 grupos exactos y 12 copias adicionales entre todos los tipos de archivo. Incluyen archivos de editor, índices mínimos y recursos; no equivalen a 12 notas técnicas redundantes.

## Equivalencias de contenido verificadas

| Par | Diferencia | Tratamiento |
| --- | --- | --- |
| pentestNotes/Web/LFI/Cheatsheet.md y notes/web/lfi.md | Títulos, espaciado o formato de tablas; ejemplos equivalentes en la comparación. | Equivalencia registrada; cuerpos operativos no republicados. |
| pentestNotes/Web/SQLi/SQLmap.md y notes/web/sqlmap.md | Títulos, espaciado o formato de tablas; ejemplos equivalentes en la comparación. | Equivalencia registrada; cuerpos operativos no republicados. |
| pentestNotes/Active Directory/Pass the hash.md y notes/password-attacks/pass-the-hash.md | Títulos, espaciado o formato de tablas; ejemplos equivalentes en la comparación. | Equivalencia registrada; cuerpos operativos no republicados. |

## Contenido complementario: no eliminar como duplicado

- TTY: una versión añade un fragmento de Python que no está en la otra.
- Command Injections: hay diferencias reales en operadores y representación de una nueva línea; requieren revisar la fuente.
- File Upload: los ejemplos de código y las listas de extensiones difieren.
- Los resúmenes y walkthroughs de Proving Grounds contienen niveles de detalle distintos. Cada caso mantiene todos sus registros de origen.

## Fusiones aplicadas

| Documento canónico | Fuentes | Criterio |
| --- | ---: | --- |
| [cURL y HTTP](../../Tools/curl.md) | 9 | Reunir fundamentos y ejemplos distintos; omitir solo ejemplos repetidos y filas de comando idénticas. |
| [Arquitectura web](../../Web-Security/Fundamentals/architecture.md) | 3 | Introducción, disposición y componentes de front end y back end. |
| [Front end](../../Web-Security/Fundamentals/frontend.md) | 3 | Ejemplos complementarios de HTML, CSS y JavaScript. |
| [Back end](../../Web-Security/Fundamentals/backend.md) | 4 | Servidores, bases de datos y APIs. |

Se han consolidado 19 fuentes en 4 documentos compartidos. Los comandos existentes de las notas operativas de CBBH se conservan en sus documentos individuales; no se han sintetizado nuevas cadenas de explotación.

232 pares por encima del umbral de similitud quedaron registrados en [el informe de candidatos](semantic-candidates.csv). Estos pares son candidatos, no fusiones verificadas.
