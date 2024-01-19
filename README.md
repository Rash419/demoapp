# demoapp
This app is created to reproduce mis-balancing in HAproxytech's ingress controller

## Steps to install demoapp
1. Install [HAproxy Ingress Controller](https://github.com/haproxytech/kubernetes-ingress) with Nodeport service type

2. Install demoapp using chart given in [demoapp repository](https://github.com/Rash419/demoapp)
```sh
helm install --create-namespace --namespace demoapp demoapp path/to/chart/given/in/repo
```
