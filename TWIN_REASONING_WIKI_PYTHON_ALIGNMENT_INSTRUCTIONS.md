# Instructions de correction — Twin Reasoning Wiki Python
## Alignement avec `nashsu/llm_wiki`

## 1. Objectif
Adapter le projet Python existant pour préserver les mécanismes fonctionnels importants du repo `nashsu/llm_wiki`, sans recopier l'UI desktop ni la stack Tauri/Rust.

Invariant principal :

> **Wiki Markdown = représentation canonique de la connaissance.**
> **Graph = mécanisme actif de retrieval et d'expansion.**
> **Vector index = mécanisme optionnel de découverte sémantique.**
> **Raw = couche de fidélité / preuve originale.**

Le défaut à corriger en priorité est une implémentation où le graphe est seulement visualisé alors que la recherche repose uniquement sur fichiers/JSON.

---

## 2. Rôle du graphe

Le graphe ne doit PAS devenir la source de vérité, mais il ne doit PAS être décoratif.

Pipeline cible :

```text
Query
  ↓
Lexical search
  +
Optional vector search
  ↓
Seed Wiki pages
  ↓
Graph expansion
  ↓
Related Wiki pages
  ↓
Combined ranking
  ↓
Context budget
  ↓
Full relevant Wiki content
  ↓
Agent / LLM
```

Les `[[wikilinks]]`, la provenance partagée et les métadonnées doivent produire les relations du graphe.

Le graphe doit être dérivé et reconstructible depuis le Wiki.

---

## 3. Modèle de pertinence graphe

S'inspirer du modèle 4-signaux du repo de référence :

```text
Direct wikilink       × 3.0
Source overlap        × 4.0
Adamic-Adar           × 1.5
Type affinity         × 1.0
```

Les poids doivent être configurables.

Signaux minimum :
1. lien direct entre pages ;
2. sources Raw communes ;
3. voisins communs ;
4. types/domaines compatibles.

Le but n'est pas de copier exactement l'algorithme TypeScript, mais de préserver le principe de pertinence multi-signaux.

---

## 4. Graph expansion

Après la première recherche :

```text
top K results
   ↓
seed nodes
   ↓
graph_expand(depth <= 2)
   ↓
new candidates
```

Valeurs initiales possibles :

```text
seed   × 1.0
1 hop  × 0.6
2 hops × 0.3
```

Pas d'expansion illimitée.

Exemple attendu :

```text
Query -> Functional Decomposition
              |
              +-> Intent Understanding
              +-> Granularity Principles
              +-> Architecture Reasoning
```

Une page sans correspondance lexicale doit pouvoir apparaître grâce au graphe si sa relation avec une seed page est forte.

---

## 5. Retrieval hybride

Créer un `Knowledge Retrieval Pipeline` unifié :

### Phase 1 — Lexical search
Chercher dans :
- title ;
- tags / metadata ;
- body Wiki ;
- Raw si le mode le permet.

Prévoir un bonus fort sur le titre.

### Phase 1.5 — Vector search optionnelle
Si activée :
- embeddings ;
- semantic similarity ;
- fusion avec les résultats lexicaux.

Si désactivée :
- le système doit continuer à fonctionner avec lexical + graph.

### Phase 2 — Graph expansion
Utiliser les meilleurs résultats comme seeds.

### Phase 3 — Combined ranking
Conceptuellement :

```python
final_score = lexical + vector + graph + metadata
```

Retourner les signaux utilisés afin que le retrieval soit explicable.

### Phase 4 — Context budget
Classer puis sélectionner selon le budget de tokens.

### Phase 5 — Context assembly
Envoyer les pages complètes pertinentes ou les sections significatives, pas seulement des snippets d'embedding.

---

## 6. Vector search non obligatoire

La vectorisation ne doit jamais être obligatoire pour rendre le Wiki utilisable.

```text
vector enabled  -> lexical + vector + graph
vector disabled -> lexical + graph
```

Un expert doit pouvoir modifier un Markdown et continuer à exploiter le Wiki même si l'index vectoriel est absent.

Tout index vectoriel est un **derived index**, jamais la vérité.

---

## 7. Canonical Wiki / indexes dérivés

Ne pas maintenir trois vérités indépendantes :

