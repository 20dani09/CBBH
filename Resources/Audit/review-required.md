# Revisión pendiente

## Material sensible

Se encontraron 3 bloques de clave privada en las fuentes siguientes. No se han copiado sus valores ni sus documentos operativos a CBBH:

- notes/write-ups/proving-grounds-play/infosecprep.md, línea 76.
- notes/write-ups/proving-grounds-play/seppuku.md, línea 91.
- writeups/Proving Grounds Practice/Windows/WriteUps/DVR4.md, línea 153.

Las claves podrían ser de laboratorio, pero su contexto no basta para autorizar su republicación. Si alguna pertenece a un sistema real, debe revocarse. Los cuatro repositorios externos permanecen sin cambios y podrían seguir exponiendo esos valores. No se ha reescrito ningún historial Git.

En CBBH se han sustituido valores de tokens, cookies, una clave de API y direcciones de correo por marcadores. El token de WPScan es un dato especialmente relevante para revisar. Si continúa siendo válido, debe rotarse: quitarlo del estado actual no lo elimina del historial.

[Hallazgos sin valores](sensitive-findings.csv) · [Cambios y redacciones](redactions.csv)

## Capturas

La revisión OCR abarca 583 imágenes únicas, equivalentes a los 586 archivos de imagen. Se trata de una revisión automática; no certifica que no existan datos sensibles fuera del texto reconocido. No se publican de nuevo las capturas con coincidencias de credenciales, correos, tokens o claves ni las que no se pudieron leer. Sus referencias muestran un enlace al registro de medios.

[Medios y estados de revisión](media.csv)

## Documentación externa no migrada íntegramente

Las fichas de laboratorio conservan nombre, plataforma cuando consta, procedencia, tamaño y referencias de integridad. Sus cuerpos operativos, comandos de explotación y evidencias externas no se han importado. Los catálogos técnicos tienen la misma limitación. Esta es una consolidación documental parcial; no sustituye íntegramente los cinco repositorios.

## Aspectos técnicos sin verificar

- Los servidores, puertos y credenciales de los ejercicios son históricos. No se han conectado ni probado.
- Las notas genéricas de CVE, extracción de credenciales, evasión y escalada externa no se han validado ni actualizado para funcionar contra objetivos.
- El ejemplo de Scrapy existente referencia interesting_extensions sin definirlo. Se conserva y requiere revisar el objetivo del fragmento.
- Los fragmentos PHP de bases de datos incluyen una sentencia incompleta y concatenación insegura de entradas; se han señalado, sin reconstruir la aplicación.
- La ruta red/values de la nota APK requiere comprobar el directorio real del proyecto.
- Las tablas de Command Injections presentan diferencias reales entre fuentes. No se han resuelto incorporando nuevas instrucciones de explotación.
- Anbox está archivado; se conserva como entorno histórico.

## Documentos breves o incompletos

Son candidatos automáticos por longitud o formato, no pruebas de que la nota carezca de valor.

