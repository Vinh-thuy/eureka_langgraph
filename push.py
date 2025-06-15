CREATE QUERY GetInfraAndChangesForProduction() FOR GRAPH UKG_V2 {

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

  // Étape 4 : clusters liés
  ToClusters = SELECT c FROM AppTech:at - (USES:e) -> Cluster:c
               ACCUM @@infraSet += c;

  // Étape 5 : changes depuis serveurs
  ServerChanges = SELECT ch FROM ToServers:s - (IMPACTS:e) -> Change:ch
                  ACCUM @@changeSet += ch;

  // Étape 6 : changes depuis clusters
  ClusterChanges = SELECT ch FROM ToClusters:c - (IMPACTS:e) -> Change:ch
                   ACCUM @@changeSet += ch;

  // Résultat final
  PRINT @@infraSet;
  PRINT @@changeSet;
}
