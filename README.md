# demoapp

- This app is created to reproduce mis-balancing in HAproxytech's ingress controller. It only servs `/serverId` endpoint which returns a json with serverId key and a random string which is the unique identifier for that server. For example: `{serverId: ABCDEF}`
- [Ingress object](https://github.com/Rash419/demoapp/blob/9a8c17c00a2606e4becd8e8191874f2b646ee188/chart/values.yaml#L49) of demoapp is configured like following:
    ```yaml
    ingress:
      enabled: true
      className: "haproxy"
      annotations:
        haproxy.org/timeout-tunnel: "3600s"
        haproxy.org/backend-config-snippet: |
          balance url_param RouteToken check_post
      hosts:
        - host: test.demoapp
          paths:
          - path: /serverId
            pathType: Prefix
    ```
- HAproxy is configured to balance based on `url_param RouteToken`

## Steps to install demoapp
1. Install [HAproxy Ingress Controller](https://github.com/haproxytech/kubernetes-ingress) with Nodeport service type

2. Install demoapp using chart given in [demoapp repository](https://github.com/Rash419/demoapp)
    ```sh
    helm install --create-namespace --namespace demoapp demoapp path/to/chart/given/in/repo
    ```

## test-ha.py
- It is simple script that creates a hashmap serverId<->routeToken map. Here routeToken also is random string which signifies to which pod the request should endup. The hope is whenever there is `RouteToken` parameter in url HAproxy should always send the request to appropriate pod.
- For example, If script creates serverid map like following:
    ```sh
    serverId<->routeToken
    ABC<->123
    PQR<->456
    XYZ<->789
    ```
    - Then request with url `http://test.demoapp:30080/serverId?RouteToken=123` should always endup on demoapp pod with `serverId=ABC`. The problem it deosn't happen number when pods are very high for example 50 demoapp pods
- There is function in `test-ha.py` [test_serverid_mismatch](https://github.com/Rash419/demoapp/blob/9a8c17c00a2606e4becd8e8191874f2b646ee188/test-ha.py#L47) which tests the above explain behaviour
- To run the script
  ```sh
  python test-ha.py http://test.demoapp:<whatever-nodeport-you-have-configured>  
  ```