| Fuente | Estado | Destino |
| --- | --- | --- |
| CBBH/1- Web Requests/HTTP Fundamentals/3 - HTTP Requests and Responses.md | fusionado: contenido CBBH | [Tools/curl.md](../../Tools/curl.md) |
| CBBH/14- Broken Authentication/3 - Session Tokens.md | nota CBBH conservada | [Web-Security/Authentication/session-tokens.md](../../Web-Security/Authentication/session-tokens.md) |
| CBBH/15- Web Attacks/1 - HTTP Verb Tampering.md | nota CBBH conservada | [Web-Security/Access-Control-and-XXE/http-verb-tampering.md](../../Web-Security/Access-Control-and-XXE/http-verb-tampering.md) |
| CBBH/17-Session Security/6 - Open Redirect.md | nota CBBH conservada | [Web-Security/Session-Security/open-redirect.md](../../Web-Security/Session-Security/open-redirect.md) |
| CBBH/18- Web Service & API Attacks/2 - Command Injection.md | nota CBBH conservada | [Web-Security/API/command-injection.md](../../Web-Security/API/command-injection.md) |
| CBBH/18- Web Service & API Attacks/4 - File Upload.md | nota CBBH conservada | [Web-Security/API/file-upload.md](../../Web-Security/API/file-upload.md) |
| CBBH/18- Web Service & API Attacks/5 - LFI.md | nota CBBH conservada | [Web-Security/API/lfi.md](../../Web-Security/API/lfi.md) |
| CBBH/18- Web Service & API Attacks/6 - XSS.md | nota CBBH conservada | [Web-Security/API/xss.md](../../Web-Security/API/xss.md) |
| CBBH/2- Introduction to Web Applications/4 - Back End Components/2 - Web Servers.md | fusionado: contenido CBBH | [Web-Security/Fundamentals/backend.md](../../Web-Security/Fundamentals/backend.md) |
| CBBH/3- Using Web Proxies/2 - Encoding - Decoding.md | nota CBBH conservada | [Tools/Burpsuite/encoding-decoding.md](../../Tools/Burpsuite/encoding-decoding.md) |
| CBBH/3- Using Web Proxies/5 - Scanner.md | nota CBBH conservada | [Tools/Burpsuite/scanner.md](../../Tools/Burpsuite/scanner.md) |
| CBBH/7- XSS/4 - Skills Assessment.md | nota CBBH conservada | [Labs-and-Writeups/CBBH/xss/assessment.md](../../Labs-and-Writeups/CBBH/xss/assessment.md) |
| CBBH/API Attacks/10 - Unsafe Consumption of APIs.md | nota CBBH conservada | [Web-Security/API/unsafe-consumption-of-apis.md](../../Web-Security/API/unsafe-consumption-of-apis.md) |
| CBBH/API Attacks/8 - Security Misconfiguration.md | nota CBBH conservada | [Web-Security/API/security-misconfiguration.md](../../Web-Security/API/security-misconfiguration.md) |
| CBBH/API Attacks/9 - Improper Inventory Management.md | nota CBBH conservada | [Web-Security/API/improper-inventory-management.md](../../Web-Security/API/improper-inventory-management.md) |
| CBBH/Attacking GraphQL/2- Insecure Direct Object Reference (IDOR).md | nota CBBH conservada | [Web-Security/GraphQL/insecure-direct-object-reference-idor.md](../../Web-Security/GraphQL/insecure-direct-object-reference-idor.md) |
| CBBH/BB/Bug bounty.md | nota CBBH conservada | [Methodologies/bug-bounty.md](../../Methodologies/bug-bounty.md) |
| CBBH/BB/Hackerone/7 - Postbook.md | nota CBBH conservada | [Labs-and-Writeups/HackerOne/postbook.md](../../Labs-and-Writeups/HackerOne/postbook.md) |
| CBBH/BB/hackinghub/Client side/Open Redirect.md | nota CBBH conservada | [Web-Security/Browser-Security/hackinghub-client-side-open-redirect.md](../../Web-Security/Browser-Security/hackinghub-client-side-open-redirect.md) |
| CBBH/BB/hackinghub/Client side/RegEx.md | nota CBBH conservada | [Web-Security/Browser-Security/hackinghub-client-side-regex.md](../../Web-Security/Browser-Security/hackinghub-client-side-regex.md) |
| CBBH/BB/hackinghub/Client side/XSS/Blind.md | nota CBBH conservada | [Web-Security/XSS/hackinghub-client-side-xss-blind.md](../../Web-Security/XSS/hackinghub-client-side-xss-blind.md) |
| CBBH/BB/hackinghub/Client side/XSS/Markdown.md | nota CBBH conservada | [Web-Security/XSS/hackinghub-client-side-xss-markdown.md](../../Web-Security/XSS/hackinghub-client-side-xss-markdown.md) |
| CBBH/BB/hackinghub/Local File Read.md | nota CBBH conservada | [Web-Security/Variants/hackinghub-local-file-read.md](../../Web-Security/Variants/hackinghub-local-file-read.md) |
| CBBH/BB/hackinghub/Recon/Google Dorking.md | nota CBBH conservada | [Enumeration/Reconnaissance/hackinghub-recon-google-dorking.md](../../Enumeration/Reconnaissance/hackinghub-recon-google-dorking.md) |
| CBBH/BB/hackinghub/Recon/HTTPx.md | nota CBBH conservada | [Enumeration/Reconnaissance/hackinghub-recon-httpx.md](../../Enumeration/Reconnaissance/hackinghub-recon-httpx.md) |
| CBBH/BB/hackinghub/Recon/Shodan.md | nota CBBH conservada | [Enumeration/Reconnaissance/hackinghub-recon-shodan.md](../../Enumeration/Reconnaissance/hackinghub-recon-shodan.md) |
| CBBH/BB/hackinghub/Recon/Subfinder.md | nota CBBH conservada | [Enumeration/Reconnaissance/hackinghub-recon-subfinder.md](../../Enumeration/Reconnaissance/hackinghub-recon-subfinder.md) |
| CBBH/BB/hackinghub/Recon/gitTools.md | nota CBBH conservada | [Enumeration/Reconnaissance/hackinghub-recon-gittools.md](../../Enumeration/Reconnaissance/hackinghub-recon-gittools.md) |
| CBBH/BB/hackinghub/Reverse Proxy.md | nota CBBH conservada | [Web-Security/Variants/hackinghub-reverse-proxy.md](../../Web-Security/Variants/hackinghub-reverse-proxy.md) |
| CBBH/Owasp top 10/1 - looking glass.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/looking-glass.md](../../Labs-and-Writeups/OWASP-Challenges/looking-glass.md) |
| CBBH/Owasp top 10/10 - baby breaking grad.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/baby-breaking-grad.md](../../Labs-and-Writeups/OWASP-Challenges/baby-breaking-grad.md) |
| CBBH/Owasp top 10/2 - sanitize.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/sanitize.md](../../Labs-and-Writeups/OWASP-Challenges/sanitize.md) |
| CBBH/Owasp top 10/3 - baby auth.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/baby-auth.md](../../Labs-and-Writeups/OWASP-Challenges/baby-auth.md) |
| CBBH/Owasp top 10/6 - bay todo or no todo.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/bay-todo-or-no-todo.md](../../Labs-and-Writeups/OWASP-Challenges/bay-todo-or-no-todo.md) |
| CBBH/Owasp top 10/7 - BoneCheweCon.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/bonechewecon.md](../../Labs-and-Writeups/OWASP-Challenges/bonechewecon.md) |
| CBBH/Owasp top 10/8 - Full Stack Conf.md | nota CBBH conservada | [Labs-and-Writeups/OWASP-Challenges/full-stack-conf.md](../../Labs-and-Writeups/OWASP-Challenges/full-stack-conf.md) |
| CBBH/Study/Authetication.md | nota CBBH conservada | [Labs-and-Writeups/Web-Study/authetication.md](../../Labs-and-Writeups/Web-Study/authetication.md) |
| CBBH/Study/File upload.md | nota CBBH conservada | [Labs-and-Writeups/Web-Study/file-upload.md](../../Labs-and-Writeups/Web-Study/file-upload.md) |
| CBBH/Vulnyx/Jarjar.md | nota CBBH conservada | [Labs-and-Writeups/Vulnyx/jarjar.md](../../Labs-and-Writeups/Vulnyx/jarjar.md) |
| CBBH/Vulnyx/Vulnyx.md | nota CBBH conservada | [Labs-and-Writeups/Vulnyx/vulnyx.md](../../Labs-and-Writeups/Vulnyx/vulnyx.md) |
| pentestNotes/Passwords Attacks/Password crack.md | inventariado; cuerpo no importado | [Password-Attacks/source-catalog.md](../../Password-Attacks/source-catalog.md) |
| pentestNotes/Passwords Attacks/ffuf.md | inventariado; cuerpo no importado | [Password-Attacks/source-catalog.md](../../Password-Attacks/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/AutoEnums.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/CVEs/CUPS - CVE-2012-5519.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/CVEs/DirtyPipe - CVE-2022-0847.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/CVEs/Pwnkit - CVE-2021-4034.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/PHP config files.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Linux/SSH tunneling.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/AlwaysInstallElevated (msiexec-msi file).md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/AutoEnums.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/Commands.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/MS/MS11-046.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/MS/Windows Exploits.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/PowerUp.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/PrivEsc/Windows/SSH Tunnel.md | inventariado; cuerpo no importado | [Privilege-Escalation/source-catalog.md](../../Privilege-Escalation/source-catalog.md) |
| pentestNotes/Readme.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| pentestNotes/Services/3306 - MySQL.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| pentestNotes/Services/389 - LDAP.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| pentestNotes/Shells/PHP cmd.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| pentestNotes/Shells/bash script.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| pentestNotes/Web/API/LFI.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/Command Injections/Command injection.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/LFI/LFI.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/Links.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/NoSQLi.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/Session security/Session security.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/XSS/Reflected.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Web/XSS/Stored.md | inventariado; cuerpo no importado | [Web-Security/source-catalog.md](../../Web-Security/source-catalog.md) |
| pentestNotes/Windows/Net-NTLMv2.md | inventariado; cuerpo no importado | [Password-Attacks/source-catalog.md](../../Password-Attacks/source-catalog.md) |
| pentestNotes/Windows/Responder.md | inventariado; cuerpo no importado | [Windows/source-catalog.md](../../Windows/source-catalog.md) |
| pentestNotes/Windows/SmbFolder.md | inventariado; cuerpo no importado | [Windows/source-catalog.md](../../Windows/source-catalog.md) |
| notes/README.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| notes/active-directory/README.md | inventariado; cuerpo no importado | [Active-Directory/source-catalog.md](../../Active-Directory/source-catalog.md) |
| notes/copy/copy1.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| notes/enumeration/3389-rdp.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| notes/file-transfers/README.md | inventariado; cuerpo no importado | [Network-Pentesting/source-catalog.md](../../Network-Pentesting/source-catalog.md) |
| notes/import.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| notes/password-attacks/linux/README.md | inventariado; cuerpo no importado | [Password-Attacks/source-catalog.md](../../Password-Attacks/source-catalog.md) |
| notes/write-ups/vulnhub/README.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| notes/write-ups/vulnhub/dc-9.md | caso externo inventariado; cuerpo no importado | [Labs-and-Writeups/VulnHub/dc-9.md](../../Labs-and-Writeups/VulnHub/dc-9.md) |
| writeups/Proving Grounds Practice/Linux/Easy/Wombo.md | caso externo inventariado; cuerpo no importado | [Labs-and-Writeups/Proving-Grounds-Practice/Linux/wombo.md](../../Labs-and-Writeups/Proving-Grounds-Practice/Linux/wombo.md) |
| writeups/Proving Grounds Practice/Linux/Intermediate/Marketing.md | caso externo inventariado; cuerpo no importado | [Labs-and-Writeups/Proving-Grounds-Practice/Linux/marketing.md](../../Labs-and-Writeups/Proving-Grounds-Practice/Linux/marketing.md) |
| writeups/Proving Grounds Practice/Windows/Intermediate/Resourced.md | caso externo inventariado; cuerpo no importado | [Labs-and-Writeups/Proving-Grounds-Practice/Windows/resourced.md](../../Labs-and-Writeups/Proving-Grounds-Practice/Windows/resourced.md) |
| writeups/README.md | inventariado; cuerpo no importado | [Resources/source-catalog.md](../source-catalog.md) |
| web/1 - Foothold/HTTP Smuggling/Examples.md | caso externo inventariado; cuerpo no importado | [Labs-and-Writeups/Web-Study-External/http-smuggling-examples.md](../../Labs-and-Writeups/Web-Study-External/http-smuggling-examples.md) |

## Referencias sin resolver

[Referencias originales ambiguas, inexistentes o capturas retenidas](link-review.csv)

## Enlaces externos

Se comprobó la disponibilidad de documentación con una lista limitada de dominios. No se solicitaron URLs dinámicas, IP de ejercicios ni endpoints de aplicación. Los fallos de red y bloqueos HTTP no se etiquetan como enlaces rotos. Dos enlaces de PortSwigger devolvieron 404 a HEAD y se verificaron por lectura de la página oficial: siguen disponibles.

[Resultados individuales](external-links.csv)
