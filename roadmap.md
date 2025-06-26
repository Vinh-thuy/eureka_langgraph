# 🚀 Initiative 1 : Analyse et optimisation de l’existant
> Objectif : Comprendre et fiabiliser les données disponibles dans le Knowledge Graph existant et améliorer les flux de synchronisation.

## 🧩 Epic 1.1 : Cartographie du Knowledge Graph actuel
- Objectif : Identifier les objets présents, leurs sources et les relations existantes.

### ✅ User Story 1.1.1 : Auditer la structure du Knowledge Graph
- En tant que : Architecte IT
- Je veux : Visualiser les types de nœuds, les relations et leur volume
- Afin de : Identifier les zones de faiblesse ou de redondance
- Critères d’acceptation :
  - Les types de nœuds sont listés avec leur volumétrie
  - Les principales relations sont représentées graphiquement

### ✅ User Story 1.1.2 : Identifier les sources de données de chaque objet
- En tant que : Data steward
- Je veux : Connaître la provenance des données (ServiceNow, BMC, etc.)
- Afin de : Qualifier la fiabilité de chaque objet
- Critères d’acceptation :
  - Chaque type d’objet est associé à une ou plusieurs sources identifiées

## 🧩 Epic 1.2 : Optimisation des flux de synchronisation
- Objectif : Réduire les redondances et les écarts entre les sources

### ✅ User Story 1.2.1 : Visualiser les écarts entre données CMDB et Discovery
- En tant que : Exploitant
- Je veux : Voir les différences entre les données déclaratives et les données scannées
- Afin de : Prendre des décisions sur les synchronisations futures
- Critères d’acceptation :
  - Un tableau met en évidence les écarts majeurs pour un périmètre applicatif donné

---

# 💬 Initiative 2 : Enrichissement et interaction avec la simulation

## 🧩 Epic 2.1 : Intégration d’un chatbot agentique (Eureka)
- Objectif : Permettre aux utilisateurs d’interroger le graphe et les simulations

### ✅ User Story 2.1.1 : Paramétrer Eureka pour interroger le graphe
- En tant que : Utilisateur IT
- Je veux : Poser des questions comme "Quels serveurs sont obsolètes ?"
- Afin de : Obtenir des réponses immédiates sans requête technique
- Critères d’acceptation :
  - Eureka répond correctement à des questions sur la structure du graphe

## 🧩 Epic 2.2 : Tests de raisonnement avec LangGraph + LangChain
- Objectif : Simuler des scénarios métier avec des agents

### ✅ User Story 2.2.1 : Définir un flux de raisonnement pour une obsolescence
- En tant que : Responsable production
- Je veux : Simuler l’impact d’un plan de décommissionnement
- Afin de : Prioriser les actions correctives
- Critères d’acceptation :
  - Une simulation est lancée à partir de données d’un sous-graphe

---

# 🌐 Initiative 3 : Construction du Knowledge Graph global

## 🧩 Epic 3.1 : Fusion des axes Organisation et Documentation
- Objectif : Ajouter les graphes "Organisation" et "Documents" à la base centrale

### ✅ User Story 3.1.1 : Ingestion du graphe organisationnel (Insight Booster)
- En tant que : Responsable transformation
- Je veux : Avoir une vision des entités et comités liés aux applications
- Afin de : Comprendre les liens entre gouvernance et infrastructure
- Critères d’acceptation :
  - Chaque application est liée à une ou plusieurs entités métier

### ✅ User Story 3.1.2 : Indexer les documents avec leurs topiques
- En tant que : Utilisateur expert
- Je veux : Rechercher des indicateurs ou décisions dans les CR de comités
- Afin de : Accéder plus rapidement à la connaissance décisionnelle
- Critères d’acceptation :
  - Chaque document est indexé avec les entités, dates et topiques pertinents

## 🧩 Epic 3.2 : Mise en place de la gouvernance et des dashboards
- Objectif : Structurer l’exploitation opérationnelle du graphe

### ✅ User Story 3.2.1 : Définir les règles de gouvernance du graphe
- En tant que : Product Owner
- Je veux : Définir les responsables, fréquences de mise à jour, règles de qualité
- Afin de : Garantir la cohérence et la pérennité du graphe
- Critères d’acceptation :
  - Un document de gouvernance est validé et partagé avec les parties prenantes

