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

## For finding subdomains
```bash
subfinder -d projectbaseline.com -all -recursive > projectbaseline.txt
```

## For filter out live subdomains
```bash
httpx -l projectbaseline.txt -cl -sc -location -favicon -title -tech-detect -ip -ports 80,443,8000,8080 -o projectbaseline-httpx.txt -follow-redirects
```

```bash
cat projectbaseline.txt | httpx -ports 80,443,8080,8000,8888 -threads 200 > projectbaseline_alive.txt
```

## For fetching passive urls

```bash
katana -u projectbaseline_alive.txt -d 5 -ps -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg > allurls.txt
```



