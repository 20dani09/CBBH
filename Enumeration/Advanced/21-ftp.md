# 21 - FTP

***

| **Command**                                               | **Description**                                                         |
| --------------------------------------------------------- | ----------------------------------------------------------------------- |
| `ftp <FQDN/IP>`                                           | Interact with the FTP service on the target.                            |
| `nc -nv <FQDN/IP> 21`                                     | Interact with the FTP service on the target.                            |
| `telnet <FQDN/IP> 21`                                     | Interact with the FTP service on the target.                            |
| `openssl s_client -connect <FQDN/IP>:21 -starttls ftp`    | Interact with the FTP service on the target using encrypted connection. |
| `wget -m --no-passive ftp://anonymous:anonymous@<target>` | Download all available files on the target FTP server.                  |

## Anonymous login

There are many different security-related settings we can make on each FTP server. These can have various purposes, such as testing connections through the firewalls, testing routes, and authentication mechanisms. One of these authentication mechanisms is the _anonymous_ user. This is often used to allow everyone on the internal network to share files and data without accessing each other's computers.

## Commands

#### FTP Commands

* **USER username** Log in using the specified username.
* **PASS password** Provide the corresponding password for authentication.
* **HELP** The server indicates which commands are supported.
* **PORT 127.0.0.1 0 80** Establish a connection with the IP 127.0.0.1 on port 80. The 5th character is "0", and the 6th character represents the port in decimal or can be used to express the port in hexadecimal.
* **EPRT |2|127.0.0.1|80|** Establish a TCP connection (indicated by "2") with the IP 127.0.0.1 on port 80. This command supports IPv6.
* **LIST** Send the list of files in the current folder.
* **LIST -R** List files recursively (if allowed by the server).
* **APPE /path/something.txt** Store the data received from a passive connection or from a PORT/EPRT connection to a file. If the filename exists, it will append the data.
* **STOR /path/something.txt** Store the data received from a passive connection or from a PORT/EPRT connection to a file. If the file exists, it will be overwritten.
* **STOU /path/something.txt** Store the data received from a passive connection or from a PORT/EPRT connection to a file. If the file exists, it won't do anything.
* **RETR /path/to/file** Establish a passive or a port connection and send the indicated file through that connection.
* **REST 6** Indicate the server that the next time it sends something using RETR, it should start from the 6th byte.
* **TYPE i** Set transfer mode to binary.
* **PASV** Open a passive connection and indicate the user where to connect.
* **PUT /tmp/file.txt** Upload the indicated file to the FTP server.