### ✅ User Story 3.2.2 : Construire un dashboard de couverture des données
- En tant que : Manager IT
- Je veux : Visualiser la couverture, la fraîcheur et la complétude des données
- Afin de : Piloter les actions de fiabilisation
- Critères d’acceptation :
  - Le dashboard présente un taux de complétude par domaine et par source



  # 🌱 Initiative 1 : Fiabiliser et valoriser l’existant (Quick Wins analytiques)
> Objectif : Apporter rapidement des visualisations et insights tangibles à partir des données du Knowledge Graph actuel, en exploitant la data science légère et l’analyse structurelle.

## 🧩 Epic 1.1 : Cartographie des objets & relations du graphe (démo possible semaine 2-3)
- 🎯 But : Offrir une première vision consolidée et visuelle du patrimoine data.
- 🧪 Démo attendue : interface graphique montrant les objets et leurs relations.

### ✅ User Story 1.1.1 : Inventorier les types d’objets et leurs sources
### ✅ User Story 1.1.2 : Afficher un graphe interactif par domaine (infra, app, orga)
### ✅ User Story 1.1.3 : Isoler les nœuds orphelins ou sans relation fiable

## 🧩 Epic 1.2 : Analyse des écarts entre CMDB et données scannées
- 🎯 But : Démontrer l’intérêt immédiat du croisement de sources via un scoring de cohérence.
- 🧪 Démo attendue : tableau de bord montrant les écarts de vérité entre ServiceNow et Discovery.

### ✅ User Story 1.2.1 : Rapprocher les assets techniques scannés et déclarés
### ✅ User Story 1.2.2 : Proposer un score de confiance par objet
### ✅ User Story 1.2.3 : Représenter les écarts visuellement (répartition, % de couverture)

---

# 🤖 Initiative 2 : Interaction intelligente et raisonnement agentique
> Objectif : Apporter une brique innovante visible : permettre aux utilisateurs de dialoguer avec le graphe et d’obtenir des réponses via IA.

## 🧩 Epic 2.1 : Chatbot raisonneur (PoC démontrable dès fin Epic)
- 🎯 But : Montrer une première interaction agentique via Eureka ou autre framework LLM.
- 🧪 Démo attendue : chat permettant de poser des questions comme « quels serveurs critiques sont obsolètes ? »

### ✅ User Story 2.1.1 : Activer l’agent Eureka et le connecter au graphe infra
### ✅ User Story 2.1.2 : Ajouter des cas métiers simples préconfigurés
### ✅ User Story 2.1.3 : Journaliser les interactions et scores de réponse

## 🧩 Epic 2.2 : Simulation ciblée avec LangGraph (démo scénarisée)
- 🎯 But : Montrer qu’on peut simuler l’effet d’une action (ex : suppression d’un serveur ou changement de config).
- 🧪 Démo attendue : scénario type « que se passe-t-il si je retire ce serveur ? »

### ✅ User Story 2.2.1 : Préparer un scénario simulable avec données réelles
### ✅ User Story 2.2.2 : Intégrer le raisonnement dans une boucle LangGraph
### ✅ User Story 2.2.3 : Générer une narration de l’impact en langage naturel

---

# 🧠 Initiative 3 : Structuration organisationnelle & gouvernance
> Objectif : Livrer rapidement une vision exploitable du lien entre gouvernance, documentation, et infrastructure – utile pour la gestion des risques, de la conformité ou des projets de transformation.

## 🧩 Epic 3.1 : Graphe Organisation & Insight Booster
- 🎯 But : Visualiser quels comités, entités ou projets pilotent chaque domaine applicatif.
- 🧪 Démo attendue : graphe interactif avec les comités, leurs topiques, les indicateurs associés.

### ✅ User Story 3.1.1 : Ingestion de la structure organisationnelle
### ✅ User Story 3.1.2 : Croisement avec les applications & responsabilités
### ✅ User Story 3.1.3 : Construction d’un graphe Gouvernance → Comités → App

## 🧩 Epic 3.2 : Gouvernance des données du graphe
- 🎯 But : Définir un cadre dès maintenant pour pérenniser les briques livrées.
- 🧪 Démo attendue : dashboard de qualité des données + règles de gouvernance partagées

### ✅ User Story 3.2.1 : Suivi de la complétude et de la fraîcheur des données
### ✅ User Story 3.2.2 : Mise en place d’un dictionnaire technique de graphe
### ✅ User Story 3.2.3 : Publication d’un contrat de gouvernance des objets clés

