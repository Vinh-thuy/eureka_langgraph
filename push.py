Subject: Request for GSQL Query Logic to Traverse from Application to Incidents/Changes, with Infrastructure Context

Hi [Name],

As part of a broader initiative to feed knowledge into a multi-agent LLM system, I’d like to request your support in building a GSQL query that captures the full technical and contextual path between a specific application and its associated infrastructure and operational events.

⸻

🔹 Use Case #1 – From an Application to Related Changes and Incidents

Objective:
Starting from a specific node of type Application (with attribute auid = "AP85343"), I want to:
	•	Traverse the infrastructure graph to reach all associated Incident and Change nodes.
	•	Retrieve the full path, including all intermediate nodes like Cluster, Application, etc.
	•	Get all attributes of the traversed nodes, especially for the infrastructure layer (i.e., CMDB context).

This will allow us to reconstruct a complete infrastructure and operational lineage associated with the application. The resulting subgraph will then be integrated into a graph-based memory for LLM agents to reason upon.

⸻

🔹 Toward a General Query Logic – Reusable Traversal Patterns

While this first query focuses on traversing from an Application to Incidents/Changes, our broader goal is to build a general GSQL query logic that we can reuse for other traversal types. For example:

Use Case #2 – From an Incident Back to Impacted Applications

In this variant:
	•	The starting point is an Incident.
	•	We want to traverse back through the infrastructure (e.g., via Cluster nodes),
	•	And identify the Applications that are associated with the incident, either directly or indirectly.

The logic is similar in spirit to Use Case #1, with the starting vertex type changed and the traversal inverted, but it should follow the same principles:
	•	Preserve all intermediate nodes in the traversal path.
	•	Return all relevant node attributes to reconstruct the full context.

⸻

I would like your help not only to write the first query, but also to help us define a clean and reusable GSQL pattern for such path-based traversal logic across the CMDB.

Let me know if you need any input regarding the schema or relationships.

Thanks a lot for your help!

Best regards,




CREATE DISTRIBUTED QUERY app_to_incidents_and_changes() FOR GRAPH UKG_V2 {

    MinAccum<INT> @distance = 1000;
    SumAccum<INT> @@target_visit_count;

    // Définition des types de nœuds et de relations autorisés
    SetAccum<STRING> @@v_types;
    SetAccum<STRING> @@e_types;

    @@v_types += "Application";
    @@v_types += "Cluster";
    @@v_types += "Incident";
    @@v_types += "Change";

    @@e_types += "USES";
    @@e_types += "IMPACTS";

    // Point de départ : Application avec l'attribut auid = "AP85343"
    verts = SELECT a
            FROM Application:a
            WHERE a.auid == "AP85343"
            POST-ACCUM a.@distance = 0;

    // Parcours BFS sans sens imposé sur les arêtes
    WHILE verts.size() > 0 LIMIT 10 DO
        verts = 
            SELECT t
            FROM verts:s -(@@e_types)-@@v_types:t
            WHERE t.@distance == 1000
            ACCUM t.@distance = s.@distance + 1;
    END;

    // Récupération des cibles atteintes : Incident et Change
    targets = 
        SELECT x
        FROM {Incident, Change}:x
        WHERE x.@distance < 1000;

    PRINT targets[x.@distance];
}


// Version OK
CREATE QUERY GetInfraFromApp(STRING auid, STRING env) FOR GRAPH UKG_V2 {
  // 1. Récupération de tous les vertices Application
  startApps = { Application.* };
  
  // 2. Filtrage sur l'attribut auid
  selApp =
    SELECT a
    FROM startApps AS a
    WHERE a.auid == auid;
  
  // 3. Navigation via l'arête USES vers l'application dans l'environnement spécifié
  envApps =
    SELECT a2
    FROM selApp AS a - (USES:e) -> Application AS a2
    WHERE a2.environment == env;
  
  // 4. Navigation via l'arête USES vers les Clusters
  resultClusters =
    SELECT c
    FROM envApps AS a2 - (USES:e2) -> Cluster AS c;
  
  // 5. Affichage du résultat
  PRINT resultClusters;
}

