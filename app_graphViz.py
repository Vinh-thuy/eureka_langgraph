import streamlit as st
import yaml
from graphviz import Digraph

st.set_page_config(page_title="Kubernetes Visualizer", page_icon="☸️", layout="wide")
st.title("Visualisation d'un cluster Kubernetes (YAML local)")

# Lecture du fichier YAML local
with open("k8s_example.yaml", "r") as f:
    docs = list(yaml.safe_load_all(f))

# Extraction clusters/namespaces/pods/deployments
namespaces = {}
deployments = {}
pods = {}
for doc in docs:
    if not isinstance(doc, dict):
        continue
    kind = doc.get('kind', '')
    meta = doc.get('metadata', {})
    ns_name = meta.get('namespace', meta.get('name', 'default'))
    if kind == 'Namespace':
        namespaces[meta.get('name', '')] = True
    elif kind == 'Deployment':
        dep_name = meta.get('name', '')
        dep_ns = meta.get('namespace', 'default')
        deployments.setdefault(dep_ns, []).append(dep_name)
    elif kind == 'Pod':
        pod_name = meta.get('name', '')
        pod_ns = meta.get('namespace', 'default')
        pods.setdefault(pod_ns, []).append(pod_name)

# Création du graphe (MCE : ensembles imbriqués, pas de flèches)
if namespaces:
    dot = Digraph(comment="Kubernetes Architecture", format='png')
    dot.attr(compound='true')
    dot.attr('node', style='filled', color='white')
    # Cluster principal
    with dot.subgraph(name='cluster_main') as c:
        c.attr(label='Cluster', color='lightblue', style='filled', bgcolor='aliceblue')
        for ns in namespaces:
            ns_id = f'ns_{ns}'
            with c.subgraph(name=f'cluster_{ns}') as ns_sub:
                ns_sub.attr(label=f'Namespace {ns}', color='grey90', style='filled', bgcolor='whitesmoke')
                # Deployments
                for dep in deployments.get(ns, []):
                    dep_id = f'dep_{ns}_{dep}'
                    ns_sub.node(dep_id, dep, shape='component', color='orange', style='filled', fillcolor='orange')
                # Pods
                for pod in pods.get(ns, []):
                    pod_id = f'pod_{ns}_{pod}'
                    ns_sub.node(pod_id, pod, shape='component', color='deepskyblue', style='filled', fillcolor='white')
    st.graphviz_chart(dot)
else:
    st.warning("Aucune ressource Namespace trouvée dans le YAML.")

st.caption("Créé avec ❤️ et Python | Visualisation directe du YAML Kubernetes")
