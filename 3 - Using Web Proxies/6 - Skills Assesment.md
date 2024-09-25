___
The /lucky.php page has a button that appears to be disabled. Try to enable the button, and then click it to get the flag.

![[Pasted image 20240925135308.png]]

The /admin.php page uses a cookie that has been encoded multiple times. Try to decode the cookie until you get a value with 31-characters. Submit the value as the answer

![[Pasted image 20240925140558.png]]

Once you decode the cookie, you will notice that it is only 31 characters long, which appears to be an md5 hash missing its last character. So, try to fuzz the last character of the decoded md5 cookie with all alpha-numeric characters, while encoding each request with the encoding methods you identified above. (You may use the "alphanum-case.txt" wordlist from Seclist for the payload)

3dac93b8cd250aa8c1a36fffc79a17a