---

# 💡 Principes agiles de la roadmap

- 🔁 Chaque Epic se termine par une valeur démontrable (demo, prototype, analyse exploitable).
- 🧪 Les user stories sont pensées pour être livrées rapidement (<2 semaines si possible).
- 🚩 Les initiatives ne sont pas en cascade : elles peuvent évoluer en parallèle avec une montée en complexité progressive.
- 👥 Les feedbacks utilisateurs (IT, data, gouvernance) sont intégrés à chaque étape pour ajuster la suite.



# 🚀 Initiative 1 : Interaction intelligente et démonstrateur Eureka
> Objectif : Offrir dès les premières semaines une capacité visible d’interaction avec les données du graphe via LLM, intégrée à l’outil Domino. Cette initiative est la vitrine du projet, soutenant les premiers cas d’usage concrets.

## 🧩 Epic 1.1 : Démonstrateur Eureka connecté au graphe
- 🎯 Cible : Permettre à l’utilisateur de poser une question métier et d’obtenir une réponse issue du graphe.
- 🧪 Démo cible : "Quels serveurs critiques sont obsolètes ?" → réponse affichée dans Eureka.

### ✅ User Story 1.1.1 : Connexion initiale de Eureka à LangGraph
### ✅ User Story 1.1.2 : Sélection d’un sous-graphe d’expérimentation (ex : obsolescence applicative)
### ✅ User Story 1.1.3 : Affichage d’un raisonnement interprétable par l’utilisateur

## 🧩 Epic 1.2 : Scénarios pilotés par LangChain
- 🎯 Cible : Injecter des cas de simulation ou d’analyse enrichie pilotés par agents.
- 🧪 Démo cible : simulation de l’impact d’un changement dans une infrastructure donnée

### ✅ User Story 1.2.1 : Création d’un scénario de changement (ex : migration serveur)
### ✅ User Story 1.2.2 : Interfaçage Eureka ↔ LangChain ↔ Graphe
### ✅ User Story 1.2.3 : Présentation de la chaîne de raisonnement dans Domino

---

# 🧠 Initiative 2 : Cartographie et fiabilisation du graphe actuel
> Objectif : Analyser et visualiser les données du graphe existant pour assurer à la fois une qualité exploitable et une base de vérité consolidée.

## 🧩 Epic 2.1 : Analyse structurée du graphe existant
- 🎯 Cible : Comprendre ce qui est déjà modélisé, quelles sont les sources et la couverture.
- 🧪 Démo cible : vue graphique complète des types d’objets, leur volumétrie et origine.

### ✅ User Story 2.1.1 : Extraction du schéma actuel (types, relations, sources)
### ✅ User Story 2.1.2 : Visualisation de sous-graphes par périmètre (infrastructure, orga…)
### ✅ User Story 2.1.3 : Mise en évidence des nœuds orphelins, doublons ou incohérences

## 🧩 Epic 2.2 : Alignement des données Discovery et CMDB
- 🎯 Cible : Croiser données déclaratives et scannées pour fiabiliser la connaissance
- 🧪 Démo cible : dashboard montrant les écarts de vérité et un score de confiance

### ✅ User Story 2.2.1 : Rapprocher les objets (serveurs, équipements, applis) entre Discovery et CMDB
### ✅ User Story 2.2.2 : Définir un score de fiabilité par objet
### ✅ User Story 2.2.3 : Afficher un tableau de couverture et d’écarts

---

# 📊 Initiative 3 : Gouvernance & structuration du graphe élargi
> Objectif : Poser les fondations pour intégrer de nouvelles dimensions (organisation, documentation) tout en instaurant les premiers outils de gouvernance.

## 🧩 Epic 3.1 : Ajout de l’axe Organisation (Insight Booster)
### ✅ User Story 3.1.1 : Ingestion des entités, équipes, comités
### ✅ User Story 3.1.2 : Liaison applications ↔ responsables ↔ comités

## 🧩 Epic 3.2 : Gouvernance du graphe
### ✅ User Story 3.2.1 : Définition des règles de fraîcheur, complétude et traçabilité
### ✅ User Story 3.2.2 : Mise en place d’un tableau de pilotage qualité

---

# 🔁 Synthèse agile et incrémentale

