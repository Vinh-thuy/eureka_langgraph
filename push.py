CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : récupérer l'application fonctionnelle
  VertexSet<Application> startApp = 
    SELECT a FROM Application:a 
    WHERE a.auid == "AP85343";
  PRINT startApp;

  // Étape 2 : récupérer les applications techniques en "Production"
  VertexSet<Application> appTech = 
    SELECT at FROM startApp - (USES) -> Application:at
    WHERE at.environment == "Production";
  PRINT appTech;

  // Étape 3a : serveurs
  VertexSet<Server> servers = 
    SELECT s FROM appTech - (USES) -> Server:s
    ACCUM @@infraSet += s;
  PRINT servers;

  // Étape 3b : clusters
  VertexSet<Cluster> clusters = 
    SELECT c FROM appTech - (USES) -> Cluster:c
    ACCUM @@infraSet += c;
  PRINT clusters;

  // Étape 4a : changes via serveurs
  VertexSet<Change> serverChanges = 
    SELECT ch FROM servers - (IMPACTS) -> Change:ch
    ACCUM @@changeSet += ch;
  PRINT serverChanges;

  // Étape 4b : changes via clusters
  VertexSet<Change> clusterChanges = 
    SELECT ch FROM clusters - (IMPACTS) -> Change:ch
    ACCUM @@changeSet += ch;
  PRINT clusterChanges;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
