CREATE QUERY GetInfraFromApp() FOR GRAPH UKG_V2 {
  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // 1) Clusters + Changes en une seule étape
  Result = SELECT ch
    FROM (a:Application)-[:USES]->(at:Application),
         (at)-[:USES]->(c:Cluster),
         (c)-[:IMPACTS]->(ch:Change)
    WHERE a.auid == "AP85343"
      AND at.environment == "Production"
    ACCUM 
      @@infraSet += c,
      @@changeSet += ch;

  // Résultats finaux
  PRINT @@infraSet;
  PRINT @@changeSet;
}