```text
Markdown
JSON
Graph
```

Architecture correcte :

```text
                 WIKI MARKDOWN
                    canonical
                       |
       +---------------+---------------+
       |               |               |
   metadata         graph index     search/vector
    cache             derived          derived
       |               |               |
       +---------------+---------------+
                       |
                Knowledge Resolver
```

`graph.json`, bases vectorielles et caches doivent pouvoir être supprimés puis reconstruits.

Ajouter au minimum :

```python
rebuild_graph()
rebuild_indexes()
```

---

## 8. `[[wikilinks]]` comme données de graphe

Une page :

```markdown
Voir [[Functional Decomposition]]
et [[Skill Design]].
```

doit créer automatiquement des edges.

Ne pas demander à un humain de maintenir simultanément :
- le Markdown ;
- un JSON de relations.

Le JSON est un cache, pas une vérité.

---

## 9. Provenance et source overlap

Chaque page générée doit conserver ses sources :

```yaml
---
id: functional-decomposition
type: reasoning_pattern
domain: functional-analysis
sources:
  - raw://architecture-guidelines.md#section-4
  - raw://expert-notes.md#functional-decomposition
---
```

Cette provenance sert à :
1. revenir à la preuve originale ;
2. calculer le `source overlap` entre pages ;
3. gérer suppression / mise à jour de sources ;
4. expliquer pourquoi deux pages sont liées.

---

## 10. Wiki-first / Raw escalation

Pour Twin :

```text
Wiki = chemin nominal de raisonnement
Raw  = escalade de fidélité
```

Ne pas interroger systématiquement Wiki + Raw en parallèle.

Descendre au Raw si :

```text
precision_required == high
OR exhaustiveness_required == high
OR decision_impact == high
OR exception_sensitive == true
OR wiki_confidence == low
OR contradiction_detected == true
```

Prévoir également un mode :

```text
sources_only
```

pour répondre exclusivement depuis les sources originales.

---

## 11. Séparer les outils, unifier le resolver

Exposer si utile :

```python
search_wiki(...)
search_raw(...)
search_graph(...)
```

Mais les agents doivent normalement utiliser :

```python
resolve_context(...)
```

Exemple :

```python
resolve_context(
    query=...,
    step=...,
    domain=...,
    reasoning_type=...,
    scope=...,
    entity=...,
    fidelity=...
)
```

Le resolver orchestre lexical, vector, graph et Raw fallback.

---

## 12. Résultat explicable

Exemple de résultat :

```json
{
  "seed_pages": ["functional-decomposition"],
  "expanded_pages": ["incident-reasoning", "historical-analysis"],
  "selected_pages": [
    {
      "id": "historical-analysis",
      "final_score": 0.84,
      "signals": {
        "lexical": 0.10,
        "vector": 0.32,
        "graph": 0.88
      },
      "match_reason": ["2-hop graph expansion"]
    }
  ],
  "raw_evidence": [],
  "conflicts": []
}
```

Il faut pouvoir savoir pourquoi une page est entrée dans le contexte.

---

## 13. `purpose.md`

Conserver un équivalent du `purpose.md` du repo.

Il définit :

```text
WHY
```

Pour Twin :

```text
Twin Reasoning Wiki is the human-readable and evolutive
repository of reasoning principles, rules, methods, patterns,
anti-patterns and contextual reasoning overlays used by Twin.
```

Le Knowledge Compiler et le Resolver doivent tenir compte de `purpose.md`.

---

## 14. `schema.md`

Conserver un fichier distinct :

```text
schema.md = HOW THE WIKI IS MAINTAINED
```

Il définit :
- page types ;
- metadata ;
- structure ;
- naming ;
- ingest rules ;
- conflict policy ;
- linking rules ;
- retrieval conventions.

Ne pas fusionner `purpose.md` et `schema.md`.

---

## 15. `index.md`

Maintenir un catalogue lisible :

```text
page
short description
type/domain
tags if useful
```

Il doit permettre une navigation minimale sans embeddings ni graphe.

---

## 16. `overview.md`

Maintenir une synthèse globale du Wiki.

Utilisations :
- orientation du LLM ;
- compréhension globale ;
- identification de gaps ;
- recherche approfondie.

