{
  "clusters": [
    {
      "name": "prod-cluster",
      "namespaces": ["default", "monitoring"],
      "nodes": ["node-1", "node-2"]
    }
  ],
  "namespaces": [
    {
      "name": "default",
      "parent": "prod-cluster",
      "deployments": ["web-app", "api-service"]
    },
    {
      "name": "monitoring",
      "parent": "prod-cluster",
      "deployments": ["prometheus"]
    }
  ],
  "nodes": [
    {
      "name": "node-1",
      "parent": "prod-cluster",
      "pods": ["web-app-pod-1", "web-app-pod-2"]
    },
    {
      "name": "node-2",
      "parent": "prod-cluster",
      "pods": ["api-pod-1", "prometheus-pod-1"]
    }
  ],
  "deployments": [
    {
      "name": "web-app",
      "parent": "default",
      "pods": ["web-app-pod-1", "web-app-pod-2"]
    },
    {
      "name": "api-service",
      "parent": "default",
      "pods": ["api-pod-1"]
    },
    {
      "name": "prometheus",
      "parent": "monitoring",
      "pods": ["prometheus-pod-1"]
    }
  ],
  "pods": [
    {
      "name": "web-app-pod-1",
      "parent_deployment": "web-app",
      "parent_node": "node-1",
      "containers": ["nginx-1", "sidecar-logger-1"]
    },
    {
      "name": "web-app-pod-2",
      "parent_deployment": "web-app",
      "parent_node": "node-1",
      "containers": ["nginx-2"]
    },
    {
      "name": "api-pod-1",
      "parent_deployment": "api-service",
      "parent_node": "node-2",
      "containers": ["api-1"]
    },
    {
      "name": "prometheus-pod-1",
      "parent_deployment": "prometheus",
      "parent_node": "node-2",
      "containers": ["prometheus-1"]
    }
  ],
  "containers": [
    {
      "name": "nginx-1",
      "parent": "web-app-pod-1",
      "image": "nginx:1.21"
    },
    {
      "name": "sidecar-logger-1",
      "parent": "web-app-pod-1",
      "image": "logger:v2"
    },
    {
      "name": "nginx-2",
      "parent": "web-app-pod-2",
      "image": "nginx:1.21"
    },
    {
      "name": "api-1",
      "parent": "api-pod-1",
      "image": "api-service:v3"
    },
    {
      "name": "prometheus-1",
      "parent": "prometheus-pod-1",
      "image": "prom/prometheus:v2.31"
    }
  ]
}
