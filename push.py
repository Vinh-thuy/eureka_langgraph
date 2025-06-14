MATCH (a:Application {auid: "AP853434"})-[:DEPLOYED_ON]->(c:Cluster)
OPTIONAL MATCH (c)-[:HAS_INCIDENT]->(i:Incident)
OPTIONAL MATCH (c)-[:HAS_CHANGE]->(ch:Change)
RETURN DISTINCT c, i, ch
