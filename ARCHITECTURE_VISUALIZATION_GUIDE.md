# Guide Complet de Visualisation d'Architecture avec NetworkX et Graphviz

## Table des Matières
1. [Prérequis](#prérequis)
2. [Structure de Données Requise](#structure-de-données-requise)
3. [Code de Base](#code-de-base)
4. [Exemples Complets](#exemples-complets)
5. [Personnalisation Avancée](#personnalisation-avancée)
6. [Dépannage](#dépannage)
7. [Bonnes Pratiques](#bonnes-pratiques)
8. [Ressources](#ressources)

## Prérequis

```bash
# Création d'un environnement conda (recommandé)
conda create -n archi-viz python=3.10
conda activate archi-viz
conda install -c conda-forge networkx pygraphviz

# Ou avec pip
pip install networkx pygraphviz
```

## Structure de Données Requise

### Nœuds (Nodes)

| Attribut  | Type       | Description                             | Exemple          |
|-----------|------------|-----------------------------------------|------------------|
| id        | String     | Identifiant unique du nœud (obligatoire) | "web-server-01" |
| type      | String     | Type de composant                       | "vm", "lb", "db" |
| label     | String     | Libellé affiché (optionnel)             | "API Gateway"   |
| tier      | String     | Niveau hiérarchique                     | "edge", "app", "data" |
| cluster   | String     | Groupe logique                          | "DMZ", "K8s-Cluster" |
| critical  | Boolean    | Élément critique                        | true/false       |

### Arêtes (Edges)

| Attribut  | Type    | Description                      | Exemple          |
|-----------|---------|----------------------------------|------------------|
| protocol  | String  | Protocole de communication       | "HTTP/2", "gRPC" |
| port      | Integer | Port de connexion                | 443, 8080        |
| critical  | Boolean | Connexion critique               | true/false       |
| label     | String  | Étiquette optionnelle            | "DB Connection"  |

## Conversion d'un Graphe NetworkX Existant

### Vérification de la Structure

Avant de visualiser, vérifiez les attributs de votre graphe existant :

```python
# Vérifiez les attributs actuels
print("Attributs des nœuds :", next(iter(G.nodes(data=True)))[1].keys())
print("Attributs des arêtes :", next(iter(G.edges(data=True)))[2].keys() if G.edges() else "Pas d'arêtes")
```

### Adaptation des Attributs

Si vos attributs ont des noms différents, utilisez cette fonction de conversion :

```python
def adapt_existing_graph(G_existing):
    """Convertit un graphe existant au format de visualisation."""
    G = nx.DiGraph() if G_existing.is_directed() else nx.Graph()
    
    # 1. Conversion des nœuds
    for node, attrs in G_existing.nodes(data=True):
        new_attrs = {
            "type": attrs.get("node_type", attrs.get("kind", "app")),
            "label": attrs.get("name", attrs.get("label", str(node))),
            "tier": attrs.get("layer", "app"),
            "cluster": attrs.get("group", "default"),
            "critical": attrs.get("is_critical", False)
        }
        G.add_node(node, **new_attrs)
    
    # 2. Copie des arêtes
    for u, v, attrs in G_existing.edges(data=True):
        G.add_edge(u, v, **attrs)
    
    return G

# Utilisation
G_adapted = adapt_existing_graph(votre_graphe_existant)
```

### Exemple Complet

```python
# 1. Charger votre graphe existant
# G_existing = nx.read_graphml("votre_graphe.graphml")

# 2. Adapter le graphe
G_adapted = adapt_existing_graph(G_existing)

# 3. Personnaliser les styles
for n, d in G_adapted.nodes(data=True):
    if d["type"] == "server":
        d["shape"] = "box3d"
        d["fillcolor"] = "#e1f5fe"

# 4. Générer la visualisation
visualize_architecture(G_adapted, "architecture_adaptee.png")
```

### Filtrage des Éléments

Pour les grands graphes, filtrez avant la visualisation :

```python
# Par type
web_servers = [n for n, d in G_adapted.nodes(data=True) if d.get("type") == "web"]
G_filtered = G_adapted.subgraph(web_servers)

# Par attribut personnalisé
critical_nodes = [n for n, d in G_adapted.nodes(data=True) if d.get("critical")]
G_critical = G_adapted.subgraph(critical_nodes)

visualize_architecture(G_critical, "critical_components.png")
```

## Code de Base

```python
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

def visualize_architecture(G, output_file="architecture.png"):
    """
    Convertit un graphe NetworkX en diagramme d'architecture.
    
    Args:
        G: Graphe NetworkX avec attributs
        output_file: Chemin du fichier de sortie (.png, .svg, .pdf)
    """
    # Configuration des styles
    type_to_shape = {
        # Infrastructure
        "vm": "box3d",
        "container": "box",
        "pod": "note",
        "node": "component",
        
        # Réseau
        "lb": "hexagon",
        "gateway": "doubleoctagon",
        "firewall": "house",
        "vlan": "folder",
        "network": "oval",
        
        # Stockage
        "db": "cylinder",
        "storage": "box",
        "cache": "folder",
        
        # Par défaut
        "app": "box",
        "service": "box"
    }
    
    type_to_color = {
        "vm": "#e1f5fe",
        "container": "#e8f5e9",
        "lb": "#fff3e0",
        "db": "#f3e5f5",
        "network": "#e8eaf6",
        "default": "#ffffff"
    }

    # Application des styles aux nœuds
    for n, d in G.nodes(data=True):
        node_type = d.get("type", "")
        
        # Défaut si attributs manquants
        d.setdefault("label", n)
        d.setdefault("style", "rounded,filled")
        d.setdefault("fontname", "Arial")
        d.setdefault("fontsize", "10")
        
        # Style basé sur le type
        d["shape"] = type_to_shape.get(node_type, "box")
        d["fillcolor"] = type_to_color.get(node_type, "#ffffff")
        
        # Mise en évidence des éléments critiques
        if d.get("critical"):
            d["penwidth"] = "2.0"
            d["color"] = "#d32f2f"

    # Configuration des arêtes
    for u, v, d in G.edges(data=True):
        d.setdefault("fontsize", "8")
        d.setdefault("fontname", "Arial")
        if d.get("critical"):
            d["color"] = "#d32f2f"
            d["penwidth"] = "2.0"

    # Création du graphe AGraph
    A = to_agraph(G)
    
    # Configuration globale
    A.graph_attr.update({
        "rankdir": "LR",          # De gauche à droite
        "splines": "ortho",       # Lignes droites
        "nodesep": "0.4",         # Espacement horizontal
        "ranksep": "0.8",         # Espacement vertical
        "fontname": "Arial",
        "fontsize": "12"
    })

    # Organisation en clusters (groupes logiques)
    clusters = {}
    for n, d in G.nodes(data=True):
        if "cluster" in d:
            clusters.setdefault(d["cluster"], []).append(n)
    
    for cluster_name, nodes in clusters.items():
        A.add_subgraph(
            nodes,
            name=f"cluster_{cluster_name}",
            label=cluster_name,
            style="rounded,dashed",
            color="#757575"
        )

    # Organisation hiérarchique (tiers)
    tiers = {}
    for n, d in G.nodes(data=True):
        if "tier" in d:
            tiers.setdefault(d["tier"], []).append(n)
    
    for tier in ["internet", "edge", "app", "data"]:  # Ordre de haut en bas
        if tier in tiers:
            A.add_subgraph(
                tiers[tier],
                name=f"rank_{tier}",
                rank="same"
            )

    # Génération de l'image
    A.layout("dot")
    A.draw(output_file)
    print(f"Diagramme généré : {output_file}")
```

## Exemples Complets

### Exemple 1 : Architecture Web Simple

```python
G = nx.DiGraph()

# Infrastructure
G.add_node("internet", type="cloud", tier="internet", label="Internet")
G.add_node("lb", type="lb", tier="edge", cluster="DMZ", label="Load Balancer")
G.add_node("web1", type="vm", tier="app", cluster="Web", label="Web Server 1")
G.add_node("web2", type="vm", tier="app", cluster="Web", label="Web Server 2")
G.add_node("app", type="app", tier="app", cluster="App", label="Application", critical=True)
G.add_node("db", type="db", tier="data", cluster="Database", label="PostgreSQL")

# Connexions
G.add_edge("internet", "lb", protocol="HTTPS", port=443)
G.add_edge("lb", "web1", protocol="HTTP", port=80)
G.add_edge("lb", "web2", protocol="HTTP", port=80)
G.add_edge("web1", "app", protocol="HTTP", port=3000)
G.add_edge("web2", "app", protocol="HTTP", port=3000)
G.add_edge("app", "db", protocol="PostgreSQL", port=5432, critical=True)

# Génération
visualize_architecture(G, "web_architecture.png")
```

### Exemple 2 : Architecture Microservices

```python
G = nx.DiGraph()

# Services
services = [
    ("api-gateway", "Gateway", "edge"),
    ("auth-service", "Auth", "app"),
    ("user-service", "Users", "app"),
    ("order-service", "Orders", "app"),
    ("payment-service", "Payments", "app"),
    ("notification-service", "Notifications", "app"),
    ("mongodb", "MongoDB", "data"),
    ("redis", "Redis", "data"),
]

for service_id, label, tier in services:
    G.add_node(
        service_id,
        type="service" if "service" in service_id else service_id,
        tier=tier,
        cluster="Microservices",
        label=label,
        critical=(service_id in ["api-gateway", "auth-service"])
    )

# Connexions
connections = [
    ("api-gateway", "auth-service", "gRPC"),
    ("api-gateway", "user-service", "gRPC"),
    ("api-gateway", "order-service", "gRPC"),
    ("order-service", "payment-service", "gRPC"),
    ("order-service", "notification-service", "gRPC"),
    ("auth-service", "redis", "Redis"),
    ("user-service", "mongodb", "MongoDB"),
    ("order-service", "mongodb", "MongoDB"),
]

for src, dst, protocol in connections:
    G.add_edge(src, dst, protocol=protocol)

# Génération
visualize_architecture(G, "microservices_architecture.png")
```

## Personnalisation Avancée

### Styles Personnalisés

```python
type_to_shape.update({
    "kubernetes": "folder",
    "server": "rect",
    "queue": "note",
    "function": "component"
})

type_to_color.update({
    "kubernetes": "#326ce5",
    "server": "#f1f8e9",
    "queue": "#fff0f6",
    "function": "#e6f7ff"
})
```

### Filtrage des Éléments

```python
def filter_graph(G, **filters):
    """Filtre le graphe selon des critères."""
    filtered_nodes = [
        n for n, d in G.nodes(data=True)
        if all(d.get(k) == v for k, v in filters.items())
    ]
    return G.subgraph(filtered_nodes)

# Exemple : Voir uniquement les éléments critiques
critical_view = filter_graph(G, critical=True)
visualize_architecture(critical_view, "critical_components.png")
```

## Dépannage

### Erreur "graphviz/cgraph.h not found"
```bash
# Sur macOS avec Homebrew
brew install graphviz

# Sur Ubuntu/Debian
sudo apt-get install graphviz libgraphviz-dev

# Sur Windows avec Chocolatey
choco install graphviz
```

### Problèmes Courants

1. **Étiquettes tronquées** : Augmentez `nodesep` et `ranksep`
   ```python
   A.graph_attr.update({"nodesep": "0.8", "ranksep": "1.2"})
   ```

2. **Flèches manquantes** : Vérifiez que vous utilisez `DiGraph` et non `Graph`
   ```python
   G = nx.DiGraph()  # Pour les graphes orientés
   ```

3. **Graphe trop grand** : Filtrez ou utilisez `concentrate`
   ```python
   A.graph_attr.update({"concentrate": "true"})
   ```

## Bonnes Pratiques

1. **Hiérarchie** : Utilisez `tier` pour les niveaux logiques
   - `internet` : Points d'entrée externes
   - `edge` : Load balancers, API Gateways
   - `app` : Services applicatifs
   - `data` : Bases de données, caches

2. **Regroupements** : Utilisez `cluster` pour les zones logiques
   - Par équipe : "Team A", "Team B"
   - Par environnement : "Production", "Staging"
   - Par localisation : "EU-West", "US-East"

3. **Cohérence** :
   - Utilisez les mêmes types pour des éléments similaires
   - Gardez une convention de nommage cohérente
   - Documentez vos conventions d'attributs

4. **Performance** :
   - Pour les grands graphes, filtrez avant la visualisation
   - Utilisez des clusters pour simplifier la lecture
   - Évitez les croisements d'arêtes inutiles

## Ressources

- [Documentation NetworkX](https://networkx.org/)
- [Documentation PyGraphviz](https://pygraphviz.github.io/)
- [Guide des attributs Graphviz](https://graphviz.org/doc/info/attrs.html)
- [Formes de nœuds Graphviz](https://graphviz.org/doc/info/shapes.html)

## Licence

Ce document est fourni sous licence MIT. N'hésitez pas à l'adapter à vos besoins.
