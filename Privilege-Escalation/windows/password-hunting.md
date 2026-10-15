_____
https://juggernaut-sec.com/password-hunting/


# **Registry Keys**


When autologon is enabled, there is a chance that the password has been stored in cleartext. To find out, we can query winlogon registry key with the following command:

```c
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
```
