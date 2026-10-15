____

# Different last character

```bash
python3 -c 'import string; print("\n".join([f"Th4C00lTheacha{c}" for c in string.printable[:-5]]))' > passwords
```

# Custom rockyou

- Contains at least one digit
- Contains at least one lower-case character
- Contains at least one upper-case character
- Contains NO special characters
- Is exactly 12 characters long

```bash
grep -E '^[[:alnum:]]{12}$' rockyou.txt | grep -E '[0-9]' | grep -E '[a-z]' | grep -E '[A-Z]' > wordlist.txt
```
