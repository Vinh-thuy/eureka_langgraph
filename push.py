MATCH (app:Application {auid: "AP85343"})-[:USES]->(tech:Application {environment: "Production"})
OPTIONAL MATCH (tech)-[:USES]->(s:Server)-[:IMPACTS]->(c1:Change)
OPTIONAL MATCH (tech)-[:USES]->(cl:Cluster)-[:IMPACTS]->(c2:Change)
RETURN DISTINCT app, tech, s, c1, cl, c2