Ce n'est pas une source de détail.

---

## 17. `log.md`

Maintenir un journal append-only :

```text
## [date] ingest | ...
## [date] update | ...
## [date] conflict | ...
## [date] lint | ...
```

Usage :
- audit ;
- debug ;
- évolution du Wiki.

---

## 18. Ingestion en deux passes

Ne pas faire un seul appel monolithique.

### A. Analysis

Le LLM lit la source et retourne une structure du type :

```json
{
  "key_reasoning_concepts": [],
  "new_rules": [],
  "existing_pages_impacted": [],
  "potential_contradictions": [],
  "contextual_variants": [],
  "suggested_links": [],
  "recommended_updates": []
}
```

### B. Generation / Update

Puis :
- créer / modifier les pages ;
- ajouter wikilinks ;
- mettre à jour provenance ;
- index ;
- overview ;
- reviews ;
- graph index ;
- vector index si activé.

---

## 19. Ingestion incrémentale

Hasher les sources (`SHA256` ou équivalent).

```text
source unchanged -> skip
source changed   -> determine impacted pages -> incremental update
```

Ne pas reconstruire tout le Wiki à chaque ingestion.

---

## 20. Contradictions / Review

Lors d'une ingestion :

```text
new knowledge
     ↓
compare with relevant Wiki knowledge
     ↓
compatible?
contextual variant?
real contradiction?
uncertain?
```

Une contradiction réelle devient un item de Review :

```json
{
  "type": "conflict",
  "status": "unresolved",
  "pages": [],
  "sources": [],
  "reason": "..."
}
```

Le LLM ne doit pas trancher silencieusement un vrai conflit.

Prévoir :

```python
list_reviews()
resolve_review(...)
```

---

## 21. Lint / Wiki health

Ajouter :

```python
lint_wiki()
```

Au minimum :
- broken wikilinks ;
- orphan pages ;
- missing provenance ;
- duplicate / near-duplicate pages ;
- unresolved conflicts ;
- missing metadata ;
- concepts importants mentionnés sans page dédiée ;
- éventuels stale claims.

Le graphe peut aussi aider à détecter les zones faibles.

---

## 22. Graph insights

Pas besoin de reproduire toute l'UI du repo original, mais exposer si possible :

```python
find_orphan_pages()
find_bridge_pages()
find_sparse_areas()
find_surprising_connections()
```

Le graphe sert donc à la fois :
- au retrieval ;
- à la qualité / maintenance du Wiki.

---

## 23. Communautés Louvain

Optionnel pour le premier correctif.

Prévoir cependant la possibilité de détecter des clusters émergents :

```text
Intent reasoning
Functional decomposition
Incident reasoning
Architecture
Skill design
```

Ces communautés complètent les tags explicites ; elles ne les remplacent pas.

---

## 24. Modification humaine first-class

Si un humain édite directement un fichier `wiki/*.md` :

```text
detect change
  ↓
parse metadata + wikilinks
  ↓
update lexical index
  ↓
update graph
  ↓
update embeddings if enabled
```

Le Markdown doit rester directement éditable et immédiatement exploitable.

---

## 25. Suppression de source

Si une source Raw est supprimée :
- retirer cette provenance ;
- réévaluer les pages qu'elle alimentait ;
- conserver les pages encore soutenues par d'autres sources ;
- supprimer les liens morts ;
- mettre à jour index, graph et embeddings.

Ne pas faire de cascade destructive naïve.

---

## 26. API minimale

Exemples :

```text
POST /ingest

POST /search/wiki
POST /search/raw
POST /search/graph
POST /resolve-context

GET  /wiki/pages/{id}
GET  /raw/{id}

GET  /graph
POST /graph/rebuild

GET  /reviews
POST /reviews/{id}/resolve

POST /lint
POST /indexes/rebuild
```

Adapter les noms à l'architecture Python actuelle.

---

## 27. Sémantique Twin

Adapter les types de pages au Twin Reasoning Wiki.

Types recommandés :

```text
reasoning_principle
reasoning_pattern
decision_rule
method
heuristic
anti_pattern
example
contextual_overlay
reasoning_concept
```

Exemple :

```yaml
type: reasoning_pattern
domain: incident_management
reasoning_type: diagnosis
scope: global
entity: all
```

