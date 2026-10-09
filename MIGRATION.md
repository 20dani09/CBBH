# Migración y consolidación

Fecha: 2026-10-09. Destino: 20dani09/CBBH, rama principal master. La solicitud de trabajar directamente en la rama principal se aplica a la rama existente; no se crea main ni una rama de propuesta.

## Alcance y conservación

Se inventariaron todos los archivos versionados de las ramas predeterminadas de los cinco repositorios. Se leyó el cuerpo completo de los 548 Markdown mediante análisis estático. La revisión técnica manual se centró en duplicados, diferencias relevantes y referencias corregibles; el resto no se presenta como técnicamente verificado. Los historiales completos y ramas distintas a las predeterminadas no forman parte de la auditoría.

Todos los archivos tienen un registro con ruta, tamaño, SHA-256, blob Git y commit de origen. **Contabilizar una fuente no significa que su contenido haya sido importado**. Los cuerpos externos operativos y el material sensible retenido permanecen en sus repositorios de origen. La migración completa solicitada no se ha ejecutado para esas partes.

CBBH conserva sus 176 fuentes Markdown en documentos temáticos y documentos compartidos. Las redacciones de credenciales y referencias a capturas retenidas son excepciones explícitas a la conservación literal. El commit anterior permite consultar el estado original; no se borra ni reescribe el historial.

## Snapshots auditadas

| Repositorio | Rama | Commit | Archivos |
| --- | --- | --- |
| CBBH | master | 284a0a42d23a00f2b47b7460371a517a14cb6261 | 482 |
| pentestNotes | master | ea46064dea8893ed6d54216151ae1bb0ef3661ba | 245 |
| notes | 1 | b4c68ccbe43fe7218e8cee1a15bb7346a6c3bb89 | 130 |
| writeups | main | cc44f026c6c83078dcb8efca200a1aa7f8b0a4b9 | 196 |
| web | main | 782698d7776ac77daa42e454383ee8b185a0be23 | 115 |

## Arquitectura

Las categorías responden al contenido real. No se añadieron secciones vacías de reverse engineering o malware analysis. Los fundamentos compartidos se enlazan desde Certifications, y los laboratorios mantienen cada caso y sus variantes. Las fichas externas indican de forma visible que no contienen un walkthrough importado.

[Índice principal](README.md)

## Métricas

| Métrica | Valor |
| --- | ---: |
| Archivos originales inventariados | 1168 |
| Markdown analizados estáticamente | 548 |
| Imágenes originales | 586 |
| Documentos finales, incluidos índices, auditoría y fichas | 293 |
| Documentos canónicos resultantes de fusiones | 4 |
| Fuentes de esas fusiones | 19 |
| Imágenes finales sin cambios binarios | 261 |
| Grupos de duplicados exactos de todo tipo | 10 |
| Copias adicionales exactas de todo tipo | 12 |
| Candidatos por similitud de contenido | 232 |

## Estados de los documentos originales

| Estado | Markdown originales |
| --- | ---: |
| fusionado: contenido CBBH | 18 |
| nota CBBH conservada | 158 |
| inventariado; cuerpo no importado | 230 |
| importado íntegro | 5 |
| ejemplo local corregido | 1 |
| extracto parcial | 5 |
| fusionado: referencia complementaria | 1 |
| caso externo inventariado; cuerpo no importado | 126 |
| retenido por datos sensibles | 3 |
| duplicado exacto, sin segunda copia | 1 |

## Fusiones y duplicados

Se reúnen 19 fuentes en 4 documentos compartidos de cURL y fundamentos web. Se registran 10 grupos exactos y 12 copias adicionales entre documentos, imágenes y configuración de editor. Las imágenes importadas se almacenan por hash y comparten contenido idéntico. Tres equivalencias de formato se confirmaron entre fuentes externas; sus cuerpos operativos no se republican.

[Decisiones detalladas](Resources/Audit/duplicates.md) · [Candidatos por contenido](Resources/Audit/semantic-candidates.csv)

## Cambios técnicos y de formato

Títulos coherentes, un título principal por documento, bloques etiquetados, rutas normalizadas y enlaces relativos. Se convierten las referencias Obsidian fuera de los bloques de código. Si una captura se retiene o una referencia no existe, se muestra una nota que conduce a su registro de revisión, sin inventar la evidencia.

Las correcciones de HTTP, NoSQL, Requests y contexto histórico están respaldadas por referencias primarias. Los comandos y payloads existentes de CBBH se comparan por el hash de cada cuerpo de bloque después de las redacciones documentadas; no se ejecutan para validarlos.

[Correcciones](Resources/Audit/technical-corrections.md) · [Registro de cambios](Resources/Audit/redactions.csv)

## Trazabilidad y validación

- [Tabla de los 548 documentos](Resources/Audit/migration-table.md)
- [Mapa completo de los 1.168 archivos](Resources/Audit/migration.csv)
- [Imágenes y sus destinos o estados](Resources/Audit/media.csv)
- [Resultados de validación](Resources/Audit/validation.md)
- [Revisión manual y limitaciones](Resources/Audit/review-required.md)

## Mantenimiento

Revisa versiones y referencias cuando utilices una nota. Mantén cada concepto compartido en su documento canónico, conserva los casos individuales y registra cambios de comandos. Los valores de autenticación deben ser marcadores y las capturas deben revisarse antes de añadirse. Ejecuta el validador local después de editar enlaces o mover archivos.

[Pautas y plantillas](CONTRIBUTING.md)
