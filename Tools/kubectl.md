# Kubernetes: kubectl y consulta de pods

https://kubernetes.io/docs/reference/ports-and-protocols/

A portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.

https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/kubernetes-basics

https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```


## Consulta de pods

```bash
./kubectl --server https://10.10.11.133:8443  get pod
```
