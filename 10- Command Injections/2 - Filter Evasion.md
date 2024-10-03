___
# Space
A space is a commonly blacklisted character, using `tabs (%09)` instead of spaces

Using the (`$IFS`) Linux Environment Variable may also work since its default value is a space and a tab, which would work between command arguments

`Bash Brace Expansion` feature, which automatically adds spaces between arguments wrapped between braces

```bash
{ls,-la}
```

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space

# Slash (`/`) 

```bash
echo ${PATH:0:1}

/
```

# Semi-colon (`;`)

```shell-session
echo ${LS_COLORS:10:1}

;
```

# Windows backslash (`\`)

```bash
echo %HOMEPATH:~6,-11%

\
```

```bash
$env:HOMEPATH[0]
```