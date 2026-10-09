# Validación de la migración

Fecha: 2026-10-09. Resultado de la validación local: PASS.

## Comprobaciones realizadas

| Comprobación | Resultado |
| --- | ---: |
| Markdown finales | 293 |
| Enlaces internos comprobados, incluidas imágenes | 2358 |
| Referencias locales de imagen | 254 |
| Bloques de ejemplo de las fuentes comprobados por hash | 550 |
| Fragmentos en línea de las fuentes comprobados por hash | 531 |
| Imágenes finales verificadas por SHA-256 | 261 |
| Archivos originales con registro de trazabilidad | 1168 |
| Errores de estructura, referencias o integridad | 0 |

Todos los Markdown tienen un título principal y bloques de código etiquetados. No quedan wikilinks Obsidian fuera de bloques. Todos los destinos del mapa de migración existen. El ejemplo corregido de Requests se validó por sintaxis Python; no se realizó una petición de prueba.

Se conservan las variantes de ejemplos que difieren. Las sustituciones de valores sensibles y las correcciones benignas documentadas son excepciones explícitas a la conservación literal. Los cuerpos operativos externos no forman parte de la comprobación de conservación en el destino porque no se importaron.

## Imágenes

OCR sobre 583 imágenes únicas, equivalentes a 586 archivos originales. Se revisó visualmente una muestra de 6 diagramas de fundamentos HTTP y arquitectura. Los recursos publicados conservan sus bytes originales. OCR y muestreo no garantizan que se haya detectado todo dato sensible. Las capturas retenidas se indican mediante referencias al registro de medios, no mediante enlaces de imagen rotos.

## Enlaces externos

Se inventariaron 1253 literales URL en todas las fuentes y se separaron 520 referencias documentales fuera de bloques de código. Dos falsos 404 de PortSwigger recibidos por HEAD se contrastaron con las páginas oficiales. Los resultados individuales distinguen accesible, no solicitado, fallo de red y ausente confirmado o referencia que requiere autenticación; no se presenta toda la lista como verificada.

| Estado | Referencias |
| --- | ---: |
| not-requested | 270 |
| network-unverified | 69 |
| reachable | 176 |
| requires-authentication | 1 |
| missing | 1 |
| http-unverified | 1 |
| reachable-verified-by-web | 2 |

## Límites

La validación comprueba formato, referencias e integridad de la migración. No acredita la exactitud técnica de todos los apuntes ni la vigencia de servidores, versiones o comandos de laboratorio. No se han ejecutado exploits, probado payloads ni contactado con endpoints de los ejercicios. La revisión abarca las ramas predeterminadas a los commits registrados, no todos los historiales o ramas.

## Informes reproducibles

- [Trazabilidad completa](migration.csv)
- [Integridad de ejemplos y recursos](integrity.json)
- [Enlaces externos](external-links.csv)
- [Referencias retenidas o no resueltas](link-review.csv)
- [Revisión pendiente](review-required.md)
- [Validador local](../../scripts/validate.py)


Ejecutar desde la raíz:

```bash
python3 scripts/validate.py --migration
```
