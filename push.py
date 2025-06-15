CREATE QUERY GetInfraForProduction() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  Start = SELECT a FROM Application:a
          WHERE a.auid == "AP85343";

  // Étape 2 : applications techniques en environnement "Production"
  AppTech = SELECT at FROM Start:a - (USES:e) -> Application:at
            WHERE at.environment == "Production";

  // Étape 3 : serveurs liés
  ToServers = SELECT s FROM AppTech:at - (USES:e) -> Server:s
              ACCUM @@infraSet += s;
  PRINT ToServers;

  // Étape 4 : clusters liés
  ToClusters = SELECT c FROM AppTech:at - (USES:e) -> Cluster:c
               ACCUM @@infraSet += c;
  PRINT ToClusters;

  // Étape 5a : changes depuis serveurs (si présents)
  ServerChanges = SELECT ch FROM AppTech:at - (USES:e1) -> Server:s - (IMPACTS:e2) -> Change:ch
                  ACCUM @@changeSet += ch;
  PRINT ServerChanges;

  // Étape 5b : changes depuis clusters (si présents)
  ClusterChanges = SELECT ch FROM AppTech:at - (USES:e1) -> Cluster:c - (IMPACTS:e2) -> Change:ch
                   ACCUM @@changeSet += ch;
  PRINT ClusterChanges;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
