____

# Weaponized Exploit for Maltrail v0.53 Unauthenticated OS Command Injection (RCE)

https://github.com/spookier/Maltrail-v0.53-Exploit

## Vulnerability Explanation

[In this specific case,](https://github.com/stamparm/maltrail/blob/master/core/httpd.py#L399) the `username` parameter of the login page doesn't properly sanitize the input, allowing an attacker to inject OS commands

The service uses the `subprocess.check_output()` function to execute a shell command that logs the username provided by the user. If an attacker provides a specially crafted username, they can inject arbitrary shell commands that will be executed on the server

In shell scripting, the semicolon `;` is used to separate multiple commands. So, when the attacker provides a username that includes a semicolon, followed by a shell command, the shell treats everything after the semicolon as a separate command. Basically, everything after `;` will run anyway.

## Exploit Overview

The exploit creates a reverse shell payload encoded in Base64 to bypass potential protections like WAF, IPS or IDS and delivers it to the target URL using a curl command  
The payload is then executed on the target system, establishing a reverse shell connection back to the attacker's specified IP and port
