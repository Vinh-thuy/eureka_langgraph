CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  Result = SELECT ch
    FROM Application:a - (USES) -> Application:at
                      - (USES) -> Cluster:c
                      - (IMPACTS) -> Change:ch
    WHERE a.auid == "AP85343"
      AND at.environment == "Production"
    ACCUM
      @@infraSet += c,
      @@changeSet += ch;

  PRINT @@infraSet;
  PRINT @@changeSet;
}
