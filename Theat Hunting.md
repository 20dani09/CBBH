___

# CVE-2024-3400

https://security.paloaltonetworks.com/CVE-2024-3400

The following command can be used from the PAN-OS CLI to help identify if there was an attempted exploit activity on the device:

```bash
grep pattern "failed to unmarshal session(.\+.\/" mp-log gpsvc.log*
```

