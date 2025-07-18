graph TD

  %% Clusters
  subgraph Cluster_prod-cluster
    C1["Cluster: prod-cluster"]
    NS1["Namespace: default"]
    NS2["Namespace: monitoring"]
  end

  C1 --> NS1
  C1 --> NS2

  %% Deployments avec summary inline
  D1["web-app (Pods: 2, Containers: 3, Images: 2)"]
  D2["api-service (Pods: 1, Containers: 1, Images: 1)"]
  D3["prometheus (Pods: 1, Containers: 1, Images: 1)"]

  NS1 --> D1
  NS1 --> D2
  NS2 --> D3
