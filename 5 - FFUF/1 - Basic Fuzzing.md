___

# Directory fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.255.217:55982/FUZZ
```

# Extension fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://83.136.255.217:55982/blog/indexFUZZ
```

# Page fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.255.217:55982/blog/FUZZ.php
```

