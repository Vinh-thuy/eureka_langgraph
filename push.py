CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  startApp = { Application.* };
  startApp = SELECT a FROM startApp:a
             WHERE a.auid == "AP85343";
  PRINT startApp;

  // Étape 2a : serveurs via app technique en Production
  serverPaths = SELECT s
                FROM startApp:s -(USES:e1)-> Application:at -(USES:e2)-> Server:s
                WHERE at.environment == "Production"
                ACCUM @@infraSet += s;
  PRINT serverPaths;

  // Étape 2b : clusters via app technique en Production
  clusterPaths = SELECT c
                 FROM startApp:s -(USES:e1)-> Application:at -(USES:e2)-> Cluster:c
                 WHERE at.environment == "Production"
                 ACCUM @@infraSet += c;
  PRINT clusterPaths;

  // Étape 3a : changes depuis serveurs
  serverChanges = SELECT ch
                  FROM startApp:s -(USES:e1)-> Application:at -(USES:e2)-> Server:s
                                 -(IMPACTS:e3)-> Change:ch
                  WHERE at.environment == "Production"
                  ACCUM @@changeSet += ch;
  PRINT serverChanges;

  // Étape 3b : changes depuis clusters
  clusterChanges = SELECT ch
                   FROM startApp:s -(USES:e1)-> Application:at -(USES:e2)-> Cluster:c
                                  -(IMPACTS:e3)-> Change:ch
                   WHERE at.environment == "Production"
                   ACCUM @@changeSet += ch;
  PRINT clusterChanges;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