Éviter de calquer uniquement les types génériques `person`, `company`, etc. du repo desktop.

---

## 28. Hors scope : Capability Registry

Ne PAS intégrer ici le Twin Capability Registry.

```text
Twin Reasoning Wiki = HOW SHOULD TWIN REASON?
Twin Capability Registry = WHAT CAN TWIN DO?
```

L'orchestrateur combinera les deux plus tard.

---

## 29. Ordre d'implémentation

### P0 — Audit du repo Python
Avant de coder, produire :
- ce qui existe ;
- ce qui est correct ;
- ce qui manque ;
- ce qui a été mal interprété ;
- composants à conserver ;
- composants à refactorer.

### P1 — Graph-enabled retrieval
Priorité absolue :
- lexical search ;
- vector optional ;
- seed selection ;
- graph expansion ;
- combined ranking ;
- context assembly.

### P2 — Canonical Wiki / derived indexes
Vérifier que Markdown est canonique et JSON/graph/vector rebuildables.

### P3 — Core Wiki files
`purpose.md`, `schema.md`, `index.md`, `overview.md`, `log.md`.

### P4 — Two-step ingest
Analysis puis generation/update + provenance.

### P5 — Review / conflicts / lint

### P6 — Raw escalation / sources-only

### P7 — Communities / advanced graph insights
Seulement après validation du retrieval de base.

---

## 30. Tests obligatoires du graphe

### Test A
- Page A matche fortement la query.
- Page B n'a aucun mot-clé commun.
- B est fortement reliée à A.

Attendu : B apparaît via graph expansion.

### Test B
Graph désactivé.

Attendu : B ne remonte plus, sauf si lexical/vector la trouve.

### Test C
Vector search désactivée.

Attendu : lexical + graph fonctionne toujours.

### Test D
Supprimer `graph.json` / store graph dérivé.

Attendu : `rebuild_graph()` reconstruit un graphe équivalent depuis les pages Wiki.

### Test E
Un humain ajoute :

```markdown
[[New Reasoning Page]]
```

Attendu : edge créé après re-index.

### Test F
Deux pages partagent une source Raw sans wikilink.

Attendu : `source overlap` augmente leur pertinence graphe.

---

## 31. Démonstration fonctionnelle obligatoire

Créer :

```text
Functional Decomposition
Incident Reasoning
Historical Analysis
Topology Analysis
Skill Design
```

Relations :

```text
Functional Decomposition -> Incident Reasoning
Incident Reasoning -> Historical Analysis
Incident Reasoning -> Topology Analysis
```

Query :

```text
How should I decompose the analysis of an operational incident?
```

Attendu :

```text
Functional Decomposition
  -> trouvé par lexical / semantic

Incident Reasoning
  -> trouvé par search + graph

Historical Analysis
  -> ajouté par graph expansion

Topology Analysis
  -> ajouté par graph expansion

Skill Design
  -> exclu car pertinence / budget insuffisant
```

Puis exécuter la même query avec `graph_expansion=false`.

Les résultats doivent être mesurablement différents.

> Si le résultat ne change pas, le graphe reste décoratif et l'implémentation n'est pas conforme.

---

## 32. Ce qu'il ne faut PAS recopier inutilement

Pas besoin de :
- Tauri ;
- React desktop UI ;
- Rust backend ;
- Chrome clipper ;
- gestion de fenêtres ;
- toutes les interactions visuelles du graphe.

À préserver en revanche :
- Raw immutable ;
- Wiki Markdown persistant ;
- provenance ;
- ingest incrémental ;
- ingest en deux passes ;
- wikilinks ;
- graph-assisted retrieval ;
- vector search optionnelle ;
- hybrid ranking ;
- context budgeting ;
- Review ;
- Lint ;
- indexes reconstructibles ;
- human editability.

---

## 33. Invariant final

> **The Twin Reasoning Wiki is a human-readable Markdown knowledge system. Search locates relevant knowledge; the graph expands and contextualizes it; optional embeddings improve semantic discovery; Raw sources provide fidelity. Graph and vector stores are active retrieval mechanisms but remain derived and rebuildable. They never replace the Wiki as the canonical knowledge representation.**
