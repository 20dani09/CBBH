___

  
Basic Usage

```
# Basic directory scan - start here!
ffuf -w wordlist.txt -u https://target.com/FUZZ

# Add verbosity for better output (-v)
ffuf -w wordlist.txt -u https://target.com/FUZZ -v

# Multiple extensions - scan for files
ffuf -w wordlist.txt -u https://target.com/FUZZ -e .php,.txt,.html

# Recursion (explores directories it finds)
ffuf -w wordlist.txt -u https://target.com/FUZZ \
     -recursion -recursion-depth 2 -v \
     # Output shows tree structure:
     # /admin/
     # └── /panel.php
     # └── /users/
     #     └── /list.php
```

## Request Customization

```
# Using a saved HTTP request (great for complex APIs!)
# 1. Save request to file (request.txt):
POST /api/v1/users HTTP/1.1
Host: target.com
Content-Type: application/json

{"username": "FUZZ"}

# 2. Use it:
ffuf -request request.txt -w wordlist.txt

# 3. Override parts if needed:
ffuf -request request.txt -w wordlist.txt \
     -H "Host: newdomain.com" \
     -X GET  # Change method
```

## Parameter Discovery (Finding Hidden Inputs)

```
# GET parameters
ffuf -w params.txt -u https://target.com/api?FUZZ=test

# POST parameters
ffuf -w params.txt -u https://target.com/api \
     -X POST -d "FUZZ=test"

# Multiple positions (parameter + value)
ffuf -w params.txt:FUZZ1 -w values.txt:FUZZ2 \
     -u https://target.com/api?FUZZ1=FUZZ2
```

## DNS Fuzzing & Virtual Hosts

```
# Subdomain enumeration
ffuf -w subdomains.txt -u http://FUZZ.example.com

# DNS permutation (app-dev, app-staging, etc)
ffuf -w permutations.txt -u http://app-FUZZ.example.com

# Virtual Host Discovery (finds hidden sites!)
ffuf -w vhosts.txt -u http://target.com \
     -H "Host: FUZZ.target.com"

# Quick vhost check with common values
ffuf -w /dev/null -u http://target.com \
     -H "Host: FUZZ" \
     -w "localhost,127.0.0.1,default,kubernetes,kubernetes.default"
```

Why vhost works: Web servers can host multiple sites on one IP using the Host header. Many staging/admin sites are hidden this way!

## Response Filtering (Essential for Accuracy!)

```
# Size-based (find unique responses)
-fs 1234  # Skip size
-fl 12    # Skip lines
-fw 77    # Skip words

# Status codes
-fc 404,301  # Filter out codes
-mc 200,301  # Match only these codes

# Word count (great for auth bypass)
-fw 57   # Filter word count
-mw 57   # Match word count

# Regex for specific content
-fr "error|forbidden"  # Filter regex
-mr "success|authenticated" # Match regex
```

## Performance & Output Control

```
# Rate limiting (be nice to servers)
-rate 50  # Requests per second
-p 0.1    # Pause between requests

# Save results
-o results.json  # Output file
-of json         # Format (json,csv,etc)

# Quiet mode
-s  # Only show matches
```

## Pro Tips 💡

1. Always start slow (-rate 10) and increase if stable
2. Use -v for better directory structure visualization
3. Combine filters (-mc 200 -fs 123) for accuracy
4. Save complex requests to files for reuse
5. Test filters on known endpoints first
6. Monitor response patterns before setting filters
    
## Common Use Cases

1. API endpoint discovery: -request with JSON body
2. Hidden admin panels: recursion with extensions
3. Bypassing WAFs: careful rate limiting + custom headers
4. Development endpoints: vhost fuzzing with common names



