___

![[Pasted image 20241009183717.png]]

uid=15 

![[Pasted image 20241009184106.png]]

# Encoded References

![[Pasted image 20241009184432.png]]

```bash
echo "MQ==" | base64 -d  
1
```

![[Pasted image 20241009184607.png]]

![[Pasted image 20241009184635.png]]

# Insecure APIs

![[Pasted image 20241009185527.png]]

```json
{"uid":"10","uuid":"bfd92386a1b48076792e68b596846499","role":"staff_admin","full_name":"admin","email":"admin@employees.htb","about":"Never gonna give you up, Never gonna let you down"}
```

We can modify other users' details
![[Pasted image 20241009185945.png]]