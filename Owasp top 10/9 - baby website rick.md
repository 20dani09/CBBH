___

# Insecure deserialization

![[Pasted image 20241029175340.png]]

Base64 decode

```bash
(dp0  
S'serum'  
p1  
ccopy_reg  
_reconstructor  
p2  
(c__main__  
anti_pickle_serum  
p3  
c__builtin__  
object  
p4  
Ntp5  
Rp6  
s.
```

https://docs.python.org/3/library/pickle.html

Reverse
```python
import pickle  
import pickletools  
import base64  
import os  
  
class anti_pickle_serum(object):  
       def __init__(self):  
               pass  
  
exploit_obj = anti_pickle_serum()  
raw_pickle = pickle.dumps({"serum": exploit_obj}, protocol=0)  
  
optimed_pickle = pickletools.optimize(raw_pickle)  
pickletools.dis(optimed_pickle)  
  
payload= base64.b64encode(raw_pickle)  
print(payload)
```

