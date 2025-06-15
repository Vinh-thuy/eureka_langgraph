CREATE QUERY GetInfraForProduction() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : serveurs liés et leurs changes
  ServerChanges = SELECT ch 
    FROM Application:a -(USES:e1)-> Application:at
                   -(USES:e2)-> Server:s
                   -(IMPACTS:e3)-> Change:ch
    WHERE a.auid == "AP85343" AND at.environment == "Production"
    ACCUM @@infraSet += s, @@changeSet += ch;
  PRINT ServerChanges;

  // Étape 2 : clusters liés et leurs changes
  ClusterChanges = SELECT ch 
    FROM Application:a -(USES:e1)-> Application:at
                   -(USES:e2)-> Cluster:c
                   -(IMPACTS:e3)-> Change:ch
    WHERE a.auid == "AP85343" AND at.environment == "Production"
    ACCUM @@infraSet += c, @@changeSet += ch;
  PRINT ClusterChanges;

  // Résultat global
  PRINT @@infraSet;
  PRINT @@changeSet;
}