| Sprint | Livrable démo                                | Axe principal         |
|--------|-----------------------------------------------|------------------------|
| S1     | Eureka répond à une question simple (obsolescence) | Interaction intelligente |
| S2     | Visualisation des objets du graphe et de leur couverture | Analyse graphe         |
| S3     | Premier scénario LangGraph avec simulation    | Interaction + simulation |
| S4     | Écarts Discovery vs CMDB avec score visible   | Fiabilisation données  |
| S5     | Ajout de l’axe organisation dans le graphe    | Structuration          |


# 🛰️ Initiative 4 : Alignement des données déclaratives et observées (Discovery vs CMDB)
> Objectif : Établir une base de vérité fiable pour les topologies d’infrastructure à partir de Discovery et de ServiceNow, avec validation par les équipes techniques.

## 🧩 Epic 4.1 : Cartographie des capacités Discovery sur l’infra cible
- 🎯 Cible : Savoir ce qu’on peut vraiment scanner sur les zones IaaS, DMZR, virtualisation, appliances, etc.
- 🧪 Démo attendue : tableau ou graphe de couverture avec niveau de précision atteint.

### ✅ User Story 4.1.1 : Identifier les domaines techniques couverts par Discovery
### ✅ User Story 4.1.2 : Identifier les zones non couvertes (ou non scannables)
### ✅ User Story 4.1.3 : Produire une carte des types d’objets détectés + fréquence de mise à jour

## 🧩 Epic 4.2 : Validation terrain avec les équipes (APS, Exploitants, Experts)
- 🎯 Cible : Faire valider que la topologie observée est représentative du réel.
- 🧪 Démo attendue : rapport d’écarts et validation explicite (ou rejet) par les équipes terrain.

### ✅ User Story 4.2.1 : Comparer la topologie scannée avec les vues métiers
### ✅ User Story 4.2.2 : Organiser des ateliers de validation avec les équipes (APS, architectes)
### ✅ User Story 4.2.3 : Produire un "score de vérité" par périmètre ou par type d’objet

## 🧩 Epic 4.3 : Réconciliation CMDB / Discovery dans le graphe de vérité
- 🎯 Cible : Injecter les objets issus de Discovery dans le Knowledge Graph en les marquant comme "observés" vs "déclarés".
- 🧪 Démo attendue : graphe enrichi avec distinction des objets déclarés / observés.

### ✅ User Story 4.3.1 : Injecter les données Discovery dans une base temporaire
### ✅ User Story 4.3.2 : Croiser CMDB vs Discovery (par ID, nom, IP, etc.)
### ✅ User Story 4.3.3 : Annoter les objets avec leur provenance et leur niveau de confiance

## 🧩 Epic 4.4 : Valorisation via dashboards + Elasticsearch (si nécessaire)
- 🎯 Cible : Montrer la couverture, les écarts, et valoriser les données observées pour d'autres usages (logs, sécurité, capacity planning).
- 🧪 Démo attendue : dashboard Kibana ou tableau Streamlit montrant la couverture technique.

### ✅ User Story 4.4.1 : Évaluer l'intérêt d’exposer les données dans Elasticsearch
### ✅ User Story 4.4.2 : Construire un dashboard de couverture d'infra
### ✅ User Story 4.4.3 : Exposer les gaps de connaissance pour prioriser les enrichissements

# 🧭 Initiative 5 : Production d’une topologie validée et instrumentée (pilotée par Discovery)

> Objectif : Construire une topologie technique réaliste sur un périmètre applicatif restreint, en mobilisant les équipes Discovery, les APS et les sources de métriques, pour créer un socle connecté à Elasticsearch et exploitable dans le Knowledge Graph.

## 🧩 Epic 5.1 : Définition du périmètre applicatif et structuration du plan d’exploration

### ✅ User Story 5.1.1 : Choisir un périmètre applicatif représentatif (DMZR + IaaS)
- En tant que : Stream leader
- Je veux : Identifier une application avec des composants répartis (DMZR + IaaS)
- Afin de : Tester la couverture complète des flux de découverte et de validation

### ✅ User Story 5.1.2 : Définir les objectifs de découverte par sous-zone (réseau, VM, appliances…)
### ✅ User Story 5.1.3 : Préparer un plan de travail pour l’équipe Discovery avec jalons

## 🧩 Epic 5.2 : Exécution de la découverte sur périmètre DMZR + IaaS

### ✅ User Story 5.2.1 : Lancer la découverte des composants techniques
### ✅ User Story 5.2.2 : Documenter les types d’objets découverts
### ✅ User Story 5.2.3 : Dresser une première carte de topologie brute

