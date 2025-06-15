MATCH (a:Application {auid: "AP85343"})-[:USES]->(at:Application)
WHERE at.environment = "Production"

OPTIONAL MATCH (at)-[:USES]->(s:Server)
OPTIONAL MATCH (s)-[:IMPACTS]->(c1:Change)

OPTIONAL MATCH (at)-[:USES]->(cl:Cluster)
OPTIONAL MATCH (cl)-[:IMPACTS]->(c2:Change)

RETURN DISTINCT a, at, s, c1, cl, c2
