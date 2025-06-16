CREATE QUERY GetInfraFromApp(STRING auid, STRING env) FOR GRAPH UKG_V2 SYNTAX v2 {
  // Déclaration des sets pour V2
  // On déclare tous les vertices nécessaires en amont si on veut optimiser, mais ici on peut directement référencer les types

  // Pattern matching multi-hop avec FROM + PATTERN (V2)
  pathRes = SELECT a, b, c
            FROM Application:a, Application:b, Cluster:c
            PATTERN (a)-[e1:USES]->(b)-[e2:USES]->(c)
            WHERE a.auid == auid
              AND b.environment == env;

  PRINT pathRes;
}




// Version OK
CREATE QUERY GetInfraFromApp(STRING auid, STRING env) FOR GRAPH UKG_V2 {
  // 1. Récupération de tous les vertices Application
  startApps = { Application.* };
  
  // 2. Filtrage sur l'attribut auid
  selApp =
    SELECT a
    FROM startApps AS a
    WHERE a.auid == auid;
  
  // 3. Navigation via l'arête USES vers l'application dans l'environnement spécifié
  envApps =
    SELECT a2
    FROM selApp AS a - (USES:e) -> Application AS a2
    WHERE a2.environment == env;
  
  // 4. Navigation via l'arête USES vers les Clusters
  resultClusters =
    SELECT c
    FROM envApps AS a2 - (USES:e2) -> Cluster AS c;
  
  // 5. Affichage du résultat
  PRINT resultClusters;
}

