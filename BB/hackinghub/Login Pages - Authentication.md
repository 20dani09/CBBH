____

# Weak Passwords

![[Pasted image 20241217114441.png]]

# Default Passwords

Search for "Default credentials" on google

# Username enumeration through errors

Username is invalid

![[Pasted image 20241217120440.png]]
# Username Enumeration Through Forgot Password Function

Invalid username supplied

![[Pasted image 20241217122422.png]]

# Brute Forcing Username and Password

Cluster-bomb

# Self Registration Using Content Discovery

```
ffuf -u https://vdooaly3.eu1.ctfio.com/hidden-registration/FUZZ -w content.txt
```