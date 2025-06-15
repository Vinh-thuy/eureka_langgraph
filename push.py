CREATE QUERY GetInfraForProduction() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : serveurs liés aux apps techniques
  SELECT ch FROM Application:a
    -(USES)-> Application:at
    -(USES)-> Server:s
    -(IMPACTS)-> Change:ch
    WHERE a.auid == "AP85343" AND at.environment == "Production"
    ACCUM @@infraSet += s,
          @@changeSet += ch;

  // Étape 2 : clusters liés aux apps techniques
  SELECT ch FROM Application:a
    -(USES)-> Application:at
    -(USES)-> Cluster:c
    -(IMPACTS)-> Change:ch
    WHERE a.auid == "AP85343" AND at.environment == "Production"
    ACCUM @@infraSet += c,
          @@changeSet += ch;

  // Résultat final
  PRINT @@infraSet;
  PRINT @@changeSet;
}
