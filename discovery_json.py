{
  "clusters": [
    { "id": "c1", "name": "prod-cluster", "namespaces": ["ns1", "ns2"], "nodes": ["n1", "n2"] }
  ],
  "namespaces": [
    { "id": "ns1", "name": "default", "parent": "c1", "deployments": ["d1", "d2"] },
    { "id": "ns2", "name": "monitoring", "parent": "c1", "deployments": ["d3"] }
  ],
  "nodes": [
    { "id": "n1", "name": "node-1", "parent": "c1", "pods": ["p1", "p2"] },
    { "id": "n2", "name": "node-2", "parent": "c1", "pods": ["p3", "p4"] }
  ],
  "deployments": [
    { "id": "d1", "name": "web-app", "parent": "ns1", "pods": ["p1", "p2"] },
    { "id": "d2", "name": "api-service", "parent": "ns1", "pods": ["p3"] },
    { "id": "d3", "name": "prometheus", "parent": "ns2", "pods": ["p4"] }
  ],
  "pods": [
    { "id": "p1", "name": "web-app-pod-1", "parent_deployment": "d1", "parent_node": "n1", "containers": ["c1a", "c1b"] },
    { "id": "p2", "name": "web-app-pod-2", "parent_deployment": "d1", "parent_node": "n1", "containers": ["c2a"] },
    { "id": "p3", "name": "api-pod-1", "parent_deployment": "d2", "parent_node": "n2", "containers": ["c3a"] },
    { "id": "p4", "name": "prometheus-pod-1", "parent_deployment": "d3", "parent_node": "n2", "containers": ["c4a"] }
  ],
  "containers": [
    { "id": "c1a", "name": "nginx", "parent": "p1", "image": "nginx:1.21" },
    { "id": "c1b", "name": "sidecar-logger", "parent": "p1", "image": "logger:v2" },
    { "id": "c2a", "name": "nginx", "parent": "p2", "image": "nginx:1.21" },
    { "id": "c3a", "name": "api", "parent": "p3", "image": "api-service:v3" },
    { "id": "c4a", "name": "prometheus", "parent": "p4", "image": "prom/prometheus:v2.31" }
  ]
}
