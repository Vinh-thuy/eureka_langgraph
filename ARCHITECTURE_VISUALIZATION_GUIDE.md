# Guide Complet de Visualisation d'Architecture

## Table des Matières
1. [Présentation](#présentation)
2. [Prérequis](#prérequis)
3. [Structure du Projet](#structure-du-projet)
4. [Utilisation de Base](#utilisation-de-base)
5. [Application Streamlit](#application-streamlit)
6. [Personnalisation Avancée](#personnalisation-avancée)
7. [Exemples Complets](#exemples-complets)
8. [Dépannage](#dépannage)

## Présentation

Ce guide explique comment créer des visualisations d'architecture à partir de graphes NetworkX en utilisant Graphviz, avec une interface web interactive via Streamlit.

## Prérequis

```bash
# Installation des dépendances
pip install networkx graphviz streamlit
```

## Structure du Projet

```
architecture-viz/
├── app.py              # Application Streamlit principale
├── requirements.txt    # Dépendances
└── assets/            # Dossiers pour les ressources
    └── examples/      # Exemples de graphes
```

## Utilisation de Base

### Création d'un Graphe Simple

```python
import networkx as nx

# Initialisation
G = nx.DiGraph()

# Ajout de nœuds avec attributs
G.add_node("web01", 
          type="web", 
          label="Serveur Web", 
          tier="front", 
          cluster="frontend")

# Ajout d'arêtes avec attributs
G.add_edge("web01", "api01", 
          protocol="HTTPS",
          port=443,
          critical=True)
```

### Attributs des Nœuds

| Attribut | Type    | Description                    | Exemple          |
|----------|---------|--------------------------------|------------------|
| type     | String  | Type du composant             | "web", "db", "app"|
| label    | String  | Libellé affiché               | "API Gateway"    |
| tier     | String  | Niveau dans l'architecture    | "front", "middle", "back" |
| cluster  | String  | Groupe logique                | "frontend", "backend" |

### Attributs des Arêtes

| Attribut | Type    | Description                    | Exemple          |
|----------|---------|--------------------------------|------------------|
| protocol | String  | Protocole de communication    | "HTTP/2", "gRPC" |
| port     | Integer | Port de connexion             | 443, 8080        |
| critical | Boolean | Connexion critique            | true/false       |

## Application Streamlit

### Fichier `app.py`

```python
import streamlit as st
import networkx as nx
import graphviz
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Visualisateur d'Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction de visualisation
def visualize_networkx_graph(G, output_file="architecture"):
    # Configuration du graphe
    dot = graphviz.Digraph(
        comment='Architecture',
        format='svg',
        graph_attr={
            'rankdir': 'LR',
            'splines': 'ortho',
            'nodesep': '0.4',
            'ranksep': '0.8',
            'fontname': 'Arial'
        },
        node_attr={
            'shape': 'box',
            'style': 'rounded,filled',
            'fontname': 'Arial',
            'fontsize': '10'
        },
        edge_attr={
            'fontname': 'Arial',
            'fontsize': '8',
            'labelfloat': 'true',
            'decorate': 'true'
        }
    )
    
    # Styles par type de nœud
    type_to_shape = {
        "web": "ellipse",
        "app": "box",
        "db": "cylinder",
        "lb": "hexagon",
        "gateway": "diamond"
    }
    
    type_to_fill = {
        "web": "#e0f3ff",
        "app": "#e8ffe8",
        "db": "#fff2cc",
        "lb": "#f0f0f0",
        "gateway": "#f3e0ff"
    }
    
    # Création des clusters
    clusters = {}
    for node, attrs in G.nodes(data=True):
        if 'cluster' in attrs:
            cluster_name = attrs['cluster']
            clusters.setdefault(cluster_name, []).append(node)
    
    # Ajout des nœuds aux clusters
    for cluster_name, node_ids in clusters.items():
        with dot.subgraph(name=f'cluster_{cluster_name}') as c:
            c.attr(
                label=cluster_name,
                style='rounded,dashed',
                color='#cccccc',
                fontsize='10'
            )
            for node_id in node_ids:
                attrs = G.nodes[node_id]
                node_type = attrs.get('type', '')
                c.node(
                    str(node_id),
                    label=attrs.get('label', str(node_id)),
                    shape=type_to_shape.get(node_type, 'box'),
                    fillcolor=type_to_fill.get(node_type, '#eeeeee')
                )
    
    # Ajout des nœuds hors cluster
    for node, attrs in G.nodes(data=True):
        if 'cluster' not in attrs:
            node_type = attrs.get('type', '')
            dot.node(
                str(node),
                label=attrs.get('label', str(node)),
                shape=type_to_shape.get(node_type, 'box'),
                fillcolor=type_to_fill.get(node_type, '#eeeeee')
            )
    
    # Ajout des arêtes
    for u, v, attrs in G.edges(data=True):
        edge_attrs = {
            'xlabel': attrs.get('protocol', ''),
            'fontsize': '8',
            'penwidth': '2' if attrs.get('critical') else '1',
            'color': '#cc0000' if attrs.get('critical') else '#888888'
        }
        dot.edge(str(u), str(v), **{k: v for k, v in edge_attrs.items() if v})
    
    # Organisation par niveau (tier)
    tiers = {}
    for node, attrs in G.nodes(data=True):
        if 'tier' in attrs:
            tier = attrs['tier']
            tiers.setdefault(tier, []).append(node)
    
    for tier, nodes in tiers.items():
        with dot.subgraph() as s:
            s.attr(rank='same')
            for node in nodes:
                s.node(str(node))
    
    # Génération du fichier
    dot.render(output_file, cleanup=True)
    return f"{output_file}.svg"

# Interface utilisateur
st.title("🖥️ Visualisateur d'Architecture")

# Éditeur de code pour le graphe
graph_code = st.text_area(
    "Définissez votre graphe NetworkX",
    height=300,
    help="Utilisez la syntaxe NetworkX pour définir votre architecture"
)

# Bouton de génération
if st.button("Générer le diagramme", type="primary"):
    try:
        # Exécution du code
        local_vars = {}
        exec(graph_code, {"nx": nx}, local_vars)
        G = local_vars.get('G')
        
        if G and isinstance(G, (nx.Graph, nx.DiGraph)):
            # Génération du diagramme
            output_file = visualize_networkx_graph(G)
            
            # Affichage
            with open(output_file, 'r') as f:
                svg = f.read()
                st.components.v1.html(
                    f"""
                    <div style="width: 100%; overflow: auto;">
                        {svg}
                    </div>
                    """,
                    height=600
                )
                
            # Téléchargement du SVG
            with open(output_file, 'rb') as f:
                st.download_button(
                    label="Télécharger le SVG",
                    data=f,
                    file_name="architecture.svg",
                    mime="image/svg+xml"
                )
        else:
            st.error("Aucun graphe NetworkX valide n'a été trouvé dans le code.")
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

# Exemple dans la barre latérale
with st.sidebar:
    st.header("Aide")
    st.markdown("""
    ### Exemple de graphe
    ```python
    import networkx as nx
    
    G = nx.DiGraph()
    G.add_node("web", type="web", label="Serveur Web", tier="front")
    G.add_node("api", type="app", label="API", tier="middle")
    G.add_edge("web", "api", protocol="HTTPS")
    ```
    """)
```

## Personnalisation Avancée

### Ajouter des Types de Nœuds

```python
type_to_shape = {
    "web": "ellipse",
    "app": "box",
    "db": "cylinder",
    "queue": "folder",
    "cache": "doublecircle",
    "gateway": "diamond"
}

type_to_fill = {
    "web": "#e0f3ff",
    "app": "#e8ffe8",
    "db": "#fff2cc",
    "queue": "#ffe0e0",
    "cache": "#fff0f5",
    "gateway": "#f3e0ff"
}
```

### Styles des Arêtes

```python
edge_attrs = {
    'xlabel': attrs.get('protocol', ''),
    'fontsize': '8',
    'penwidth': '2' if attrs.get('critical') else '1',
    'color': '#cc0000' if attrs.get('critical') else '#888888',
    'fontcolor': '#333333',
    'arrowsize': '0.8'
}
```

## Exemples Complets

### Architecture Microservices

```python
G = nx.DiGraph()

# Frontend
G.add_node("cdn", type="gateway", label="CDN", tier="front", cluster="frontend")
G.add_node("lb", type="lb", label="Load Balancer", tier="front", cluster="frontend")

# Services
services = ["users", "products", "orders", "auth"]
for svc in services:
    G.add_node(f"svc_{svc}", type="app", label=f"Service {svc.capitalize()}", tier="middle", cluster="backend")

# Bases de données
G.add_node("db_primary", type="db", label="PostgreSQL", tier="back", cluster="database")
G.add_node("cache", type="cache", label="Redis", tier="back", cluster="database")

# Connexions
G.add_edge("cdn", "lb", protocol="HTTPS")
G.add_edge("lb", "svc_users", protocol="HTTP/2")
G.add_edge("lb", "svc_products", protocol="HTTP/2")
G.add_edge("lb", "svc_orders", protocol="HTTP/2")
G.add_edge("lb", "svc_auth", protocol="HTTP/2")

for svc in services:
    G.add_edge(f"svc_{svc}", "db_primary", protocol="SQL")
    G.add_edge(f"svc_{svc}", "cache", protocol="TCP")
```

## Dépannage

### Problèmes Courants

1. **Graphviz non trouvé**
   ```bash
   # Sur macOS
   brew install graphviz
   
   # Sur Ubuntu/Debian
   sudo apt-get install graphviz
   ```

2. **Erreurs de rendu**
   - Vérifiez les noms des attributs
   - Assurez-vous que tous les nœuds référencés existent

3. **Problèmes de performance**
   - Limitez le nombre de nœuds à quelques centaines
   - Utilisez `splines="ortho"` pour de meilleures performances

### Améliorations Possibles

1. Ajouter l'export en PNG/PDF
2. Implémenter le glisser-déposer des nœuds
3. Ajouter la sauvegarde/chargement de configurations
4. Intégrer avec des outils comme Prometheus pour des métriques en temps réel

## Conclusion

Ce guide fournit une base solide pour créer des visualisations d'architecture professionnelles. N'hésitez pas à personnaliser les styles et les fonctionnalités selon vos besoins spécifiques.

Pour toute question ou problème, consultez la documentation de [NetworkX](https://networkx.org/) et [Graphviz](https://graphviz.org/).

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
