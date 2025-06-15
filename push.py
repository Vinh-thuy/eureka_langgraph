CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  Start = SELECT a FROM Application:a
          WHERE a.auid == "AP85343";
  PRINT Start;

  // Étape 2 : applications techniques en "Production"
  AppTech = SELECT at FROM Start:a - (USES:e) -> Application:at
            WHERE at.environment == "Production";
  PRINT AppTech;

  // Étape 3 : collecte directe des servers et changes
  FromAppToServer = SELECT s FROM AppTech:at - (USES:e) -> Server:s
                    ACCUM @@infraSet += s;
  PRINT FromAppToServer;

  ServerChanges = SELECT ch FROM AppTech:at - (USES:e) -> Server:s - (IMPACTS:e2) -> Change:ch
                  ACCUM @@changeSet += ch;
  PRINT ServerChanges;

  // Étape 4 : collecte directe des clusters et changes
  FromAppToCluster = SELECT c FROM AppTech:at - (USES:e) -> Cluster:c
                     ACCUM @@infraSet += c;
  PRINT FromAppToCluster;

  ClusterChanges = SELECT ch FROM AppTech:at - (USES:e) -> Cluster:c - (IMPACTS:e2) -> Change:ch
                   ACCUM @@changeSet += ch;
  PRINT ClusterChanges;

  // Résultats
  PRINT @@infraSet;
  PRINT @@changeSet;
}
