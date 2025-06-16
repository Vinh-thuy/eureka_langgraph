CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // 1) D'abord, trouver l'application source
  SourceApp = SELECT a 
              FROM Application:a 
              WHERE a.auid == "AP85343";

  // 2) Ensuite, trouver les applications de production liées
  ProdApps = SELECT t 
             FROM SourceApp:s - (USES) - Application:t
             WHERE t.environment == "Production";

  // 3) Puis trouver les clusters liés
  Clusters = SELECT c 
             FROM ProdApps:p - (USES) - Cluster:c
             ACCUM @@infraSet += c;

  // 4) Enfin, trouver les changements liés
  Changes = SELECT ch 
            FROM Clusters:c - (IMPACTS) - Change:ch
            ACCUM @@changeSet += ch;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