## 🧩 Epic 5.3 : Validation métier et enrichissement par les APS

### ✅ User Story 5.3.1 : Organiser des ateliers de validation de topologie avec les APS
### ✅ User Story 5.3.2 : Identifier les types d’objets pertinents à instrumenter (serveur, interco, VIP…)
### ✅ User Story 5.3.3 : Définir les métriques cibles par type d’objet (config, perf, logs…)

## 🧩 Epic 5.4 : Collecte des métriques et centralisation dans Elasticsearch

### ✅ User Story 5.4.1 : Identifier les outils de collecte adaptés (Discovery, Filebeats, autres ?)
### ✅ User Story 5.4.2 : Mettre en place un pipeline d’injection vers Elasticsearch
### ✅ User Story 5.4.3 : Valider la qualité, fréquence et structuration des données injectées

## 🧩 Epic 5.5 : Connexion avec le Knowledge Graph et usage aval

### ✅ User Story 5.5.1 : Exposer les données Elasticsearch comme source observable pour le KG
### ✅ User Story 5.5.2 : Annoter les nœuds du graphe comme "monitorés"
### ✅ User Story 5.5.3 : Utiliser les patterns Elasticsearch pour déclencher des analyses ou simulations

---

# 💡 Objectifs métier associés

- Créer une **topologie validée** sur un périmètre cohérent, exploitable comme base de démonstrateur pour les LLMs.
- Préparer un pipeline **standardisable** pour d’autres applications.
- Identifier les **zones d’ombre** (non détectables, non instrumentables) pour les adresser dans des itérations ultérieures.
- Apporter une **traçabilité claire** entre ce qui est découvert, ce qui est validé, et ce qui est exploitable.

# 🧭 Initiative 5 : Production d’une topologie observée, validée et instrumentée

> Objectif : Construire une nouvelle branche du graphe IT basée sur des observations réelles issues de Discovery, en la confrontant aux données existantes (TigerGraph) et aux référentiels consolidés via le MDM, pour valider les écarts, détecter les manques et renforcer la fiabilité du socle d’infrastructure.

---

## 🧩 Epic 5.1 : État des lieux de l’IT Services Knowledge Graph existant (TigerGraph)

### ✅ User Story 5.1.1 : Extraire la liste des objets actuellement injectés (Applications, Composants, Relations)
### ✅ User Story 5.1.2 : Identifier les attributs liés à chaque objet et leur provenance (CMDB, Open Data…)
### ✅ User Story 5.1.3 : Identifier ce qui est collecté via le MDM (association C-Marchi)
### ✅ User Story 5.1.4 : Qualifier la complétude, fraîcheur et traçabilité des données TigerGraph

> 💡 But : Savoir ce que je possède déjà et ce que j’ai potentiellement surqualifié à tort dans le graphe.

---

## 🧩 Epic 5.2 : Mise en œuvre de la découverte technique (Discovery) sur un périmètre applicatif

### ✅ User Story 5.2.1 : Définir un périmètre d’expérimentation réaliste (DMZR + IaaS)
### ✅ User Story 5.2.2 : Lancer la découverte sur ce périmètre avec les équipes Discovery
### ✅ User Story 5.2.3 : Documenter les objets découverts par type et leur fréquence d’actualisation
### ✅ User Story 5.2.4 : Générer une première carte de topologie brute observée

> 💡 But : Obtenir une vision réelle du système, déconnectée du déclaratif.

---

## 🧩 Epic 5.3 : Comparaison Discovery vs MDM + Graphe

### ✅ User Story 5.3.1 : Identifier les objets communs entre TigerGraph, MDM et Discovery
### ✅ User Story 5.3.2 : Construire une matrice d’écarts par type d’objet (présence, attributs, complétude)
### ✅ User Story 5.3.3 : Classer les objets en 3 catégories : 
- uniquement MDM / uniquement Discovery / présents dans les deux

### ✅ User Story 5.3.4 : Identifier les cas où le MDM contient des données obsolètes ou désalignées

> 💡 But : Aider à la prise de décision sur les sources à prioriser, renforcer ou écarter.

---

## 🧩 Epic 5.4 : Validation par les APS et définition des métriques utiles

### ✅ User Story 5.4.1 : Organiser des ateliers de validation de la topologie observée
### ✅ User Story 5.4.2 : Déterminer les objets prioritaires à instrumenter
### ✅ User Story 5.4.3 : Lister les métriques utiles par type d’objet (performance, config, disponibilité…)

