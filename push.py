CREATE QUERY GetInfraFromApp(STRING appId) FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // 1) Serveurs + Changes
  ServerPaths = SELECT s
    FROM Application:a - (:USES) - Application:at - (:USES) - Server:s - (:IMPACTS) - Change:ch
    WHERE a.auid == appId
      AND at.environment == "Production"
    ACCUM 
      @@infraSet += s,
      @@changeSet += ch;

  // 2) Clusters + Changes
  ClusterPaths = SELECT c
    FROM Application:a - (:USES) - Application:at - (:USES) - Cluster:c - (:IMPACTS) - Change:ch
    WHERE a.auid == appId
      AND at.environment == "Production"
    ACCUM 
      @@infraSet += c,
      @@changeSet += ch;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
