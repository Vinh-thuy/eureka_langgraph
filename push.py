CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  Start = SELECT a FROM Application:a
          WHERE a.auid == "AP85343";
  PRINT Start;

  // Étape 2 : serveurs liés via application technique en Production
  FromAppToServer = SELECT s 
                    FROM Start:a - (USES:e1) -> Application:at 
                                  - (USES:e2) -> Server:s
                    WHERE at.environment == "Production"
                    ACCUM @@infraSet += s;
  PRINT FromAppToServer;

  // Étape 3 : changes depuis les serveurs
  ServerChanges = SELECT ch 
                  FROM Start:a - (USES:e1) -> Application:at 
                                - (USES:e2) -> Server:s 
                                - (IMPACTS:e3) -> Change:ch
                  WHERE at.environment == "Production"
                  ACCUM @@changeSet += ch;
  PRINT ServerChanges;

  // Étape 4 : clusters liés via application technique en Production
  FromAppToCluster = SELECT c 
                     FROM Start:a - (USES:e1) -> Application:at 
                                   - (USES:e2) -> Cluster:c
                     WHERE at.environment == "Production"
                     ACCUM @@infraSet += c;
  PRINT FromAppToCluster;

  // Étape 5 : changes depuis les clusters
  ClusterChanges = SELECT ch 
                   FROM Start:a - (USES:e1) -> Application:at 
                                 - (USES:e2) -> Cluster:c 
                                 - (IMPACTS:e3) -> Change:ch
                   WHERE at.environment == "Production"
                   ACCUM @@changeSet += ch;
  PRINT ClusterChanges;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
