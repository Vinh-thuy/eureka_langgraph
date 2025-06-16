CREATE QUERY GetInfraFromApp(STRING auid, STRING env) FOR GRAPH UKG_V2 {
  // 1. Création d'un handle pour tous les vertices Application
  appVertices = { Application.* };

  // 2. Sélection des chemins : Application -> Application(env) puis -> Cluster
  SELECT a, b, c
  INTO paths
  FROM (appVertices:a) -(USES:e1)-> (appVertices:b),
       (appVertices:b) -(USES:e2)-> (Cluster:c)
  WHERE a.auid == auid
    AND b.environment == env;

  // 3. Affichage des chemins complets
  PRINT paths;
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

