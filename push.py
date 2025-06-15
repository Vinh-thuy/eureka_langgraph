CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  Start = SELECT a FROM Application:a
          WHERE a.auid == "AP85343";
  PRINT Start;

  // Étape 2 : applications techniques en environnement "Production"
  AppTech = SELECT at FROM Start:a - (USES:e) -> Application:at
            WHERE at.environment == "Production";
  PRINT AppTech;

  // Étape 3 : serveurs liés
  TmpServers = SELECT s FROM AppTech:at - (USES:e) -> Server:s
               ACCUM @@infraSet += s;
  PRINT TmpServers;

  // Étape 4 : clusters liés
  TmpClusters = SELECT c FROM AppTech:at - (USES:e) -> Cluster:c
                ACCUM @@infraSet += c;
  PRINT TmpClusters;

  // Étape 5 : changes depuis servers
  ServerChanges = SELECT ch FROM TmpServers:s - (IMPACTS:e) -> Change:ch
                  ACCUM @@changeSet += ch;
  PRINT ServerChanges;

  // Étape 6 : changes depuis clusters
  ClusterChanges = SELECT ch FROM TmpClusters:c - (IMPACTS:e) -> Change:ch
                   ACCUM @@changeSet += ch;
  PRINT ClusterChanges;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
