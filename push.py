// Requête simplifiée pour les clusters uniquement
MATCH (a:Application {auid: 'AP85343'})-[:USES]->(at:Application {environment: 'Production'})-[:USES]->(c:Cluster)
OPTIONAL MATCH (c)-[:IMPACTS]->(ch:Change)
RETURN COLLECT(DISTINCT c) AS clusters, 
       COLLECT(DISTINCT ch) AS changes