---

## 🧩 Epic 5.5 : Collecte des métriques et intégration dans Elasticsearch

### ✅ User Story 5.5.1 : Identifier les outils collectant ces métriques (Discovery, Filebeats, autres)
### ✅ User Story 5.5.2 : Établir le pipeline d’envoi des métriques vers Elasticsearch
### ✅ User Story 5.5.3 : Structurer les données pour permettre un requêtage par type d’objet

---

## 🧩 Epic 5.6 : Connexion au Knowledge Graph et valorisation

### ✅ User Story 5.6.1 : Annoter les nœuds comme "observés", "déclarés" ou "consolidés"
### ✅ User Story 5.6.2 : Permettre au graphe d’interroger Elasticsearch pour contextualiser les objets
### ✅ User Story 5.6.3 : Exploiter les patterns d’observation pour enrichir les simulations ou alertes

---

## 🧠 En synthèse
- 📌 Cette initiative crée une **branche parallèle “observée”** du graphe, complémentaire du déclaratif.
- 🔍 Elle permet une **comparaison structurée entre TigerGraph, Discovery et MDM**, avec preuve par les écarts.
- 🤝 Elle engage les **APS comme validateurs métiers**, et crée un pont opérationnel entre les technos data (Elasticsearch) et les raisonnements symboliques (Graphe).
- 🚀 Elle aboutit à un socle exploitable pour les cas d’usage à forte valeur (incidents, obsolescence, capacité, sécurité).

# 🔄 Initiative 6 : Traçabilité des changements réels via pipelines et DevOps Toolchains

> Objectif : Capter les modifications effectives sur l’infrastructure et les applications, issues des toolchains DevOps (infra et dev), pour les confronter aux tickets de changement déclarés dans ServiceNow et améliorer la vérité du Knowledge Graph.

---

## 🧩 Epic 6.1 : Observation des changements d’infrastructure via pipelines APS

### ✅ User Story 6.1.1 : Cartographier les endpoints ou API utilisés par les APS pour provisionner ou modifier l’infra
### ✅ User Story 6.1.2 : Identifier les pipelines DevOps internes utilisés pour les changements infra (Ansible, Terraform, Jenkins, etc.)
### ✅ User Story 6.1.3 : Mettre en place un observateur ou collecteur des logs d’exécution des pipelines APS (via Filebeats ou équivalent)
### ✅ User Story 6.1.4 : Extraire les métadonnées utiles (type de changement, cible, timestamp, utilisateur)

## 🧩 Epic 6.2 : Observation des changements applicatifs via toolchain Dev

### ✅ User Story 6.2.1 : Identifier les outils de CI/CD utilisés par les équipes dev (GitLab, Azure DevOps, Jenkins, etc.)
### ✅ User Story 6.2.2 : Collecter les événements de type push, merge, release, deployment
### ✅ User Story 6.2.3 : Extraire les métadonnées de changement applicatif : application cible, branche, env, impact attendu
### ✅ User Story 6.2.4 : Tagger ces événements dans Elasticsearch pour analyse chronologique et croisement avec logs/métriques

## 🧩 Epic 6.3 : Comparaison avec les tickets de changement ServiceNow

### ✅ User Story 6.3.1 : Extraire les tickets de changement pour le périmètre testé
### ✅ User Story 6.3.2 : Mettre en correspondance événements DevOps ↔ tickets ITSM (par date, système, nature du changement)
### ✅ User Story 6.3.3 : Identifier les changements non déclarés (shadow changes)
### ✅ User Story 6.3.4 : Générer des écarts ou alertes (changement détecté mais non tracé)

## 🧩 Epic 6.4 : Valorisation dans le Knowledge Graph & détection proactive

### ✅ User Story 6.4.1 : Annoter les objets du graphe avec l’historique réel des changements
### ✅ User Story 6.4.2 : Alimenter un flux de type “audit de vérité” pour renforcer la supervision ou la simulation
### ✅ User Story 6.4.3 : Activer des agents de scoring ou de simulation sur base des changements réels

---

## 🧠 Objectifs métier associés

- Renforcer la **véracité du graphe** : ce qui a changé est visible, traçable et justifiable.
- Aider à la **détection des écarts non conformes** (shadow IT, actions non tracées).
- Créer un **système de confiance dynamique** entre équipes Dev, Infra, et Gouvernance.
- Faciliter les **simulations d’impact de changement réels**, sans dépendre uniquement des tickets ServiceNow.

