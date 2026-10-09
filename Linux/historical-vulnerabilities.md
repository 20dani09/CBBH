# Vulnerabilidades históricas de Linux

Referencias para distinguir identificadores, componentes e impacto. Una versión antigua por sí sola no confirma vulnerabilidad: también importan los parches y backports de la distribución.

| Vulnerabilidad | Componente e impacto | Referencia |
| --- | --- | --- |
| Baron Samedit — CVE-2021-3156 | sudo: desbordamiento de memoria con impacto de escalada local. | [Ficha](https://access.redhat.com/security/cve/CVE-2021-3156) |
| CVE-2019-14287 | sudo: error en la interpretación de la identidad de destino que afecta a determinadas reglas. | [Ficha](https://access.redhat.com/security/cve/CVE-2019-14287) |
| CVE-2012-5519 | CUPS: problema de permisos con impacto sobre el acceso privilegiado a archivos. | [Ficha](https://nvd.nist.gov/vuln/detail/CVE-2012-5519) |
| CVE-2021-3560 | polkit: fallo de comprobación de credenciales en solicitudes D-Bus. | [Ficha](https://access.redhat.com/security/cve/CVE-2021-3560) |
| PwnKit — CVE-2021-4034 | polkit/pkexec: corrupción de memoria con impacto de escalada local. | [Ficha](https://www.qualys.com/2022/01/25/cve-2021-4034/pwnkit.txt) |
| Dirty Pipe — CVE-2022-0847 | Kernel Linux: fallo de inicialización de estructuras de pipe que puede afectar a páginas de archivos de solo lectura. | [Ficha](https://access.redhat.com/security/cve/CVE-2022-0847) |

## Distinciones

- PwnKit y el fallo D-Bus de polkit son vulnerabilidades diferentes.
- El identificador del fallo D-Bus es **CVE-2021-3560**; **CVE-2021-3650** es una transposición incorrecta para ese problema.
- El estado de corrección debe comprobarse en los avisos de la distribución instalada.

## Relacionado

- [Inventario del sistema](system-inventory.md)
