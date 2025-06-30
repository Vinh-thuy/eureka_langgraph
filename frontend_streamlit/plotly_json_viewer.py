import json
import plotly.io as pio
import plotly.graph_objects as go
import ast # Ajout de l'import pour ast.literal_eval

def view_plotly_json(json_file_path):
    """
    Charge un fichier JSON contenant les données d'un graphique Plotly et l'affiche.

    Args:
        json_file_path (str): Chemin vers le fichier JSON du graphique Plotly.
    """
    try:
        with open(json_file_path, 'r') as f:
            content = f.read().strip()
        
        # Tente d'extraire la partie liste Python si la ligne ressemble à un log du backend
        if content.startswith("[ORCHESTRATEUR] Contenu de 'generated_chart': "):
            list_str = content[len("[ORCHESTRATEUR] Contenu de 'generated_chart': "):]
        else:
            list_str = content

        # Utiliser ast.literal_eval pour évaluer la chaîne comme une liste Python
        # C'est plus sûr que eval() pour les données non fiables.
        chart_data = ast.literal_eval(list_str)

        # Assurez-vous que chart_data est bien une liste
        if not isinstance(chart_data, list):
            raise ValueError("Le contenu évalué n'est pas une liste.")

        for i, chart_json_str in enumerate(chart_data):
            print(f"\n--- Affichage du graphique {i+1} ---")
            try:
                # Assurez-vous que chart_json_str est bien une chaîne JSON
                if isinstance(chart_json_str, dict):
                    fig = go.Figure(chart_json_str)
                elif isinstance(chart_json_str, str):
                    fig = pio.from_json(chart_json_str)
                else:
                    print(f"Erreur: Type de données inattendu pour le graphique {i+1}: {type(chart_json_str)}")
                    continue
                
                fig.show()
                print(f"Graphique {i+1} affiché avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'affichage du graphique {i+1}: {e}")
                print(f"Contenu JSON du graphique {i+1} qui a échoué: {chart_json_str}")

    except FileNotFoundError:
        print(f"Erreur: Le fichier '{json_file_path}' n'a pas été trouvé.")
    except (ValueError, SyntaxError, ast.ValueError, ast.SyntaxError) as e:
        print(f"Erreur lors de l'évaluation de la chaîne Python ou du décodage JSON dans '{json_file_path}': {e}. Assurez-vous que le fichier contient une liste Python valide de chaînes JSON Plotly ou une ligne de log Plotly complète.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python plotly_json_viewer.py <chemin_vers_fichier_json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    view_plotly_json(json_path)
