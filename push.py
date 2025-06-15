CREATE QUERY GetInfraForProduction() FOR GRAPH UKG_V2 {

  SetAccum<VERTEX> @@infraSet;
  SetAccum<VERTEX> @@changeSet;

  // Étape 1 : application fonctionnelle
  VertexSet<Application> start = SELECT a FROM Application:a
                                 WHERE a.auid == "AP85343";

  // Étape 2 : applications techniques "Production"
  VertexSet<Application> appsTech = SELECT at FROM start - (USES) -> Application:at
                                    WHERE at.environment == "Production";

  // Étape 3 : serveurs
  VertexSet<Server> servers = SELECT s FROM appsTech - (USES) -> Server:s
                              ACCUM @@infraSet += s;

  // Étape 4 : clusters
  VertexSet<Cluster> clusters = SELECT c FROM appsTech - (USES) -> Cluster:c
                                ACCUM @@infraSet += c;

  // Étape 5 : changes via serveurs
  SELECT ch FROM servers - (IMPACTS) -> Change:ch
            ACCUM @@changeSet += ch;

  // Étape 6 : changes via clusters
  SELECT ch FROM clusters - (IMPACTS) -> Change:ch
            ACCUM @@changeSet += ch;

  // Résultats
  PRINT @@infraSet;
  PRINT @@changeSet;
}
