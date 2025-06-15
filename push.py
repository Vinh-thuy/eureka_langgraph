CREATE QUERY GetInfraFromApp(STRING appAUID) FOR GRAPH InfraGraph {
  
  SetAccum<VERTEX> @@infraSet;

  Start = SELECT a
          FROM application:a
          WHERE a.AUID == appAUID;

  // Parcours vers les serveurs
  ToServeurs = SELECT s
               FROM Start:a - (use:e) -> serveur:s
               ACCUM @@infraSet += s;

  // Parcours vers les clusters
  ToClusters = SELECT c
               FROM Start:a - (use:e) -> cluster:c
               ACCUM @@infraSet += c;

  PRINT @@infraSet;
}
