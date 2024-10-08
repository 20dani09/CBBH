___
> The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag.

![[Pasted image 20240925135308.png]]

> The /admin.php page uses a cookie that has been encoded multiple times. Try to decode the cookie until you get a value with 31-characters. Submit the value as the answer

![[Pasted image 20240925140558.png]]

> Once you decode the cookie, you will notice that it is only 31 characters long, which appears to be an md5 hash missing its last character. So, try to fuzz the last character of the decoded md5 cookie with all alpha-numeric characters, while encoding each request with the encoding methods you identified above. (You may use the "alphanum-case.txt" wordlist from Seclist for the payload)

```bash
/usr/share/seclists/Fuzzing/alphanum-case.txt
```

![[Pasted image 20240925141911.png]]

![[Pasted image 20240925141625.png]]


> You are using the 'auxiliary/scanner/http/coldfusion_locale_traversal' tool within Metasploit, but it is not working properly for you. You decide to capture the request sent by Metasploit so you can manually verify it and repeat it. Once you capture the request, what is the 'XXXXX' directory being called in '/XXXXX/administrator/..'?

The directory traversal vulnerability in older versions of ColdFusion is often exploited by targeting the **CFIDE/administrator** path, which is the administrative interface for ColdFusion. A typical path might look like `/CFIDE/administrator/..` or `/CFIDE/administrator/locale/..`, exploiting improper validation of directory access.

So, the request path would be something like:

```bash
/CFIDE/administrator/.. (followed by traversal attempts)
```
