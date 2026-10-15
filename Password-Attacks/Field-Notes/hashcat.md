____

Example

Hash: abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f

{firstname}_{firstname backwards}_{randomly generated integer between 1 and 1,000,000,000}


```bash
# determine the hash type, one hash at a time due to the password format  
hashcat -a 3 hash 'susan_nasus_?d?d?d?d?d?d?d?d?d'  
  
# cracking the password (only showing the user that helped privilege escalation)  
hashcat -a 3 -m 1400 hash 'susan_nasus_?d?d?d?d?d?d?d?d?d'
```

- The hash type is specified as SHA-256 (`-m 1400`).
- The attack pattern `"susan_nasus_?d?d?d?d?d?d?d?d?d"` indicates that the password starts with "susan_nasus_" followed by 9 digits.
