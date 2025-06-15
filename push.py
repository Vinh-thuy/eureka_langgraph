MATCH (a:Application {auid: "AP85343"})-[:USES]->(at:Application)
WHERE at.environment = "Production"

MATCH (at)-[:USES]->(cl:Cluster)
MATCH (cl)-[:IMPACTS]->(c:Change)

RETURN
  a.auid AS app_code,
  at.environment AS env,
  at.name AS tech_app_name,
  cl.name AS cluster_name,
  cl.region AS cluster_region,
  c.change_id AS change_id,
  c.type AS change_type,
  c.status AS change_status,
  c.date AS change_date
