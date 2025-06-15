MATCH (a:Application {auid: $appId})-[r1:USES]->(at:Application {environment: 'Production'})-[r2:USES]->(s:Server)
OPTIONAL MATCH (s)-[r3:IMPACTS]->(ch:Change)
WITH COLLECT(DISTINCT s) AS servers, COLLECT(DISTINCT ch) AS serverChanges

MATCH (a:Application {auid: $appId})-[r4:USES]->(at2:Application {environment: 'Production'})-[r5:USES]->(c:Cluster)
OPTIONAL MATCH (c)-[r6:IMPACTS]->(ch2:Change)
WITH servers + COLLECT(DISTINCT c) AS allInfra, 
     serverChanges + COLLECT(DISTINCT ch2) AS allChanges

UNWIND allInfra AS infra
UNWIND allChanges AS change
RETURN COLLECT(DISTINCT infra) AS infrastructure, 
       COLLECT(DISTINCT change) AS changes
