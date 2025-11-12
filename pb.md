Objet : Préparation des travaux du Conseil Scientifique – Synthèse de quatre articles de recherche pour le Digital Twin d’Infrastructure IT

Bonjour,

Dans le cadre de la construction de notre Digital Twin d’Infrastructure IT, nous avons identifié quatre articles de recherche récents qui ouvrent des perspectives intéressantes pour :
	•	détecter des événements rares mais systémiques(long-range GNN),
	•	construire automatiquement un graphe de connaissances IT fiable (GraphMERT),
	•	ingérer massivement notre documentation technique (GraphMERT),
	•	améliorer la compréhension contextuelle des événements dans l’infrastructure (GraphMERT).

L’ensemble forme un socle cohérent pour développer un Digital Twin véritablement proactif, explicable, résilient et compatible avec des agents autonomes.

Je vous propose ci-dessous une synthèse non technique de ces travaux, ainsi que les problématiques scientifiques associées que nous souhaiterions soumettre au Conseil Scientifique.


Long-range GNN & Systemic Risk Graph Modeling
Réf. openreview + arXiv:2506.05971

Ces travaux explorent une avancée majeure dans la modélisation des graphes à grande portée (long-range), un domaine critique pour analyser des phénomènes rares mais systémiques, capables de relier des zones distantes d’un réseau complexe. Dans notre contexte IT, ces mécanismes sont directement applicables à la détection d’incidents se propageant à grande échelle (effets cascade, blast radius, propagation inter-datacenters…).

Problématiques associées :

1. Détection des risques systémiques rares
Comment utiliser les long-range GNN pour détecter des incidents rares mais critiques (cascades, congestions, outages multi-domaines) se propageant à travers notre graphe d’infrastructure IT ?

2. Simulation de propagation d’incidents
Comment adapter les encodeurs long-range pour prédire l’évolution d’un incident (latence, CPU saturation, routage défaillant) au sein d’un graphe IT dynamique mêlant dépendances applicatives, réseau et métiers ?

3. Identification de signaux faibles précurseurs
Dans quelle mesure ces modèles peuvent-ils révéler des “pré-incidents” distribués (anomalies faibles mais corrélées) annonçant un futur événement systémique ?


GraphMERT – Distillation neurosymbolique fiable de graphes de connaissances

Réf. : arXiv:2510.09580

GraphMERT introduit une approche neurosymbolique permettant d’extraire automatiquement un graphe de connaissances fiable et ontologiquement cohérent à partir de données non structurées. Cette approche réduit la dépendance aux hallucinations des LLM et garantit traçabilité, auditabilité et cohérence.

Problématiques associées :

1. Construction automatique d’un IT Knowledge Graph fiable
Comment adapter GraphMERT pour convertir dynamiquement nos tickets ServiceNow, logs, documentation IT et rapports d’incidents en un graphe fiable, cohérent et aligné sur notre ontologie CMDB ?

2. Réduction des hallucinations & amélioration de la traçabilité
Dans quelle mesure GraphMERT peut-il réduire la génération erronée d’information en renforçant la traçabilité, la factualité et l’auditabilité des connaissances au sein du Digital Twin ?

3. Raisonnement neuro-symbolique pour la RCA et l’analyse d’impact
Comment combiner GraphMERT et un Knowledge Graph IT pour améliorer la Root Cause Analysis, la prédiction d’impact et le raisonnement explicable dans le Digital Twin ?


 DeepSeek-OCR – Compression optique et ingestion documentaire massive

Réf. : arXiv:2510.18234

DeepSeek-OCR propose un mécanisme de compression optique permettant d’ingérer des documents complexes (PDF, SOP, runbooks, rapports techniques) en un nombre très réduit de vision tokens, tout en préservant structure, logique et précision. Cela permet une ingestion documentaire à très grande échelle, à faible coût.

Problématiques associées :

1. Ingestion massive et compressée de documentation IT
Comment utiliser l’Optical Token Compression pour ingérer et structurer nos dossiers d’exploitation, procédures, rapports et architectures dans une mémoire persistante du Digital Twin ?

2. Alignement Documentaire → Knowledge Graph → Agents
Comment relier ces représentations compressées au Knowledge Graph IT afin de permettre aux agents d’identifier rapidement procédures, dépendances et impacts lors d’un incident ?

3. Automatisation du cycle documentation → actions
Comment exploiter DeepSeek-OCR pour extraire automatiquement les règles opérationnelles, SOP et remédiations contextuelles afin d’alimenter les agents de diagnostic et de self-healing ?


EgoPrompt – Fusion événement–composant et contextualisation

Réf. : EgoPrompt, ACM MM’25 / arXiv:2508.03266

EgoPrompt introduit un système de prompt learning centré sur la fusion action–objet. Transposé à notre contexte, il permettrait de fusionner efficacement événements IT (verbes) + composants IT (noms), améliorant la compréhension contextuelle, la détection d’incidents émergents et la résilience adaptative.

Problématiques associées :

1. Fusion contextuelle événement–composant
Comment adapter EgoPrompt (Unified Prompt Pool + Diverse Pool Criteria) pour apprendre automatiquement les relations complexes entre nos événements d’infrastructure et les composants IT ?

2. Détection cross-environnements d’incidents émergents
Dans quelle mesure les mécanismes de diversification de prompts d’EgoPrompt permettent-ils au Digital Twin de détecter des incidents nouveaux et des anomalies dans des environnements multi-cloud et Kubernetes ?

3. Intégration avec graphes de dépendances IT
Comment intégrer les patterns événement–composant d’EgoPrompt dans notre IT Knowledge Graph afin d’améliorer la RCA, la simulation d’impact et l’explicabilité ?
