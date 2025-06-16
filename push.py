Je cherche à construire une requête GSQL à partir d’un nœud Application dont l’attribut auid est "AP85343".

L’objectif est de parcourir les vertex de type Application, Cluster, Incident, et Change, et de récupérer :
	•	tous les incidents (Incident) et changements (Change) atteignables depuis cette application,
	•	mais aussi tous les vertex du chemin emprunté pour les atteindre (y compris les clusters ou autres applications traversées).

Je te laisse libre sur les choix de sens de parcours ou de modélisation, mais l’idée est bien d’avoir une vue complète sur les éléments traversés pour aboutir aux incidents et changements liés à l’application.

Merci d’avance pour ton aide !





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

