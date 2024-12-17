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

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/hidden-registration/user_FUZZ -w content.txt
```

![[Pasted image 20241217123723.png]]

## Javascript Files

![[Pasted image 20241217123935.png]]

## APIs

Leaked ``/by-api/api/auth/login/``

![[Pasted image 20241217124748.png]]

# Brute Forcing One-Time Password (OTP)