# Forensics / DFIR

Notas para analizar evidencias y distinguir **qué prueba un artefacto** de lo que solo podemos inferir.

![Cadena de análisis de evidencia](../assets/diagrams/forensic-evidence-chain.svg)

## Guías

| Tema | Qué contiene |
|---|---|
| [NTFS, $MFT y archivos eliminados](ntfs-deleted-files.md) | Flags de registro, atributos, offsets, verificación de borrado |
| [Windows Data Deduplication](windows-data-deduplication.md) | Chunks, reparse points, ChunkStore y recuperación |
| [Windows Event Logs](../Windows/event-logs.md) | Consultas `Get-WinEvent` y eventos de interés |

## Flujo de trabajo

1. Identificar formato real de la adquisición, sistema de archivos y huso horario.
2. Preservar fuente y hash; trabajar sobre copia o acceso de solo lectura.
3. Extraer artefactos manteniendo ruta, tamaños y procedencia.
4. Interpretar flags, eventos y timestamps **según su campo**.
5. Correlacionar varias fuentes antes de atribuir hechos a una identidad.
6. Validar la recuperación: firma real, apertura, integridad y SHA-256.

> Una adquisición lógica (`.ad1`, por ejemplo) no equivale siempre a una imagen sector a sector. Puede preservar entradas y contenidos seleccionados pero no todo el espacio libre.

[Inicio](../README.md)