# 🤖 Initiative 7 : Intelligence augmentée et interface agentique pour le Digital Twin

> Objectif : Offrir une interface agentique avancée via Eureka, enrichie avec des agents LangGraph/LangChain, pilotée depuis une plateforme support éditeur, et connectée à un système RAG moderne optimisé pour la documentation.

---

## 🧩 Epic 7.1 : Enrichissement d’Eureka avec des agents LLM

### ✅ User Story 7.1.1 : Intégrer LangChain / LangGraph comme moteur d’orchestration sous-jacent à Eureka
### ✅ User Story 7.1.2 : Définir les premiers agents (Q&A, simulateur d’impact, auditeur de topologie)
### ✅ User Story 7.1.3 : Activer une boucle de raisonnement interprétable et traçable dans les réponses
### ✅ User Story 7.1.4 : Déployer une démo d’interaction raisonnée (sur cas réel de topologie)

---

## 🧩 Epic 7.2 : Mise en place de la plateforme support éditeur pour agents

### ✅ User Story 7.2.1 : Sélectionner une plateforme de déploiement compatible LangChain (LangSmith, LangServe, ou stack interne)
### ✅ User Story 7.2.2 : Définir les exigences techniques (monitoring, logs, API, sécurité, scalabilité)
### ✅ User Story 7.2.3 : Déployer la plateforme dans l’écosystème Domino ou adjacent
### ✅ User Story 7.2.4 : Tester le déploiement d’un agent simple (chat simple ou retriever)

---

## 🧩 Epic 7.3 : Modernisation du RAG documentaire (Doc Knowledge Graph)

### ✅ User Story 7.3.1 : Évaluer la pertinence de la solution IBM Docking actuelle
### ✅ User Story 7.3.2 : Étudier et prototyper un LightRAG basé sur base graphe + base vectorielle
### ✅ User Story 7.3.3 : Tester des solutions type LanceDB, Chroma, ou Faiss pour les embeddings
### ✅ User Story 7.3.4 : Intégrer le nouveau RAG dans la logique agentique d’Eureka

---

## 🧩 Epic 7.4 : Gouvernance et pilotage des pipelines d’alimentation documentaire

### ✅ User Story 7.4.1 : Identifier les sources documentaires prioritaires (CR comités, docs techniques, etc.)
### ✅ User Story 7.4.2 : Définir un modèle de pipeline piloté (orchestration via Prefect, Airflow, etc.)
### ✅ User Story 7.4.3 : Suivre la fraîcheur et la qualité des données injectées dans le RAG
### ✅ User Story 7.4.4 : Mettre à disposition des dashboards de pilotage des pipelines pour l’équipe en charge

---

## 🧠 Objectifs transverses

- Passer d’un chatbot « enrichi » à un **vrai agent raisonneur et autonome**, connecté aux sources internes.
- Offrir une **expérience intelligente, traçable et personnalisée** pour les utilisateurs du jumeau numérique.
- Remplacer le moteur RAG actuel par une solution **moderne, modulaire, performante et intégrable au graphe**.
- Fiabiliser l’alimentation documentaire pour garantir une **cohérence fonctionnelle et technique** dans les réponses du chatbot.

# 🧪 Initiative transverse : Prototypage, démonstration et validation avec le APS Council

> Objectif : Organiser et cadencer les démonstrateurs, les tests et les retours avec un groupe représentatif d’opérationnels (APS Council), dans une logique itérative de validation terrain, au fil du développement sur Domino.

---

## 🧩 Epic T1 : Sélection du périmètre applicatif de référence pour le prototypage

### ✅ User Story T1.1 : Construire un échantillonnage cohérent d’applications (DMZR, IaaS, etc.)
### ✅ User Story T1.2 : Valider cet échantillon avec le APS Council
### ✅ User Story T1.3 : Garantir la représentativité des cas d’usage infra, app et orga

---

## 🧩 Epic T2 : Intégration du APS Council dans la gouvernance produit

### ✅ User Story T2.1 : Créer un cycle d’échanges régulier avec le Council (copil, design review, testing)
### ✅ User Story T2.2 : Prioriser les use cases et User Stories en lien avec les irritants identifiés par les APS
### ✅ User Story T2.3 : Identifier des profils alpha/bêta pour chaque démonstrateur

