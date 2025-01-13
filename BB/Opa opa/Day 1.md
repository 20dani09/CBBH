___

Verily Life Sciences

https://hackerone.com/verily_life_sciences

# Scope

```
https://*.projectbaseline.com/
https://*.signalpath.com/
https://*.onduo.com/
https://*.verily.com/
https://*.granularinsurance.com/
```

```
subfinder -d projectbaseline.com -all -recursive > projectbaseline.txt
```

```
httpx -l projectbaseline.txt -cl -sc -location -favicon -title -tech-detect -ip -ports 80,443,8000,8080 -o projectbaseline-httpx.txt -follow-redirects
```

