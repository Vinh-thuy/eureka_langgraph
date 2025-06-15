MATCH (a:Application {auid: "AP85343"})-[:USES]->(at:Application)
WHERE at.environment = "Production"
MATCH (at)-[:USES]->(cl:Cluster)
OPTIONAL MATCH (c:Change)-[:IMPACTS]->(cl)
OPTIONAL MATCH (i:Incident)-[:IMPACTS]->(cl)
RETURN
  a.auid AS app_code,
  at.environment AS env,
  cl.name AS cluster_name,
  c.change_id AS change_id,
  i.incident_id AS incident_id
