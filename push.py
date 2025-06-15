CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // 1) Serveurs + Changes
  ServerPaths = SELECT s
    FROM Application:a -(USES:e1)-> Application:at -(USES:e2)-> Server:s -(IMPACTS:e3)-> Change:ch
    WHERE a.auid == "AP85343"
      AND at.environment == "Production"
    ACCUM @@infraSet += s,
          @@changeSet += ch;
  PRINT ServerPaths;

  // 2) Clusters + Changes
  ClusterPaths = SELECT c
    FROM Application:a -(USES:e1)-> Application:at -(USES:e2)-> Cluster:c -(IMPACTS:e3)-> Change:ch
    WHERE a.auid == "AP85343"
      AND at.environment == "Production"
    ACCUM @@infraSet += c,
          @@changeSet += ch;
  PRINT ClusterPaths;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
