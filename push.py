MATCH (a:Application {auid: "AP853434"})-[r]-(n)
RETURN 
  a.auid AS application_auid,
  type(r) AS relation_type,
  labels(n)[0] AS neighbor_type,
  n.id AS neighbor_id
