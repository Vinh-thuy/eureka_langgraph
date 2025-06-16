CREATE DISTRIBUTED QUERY bfs_AppToIssues() FOR GRAPH UKG_V2 SYNTAX v1 {
  // Accumulateurs
  MinAccum<INT> @dist;
  SetAccum<VERTEX> @@issues;
  @@issues = {};

  // 1. Démarrage BFS : vertex Application filtré
  frontier =
    SELECT s
    FROM Application:s
    WHERE s.auid == "AP85343"
    POST-ACCUM s.@dist = 0;

  // 2. Hop 1 : Application -> Cluster via USES
  frontier =
    SELECT cl
    FROM frontier:s - USES -> Cluster:cl
    WHERE cl.@dist > s.@dist
    ACCUM cl.@dist = s.@dist + 1;

  // 3. Hop 2 : Cluster -> Change via IMPACTS
  SELECT ch
  INTO tempIssues
  FROM frontier:s - IMPACTS -> Change:ch
  ACCUM ch.@dist = s.@dist + 1,
        @@issues += ch;

  // 4. Hop 3 : Cluster -> Incident via IMPACTS
  SELECT inc
  INTO tempIncidents
  FROM frontier:s - IMPACTS -> Incident:inc
  ACCUM inc.@dist = s.@dist + 1,
        @@issues += inc;

  // 5. Affichage des Change et Incident collectés
  PRINT @@issues;
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

