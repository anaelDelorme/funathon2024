import yaml
import requests

def get_travel_time_api_response(url, request_body):
    source_file = "../../secrets.yaml"

    # Charger les secrets depuis le fichier YAML
    with open(source_file, 'r') as file:
        secrets = yaml.safe_load(file)

    x_api_id_value = secrets['travelTime']['X_API_ID']
    x_api_key_value = secrets['travelTime']['X_API_KEY']

    # Définir les en-têtes pour la requête
    headers = {
        "Content-Type": "application/json",
        "X-Application-Id": x_api_id_value,
        "X-Api-Key": x_api_key_value
    }

    # Effectuer la requête POST à l'API TravelTime
    response = requests.post(url, json=request_body, headers=headers)

    # Vérifier si la requête a été traitée avec succès
    if response.status_code == 200:
        print("La requête a bien été traitée")
        return response.json()  # Retourner la réponse JSON
    else:
        print(f"Une erreur est survenue. Code de la réponse : {response.status_code}")
        print(response.json())  # Afficher plus de détails sur l'erreur
        return None  # Retourner None en cas d'erreur

# Exemple d'utilisation de la fonction

routes_api_url = "https://api.traveltimeapp.com/v4/routes"

request_body = {
    "locations": [
        {
            "id": "point-from",
            "coords": {
                "lat": 51.5119637,
                "lng": -0.1279543
            }
        },
        {
            "id": "point-to-1",
            "coords": {
                "lat": 51.5156177,
                "lng": -0.0919983
            }
        }
    ],
    "departure_searches": [
        {
            "id": "departure-search",
            "transportation": {
                "type": "public_transport"
            },
            "departure_location_id": "point-from",
            "arrival_location_ids": [
                "point-to-1"
            ],
            "departure_time": "2024-06-26T18:00:00.000Z",
            "properties": [
                "travel_time",
                "route"
            ],
            "range": {
                "enabled": True,
                "max_results": 5,
                "width": 900
            }
        }
    ]
}

# Appeler la fonction avec l'URL de l'API et le corps de la requête
response_content = get_travel_time_api_response(routes_api_url, request_body)

if response_content:
    print(response_content)