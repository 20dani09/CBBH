___

```bash
curl -X 'GET' 'http://83.136.255.143:38876/api/v1/customers/billing-addresses' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjlAaGFja3RoZWJveC5jb20iLCJleHAiOjE3Mjc4MTE5MTgsImlzcyI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIiLCJhdWQiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIn0.ZoGYhe4DdrqFY6suPzkok45GENZ5_SAzs6mLZ3FUJZdW5XL-fofH5tK863U--j0rnK_qYV-pX4lJgOpaNBNMmQ' | jq | grep -B 1 -A 5 "daa8c984-ba84-4265-8d88-12d6607e511c" | jq
```

![[Pasted image 20241001213955.png]]

