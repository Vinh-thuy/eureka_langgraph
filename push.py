CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // 1) Clusters + Changes
  Start = {Application.*};
  
  // Première étape : trouver les applications de production
  ProdApps = SELECT at 
             FROM Start:a - (USES) -> Application:at
             WHERE a.auid == "AP85343" 
               AND at.environment == "Production";
  
  // Deuxième étape : trouver les clusters liés
  ClusterPaths = SELECT c 
                 FROM ProdApps:at - (USES) -> Cluster:c
                 POST-ACCUM
                   @@infraSet += c;
  
  // Troisième étape : trouver les changements liés
  Changes = SELECT ch 
            FROM ClusterPaths:c - (IMPACTS) -> Change:ch
            POST-ACCUM 
              @@changeSet += ch;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
