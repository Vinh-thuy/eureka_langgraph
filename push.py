CREATE QUERY GetInfraAndChangesForProduction() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  Start = SELECT a FROM Application:a
          WHERE a.auid == "AP85343";

  // Étape 2 : applications techniques en environnement "Production"
  AppTech = SELECT at FROM Start:a - (USES:e) -> Application:at
            WHERE at.environment == "Production";

  // Étape 3 : collecte des serveurs
  ToServers = SELECT s FROM AppTech:at - (USES:e) -> Server:s
              ACCUM @@infraSet += s;

  // Étape 4 : collecte des clusters
  ToClusters = SELECT c FROM AppTech:at - (USES:e) -> Cluster:c
               ACCUM @@infraSet += c;

  // Étape 5 : collecte des changes depuis les serveurs
  ServerChanges = SELECT ch FROM ToServers:s - (1PACKS:e) -> Change:ch
                  ACCUM @@changeSet += ch;

  // Étape 6 : collecte des changes depuis les clusters
  ClusterChanges = SELECT ch FROM ToClusters:c - (1PACKS:e) -> Change:ch
                   ACCUM @@changeSet += ch;

  // Résultats
  PRINT @@infraSet;
  PRINT @@changeSet;
}
