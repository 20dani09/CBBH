# NTFS — $MFT y archivos eliminados

La Master File Table (`$MFT`) contiene registros que describen archivos y directorios. La eliminación de un archivo puede liberar el registro **sin borrar inmediatamente todos sus metadatos o datos**.

## Estructura simplificada

```text
Imagen forense -> volumen NTFS -> $MFT -> registro "FILE"
    cabecera (Flags de registro)
    $STANDARD_INFORMATION (0x10, timestamps / FILE_ATTRIBUTE)
    $FILE_NAME            (0x30, nombre y referencias)
    $DATA                 (0x80, contenido/residentes o runs)
    $REPARSE_POINT        (0xC0, si existe)
```

## Campos que importan

| Campo | Offset en registro | Interpretación |
|---|---|---|
| Firma `FILE` | `0x00` | Registro FILE |
| Offset primer atributo | `0x14` | Ubicación de atributos |
| **Record Flags** | **`0x16`** | `0x0001` registro en uso; `0x0002` directorio |
| `$STANDARD_INFORMATION` | Variable | Timestamps y atributos del archivo |
| `$FILE_NAME` | Variable | Nombre y metadatos vinculados al directorio |
| `$DATA` | Variable | Datos residentes / lista de clusters |
| `$REPARSE_POINT` | Variable | Tag + datos específicos |

**Record Flags** y **FILE_ATTRIBUTE** no son equivalentes. `0x0000` en el campo de flags del registro indica que `InUse` está desactivado. Un archivo borrado puede conservar `FILE_ATTRIBUTE_REPARSE_POINT` y otros atributos.

## Inspección inicial con Python

El ejemplo solo interpreta **la cabecera** de una entrada MFT ya extraída. No aplica NTFS USA/fixups ni reemplaza un parser forense completo.

```python
from pathlib import Path
import struct

mft = Path("mft.bin").read_bytes()
entry = 46
record_size = 1024  # Confirmar el tamaño real a partir del volumen
start = entry * record_size
rec = mft[start:start + record_size]

if len(rec) != record_size or rec[:4] != b"FILE":
    raise ValueError("Registro no válido")
flags = struct.unpack_from("<H", rec, 0x16)[0]
first_attr = struct.unpack_from("<H", rec, 0x14)[0]
print(f"entry={entry} start=0x{start:08X}")
print(f"flags=0x{flags:04X} in_use={bool(flags & 1)}")
print(f"directory={bool(flags & 2)} first_attribute=0x{first_attr:X}")
```

Los registros no miden universalmente 1.024 bytes. El tamaño debe comprobarse antes de calcular offsets absolutos.

## Comprobación de borrado

1. Localizar nombre exacto y referencia de archivo/directorio.
2. Comprobar flag `InUse` en el registro, posibles reasignaciones y consistencia.
3. Si están disponibles, correlacionar `$UsnJrnl`, `$LogFile`, papelera y eventos pertinentes.
4. Separar timestamps `$STANDARD_INFORMATION` y `$FILE_NAME`: tienen semánticas distintas.
5. No confundir “nombre encontrado” con “contenido recuperado y válido”.

| Evidencia | Demuestra | No demuestra |
|---|---|---|
| Nombre en MFT | El nombre estuvo almacenado | Que el archivo aún exista |
| `InUse=0` | El registro está libre | Quién eliminó el fichero |
| `REPARSE_POINT` | El archivo tiene reparse metadata | Que sea Data Deduplication sin leer tag |
| Exportación del tamaño esperado | Bytes exportados | Que sean los bytes originales |
| SHA-256 | Identidad/integridad de esos bytes | Autoría o motivo |

## Verificar un DOCX recuperado

```bash
file recovered.docx
unzip -t recovered.docx
unzip -l recovered.docx | head
sha256sum recovered.docx
```

En PowerShell: `Get-FileHash .\recovered.docx -Algorithm SHA256`.

## Relacionado

- [Data Deduplication](windows-data-deduplication.md)
- [Eventos Windows](../Windows/event-logs.md)
- [NTFS Technical Reference (Microsoft)](https://learn.microsoft.com/en-us/windows/win32/fileio/ntfs-technical-reference)

[DFIR](./README.md)
