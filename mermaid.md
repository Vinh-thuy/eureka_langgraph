Écris un script Python qui interroge un graphe NetworkX représentant une architecture Kubernetes.
Les nœuds du graphe contiennent les types suivants : Cluster, Namespace, Deployment, Pod, Container, Image.
Les arêtes représentent les relations :
	•	asNamespace (Cluster ➔ Namespace)
	•	asDeployment (Namespace ➔ Deployment)
	•	asPod (Deployment ➔ Pod)
	•	asContainer (Pod ➔ Container)
	•	asImage (Container ➔ Image).

Le script doit :

1️⃣ Identifier tous les clusters présents.
2️⃣ Pour chaque cluster, lister les namespaces qui lui sont associés.
3️⃣ Pour chaque namespace, lister les deployments qui lui sont associés.
4️⃣ Pour chaque deployment, calculer :
	•	le nombre de pods associés,
	•	le nombre de containers associés à ces pods,
	•	le nombre d’images distinctes utilisées par ces containers.

Générer en sortie un diagramme Mermaid au format graph TD, en respectant les règles suivantes :
	•	Chaque Cluster est représenté comme un subgraph intitulé Cluster_<cluster_name>.
	•	Chaque Namespace est représenté par un nœud Namespace: <namespace_name>.
	•	Les liens Cluster ➔ Namespace et Namespace ➔ Deployment sont explicites (-->).
	•	Pour chaque Deployment, afficher les métriques sous forme compacte dans le label du nœud, par exemple :
web-app (Pods: 2, Containers: 3, Images: 2).
	•	Ne pas afficher les Pods, Containers ni Images individuellement : uniquement des comptages agrégés sous forme d’attributs textuels dans le nœud Deployment.

La sortie attendue du script doit être une chaîne de caractères contenant le code Mermaid prêt à être utilisé.

🔹 Contrainte supplémentaire :
	•	Le code doit être propre, lisible, bien structuré et prêt à être intégré dans une application Python existante.
	•	Tu peux utiliser des structures f-string Python pour formater dynamiquement les labels Mermaid.
