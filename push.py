

CREATE QUERY GetInfraPaths(STRING auid, STRING env) FOR GRAPH UKG_V2 {
  // Sélection de tous les chemins Application -> Application(env) -> Cluster
  pathResults =
    SELECT a, a2, c
    FROM Application:a -(USES:e1)-> Application:a2 -(USES:e2)-> Cluster:c
    WHERE a.auid == auid
      AND a2.environment == env;

  // Affichage de chaque chemin complet (startApp, envApp, cluster)
  PRINT pathResults;
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