---

## 🧩 Epic T3 : Structuration de la plateforme Domino pour l’expérimentation

### ✅ User Story T3.1 : Ouvrir des espaces Domino sécurisés pour les bêta-tests
### ✅ User Story T3.2 : Déployer des démonstrateurs exploitables (sans industrialisation complète)
### ✅ User Story T3.3 : Mettre en place un module de feedback utilisateur post-test

---

## 🧩 Epic T4 : Intégration continue des feedbacks dans la roadmap agile

### ✅ User Story T4.1 : Tagger les retours APS comme points d’amélioration ou d’ajustement
### ✅ User Story T4.2 : Créer un backlog parallèle des évolutions issues des démonstrateurs
### ✅ User Story T4.3 : Inclure des feedback loops à chaque fin d’epic ou sprint clé

---

## 💡 Points transverses

- Chaque démonstrateur produit (qu’il vienne de l’initiative 1, 5 ou 7) **doit intégrer un test avec les APS**.
- Les **User Stories validées par le APS Council** sont taggées dans ton backlog comme prioritaires terrain.
- Les retours du Council peuvent déclencher soit de **nouvelles stories**, soit des **pivots de design**.

# 🔧 Initiative 8 : Construction des moteurs intelligents du Digital Tool

> Objectif : Capitaliser sur les données structurées du Knowledge Graph, les flux de logs, les cas d’usage simulés et l’interaction agentique pour créer des moteurs intelligents (engines) capables de diagnostiquer, corréler, calculer des risques ou expliquer les causes dans l’environnement IT.

---

## 🧩 Epic 8.1 : Application Integrity Engine

🎯 But : détecter les incohérences entre les dépendances d’une application (version OS, base, middleware, certificats…)

### ✅ User Story 8.1.1 : Définir les patterns d’intégrité à surveiller (version, couplage, obsolescence…)
### ✅ User Story 8.1.2 : Injecter les règles dans le graphe (symbolic AI ou graphe de validation)
### ✅ User Story 8.1.3 : Détecter les écarts sur un périmètre applicatif bêta (avec APS)

---

## 🧩 Epic 8.2 : Correlation Engine

🎯 But : corréler des incidents avec des métriques observées, des changements ou des logs.

### ✅ User Story 8.2.1 : Identifier les nœuds liés à un incident (topologie, change, métriques)
### ✅ User Story 8.2.2 : Rejouer des incidents passés pour détecter des patterns corrélés
### ✅ User Story 8.2.3 : Créer une vue corrélée pour l’agent Eureka

---

## 🧩 Epic 8.3 : Risk Engine

🎯 But : anticiper le niveau de risque d’un changement ou d’un état de configuration actuel.

### ✅ User Story 8.3.1 : Définir une taxonomie des risques infra (criticité, obsolescence, point unique)
### ✅ User Story 8.3.2 : Construire un moteur de scoring basé sur les graphes et la simulation
### ✅ User Story 8.3.3 : Injecter un agent dans Eureka pour calculer le risque avant action

---

## 🧩 Epic 8.4 : Impact Calculation Engine

🎯 But : projeter la propagation d’un changement, d’un incident ou d’une coupure technique

### ✅ User Story 8.4.1 : Utiliser la topologie du graphe pour simuler la propagation
### ✅ User Story 8.4.2 : Ajouter des poids de criticité ou de dépendance dans le graphe
### ✅ User Story 8.4.3 : Fournir un graphe d’impact interprétable (input LLM ou visuel)

---

## 🧩 Epic 8.5 : Causality Engine

🎯 But : analyser les causes racines (root causes) à partir des événements passés et des relations d’impacts

### ✅ User Story 8.5.1 : Créer un modèle de propagation inverse (de l’effet à la cause)
### ✅ User Story 8.5.2 : Croiser les données logs, metrics et changements pour reconstruire l’historique
### ✅ User Story 8.5.3 : Générer une explication textuelle ou graphe de cause dans Eureka

---

## 🧠 Gouvernance & Roadmap Agile des moteurs

- Chaque **moteur est construit comme un bloc réutilisable** et découplé, branché sur le graphe.
- L’alimentation provient des **initiatives existantes** (logs, topologie, RAG, simulation).
- Les démonstrateurs sont testés sur les **applications bêta du périmètre APS Council**.
- Les moteurs peuvent être activés via des **agents LangChain**, en frontal dans Eureka ou en backend via APIs.

