____

Whenever a new Group Policy Preference (GPP) is created, there’s an xml file created in the SYSVOL share with that config data, including any passwords associated with the GPP. For security, Microsoft AES encrypts the password before it’s stored as `cpassword`. But then Microsoft [published the key](https://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be.aspx) on MSDN!

Microsoft issued a patch in 2014 that prevented admins from putting passwords into GPP. But that patch doesn’t do anything about any of these breakable passwords that were already there, and from what I understand, pentesters still find these regularly in 2018. For more details, check out this [AD Security post](https://adsecurity.org/?p=2288).
## Groups.xml
```
\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\
```


## decrypt

```
gpp-decrypt cpassword
```
