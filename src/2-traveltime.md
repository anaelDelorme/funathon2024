---
theme: dashboard
title:  Temps de trajet
toc: false
---

<!-- Load and transform the data -->

```js
import { X_API_ID, X_API_KEY } from "./components/config.js";
const gare = FileAttachment("data/liste-des-gares.csv").dsv({delimiter: ";", typed: true});
const gare_geo = FileAttachment("data/liste-des-gares.geojson").json();
const grandesGares = ["Paris-Nord","Paris-Montparnasse","Paris-Gare-de-Lyon","Lyon-Perrache", "Marseille-St-Charles", "Toulouse-Matabiau", "Lille-Flandres", "Bordeaux-St-Jean", "Nice-Ville", "Nantes", "Strasbourg-Ville" , "Montpellier-St-Roch"]
```

<div class="grid grid-cols-2">
  <div class="card" >

<h1>Carte des gares des 10 grandes agglomérations françaises</h1>

```js
const gare_geo_filter = gare_geo.features.filter(gare => grandesGares.includes(gare.properties.libelle));
//console.log("Ttt",gare_geo_filter);

// logo à afficher
const img_train = [
  FileAttachment("img/train.png")
];

const div = display(document.createElement("div"));
div.style = "height: 400px;";

const map = L.map(div).setView([46.603354, 1.888334], 5);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.geoJSON(gare_geo_filter, {
    pointToLayer: function (feature, latlng) {
      return L.marker(latlng, {
        icon: L.icon({
          iconUrl: img_train[0].href,
          iconSize: [35, 35]
        })
      });
    },
    onEachFeature: function (feature, layer) {
      layer.bindPopup('<strong>' + feature.properties.libelle);
    }
  }).addTo(map);


```



```js
function extractCoordinatesFromGeoJSON(geojson) {
  return geojson.features.map(feature => ({
    libelle: feature.properties.libelle,
    lat: feature.properties.y_wgs84,
    lng: feature.properties.x_wgs84
  }));
}

let stations_data = extractCoordinatesFromGeoJSON(gare_geo);

function getStationCoordinates(station, data, verbose = true) {
  let coords;

  if (station !== "Strasbourg-Ville") {
    // Filter the data to find coordinates for the station
    let stationData = data.filter(item => item.libelle === station);
    
    // Extract latitude and longitude
    let lat = parseFloat(stationData[0].lat);
    let lng = parseFloat(stationData[0].lng);
    
    coords = [lat, lng];
  } else {
    // Default coordinates for "Strasbourg-Ville"
    coords = [48.584488, 7.735626];
  }

  // If verbose is true, display the coordinates
  if (verbose) {
    console.log(`${station} -> (${coords[0]}, ${coords[1]})`);
  }

  return coords;
}

```
</div>
  <div class="card" >

<h1> Temps de transport en train</h1>

```js
// Fonction pour capitaliser la première lettre de chaque mot et après chaque tiret
function capitalizeName(name) {
    return name
        .toLowerCase()
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('-');
}

const uniqueGareNoms = gare
    .map((gare) => capitalizeName(gare.libelle)) // Transformer les noms
    .filter((value, index, self) => self.indexOf(value) === index); // Garder uniquement les noms uniques

uniqueGareNoms.sort(); // Trier les noms


/*
const choix_gare_depart = view(Inputs.select(uniqueGareNoms, { value: "Paris-Montparnasse", label: "Choisir la gare de départ" }));
const choix_gare_arrivee = view(Inputs.select(uniqueGareNoms, { value: "Toulouse-Matabiau", label: "Choisir la gare d'arrivée" }));
*/
const choix_gare_depart = view(Inputs.select(grandesGares, { value: "Paris-Montparnasse", label: "Choisir la gare de départ" }));
const choix_gare_arrivee = view(Inputs.select(grandesGares, { value: "Toulouse-Matabiau", label: "Choisir la gare d'arrivée" }));
```

```js
let depart_coords = getStationCoordinates(choix_gare_depart, stations_data, false);
let arrivee_coords = getStationCoordinates(choix_gare_arrivee, stations_data, false);
const now = new Date();
const maxDate = new Date(now.getTime() + (14 * 24 * 60 * 60 * 1000)); // 2 semaines après aujourd'hui
const minDate = new Date(now.getTime() - (21 * 24 * 60 * 60 * 1000)); // 3 semaines avant aujourd'hui


const date_choisie = view(Inputs.datetime({
    label: "Moment",
    value: now.toISOString().slice(0, 16) ,
    min: minDate,
    max: maxDate
}));
console.log("datetime",date_choisie);

```
```js
console.log("datetime",date_choisie);

const xApiIdValue = X_API_ID;
const xApiKeyValue = X_API_KEY;

const headers = {
        'Content-Type': 'application/json',
        'X-Application-Id': xApiIdValue,
        'X-Api-Key': xApiKeyValue
    };
const routesApiUrl = 'https://api.traveltimeapp.com/v4/routes';
const requestBody = {
    locations: [
        {
            id: 'point-from',
            coords: {
                lat: depart_coords[0],
                lng: depart_coords[1]
            }
        },
        {
            id: 'point-to-1',
            coords: {
                lat: arrivee_coords[0],
                lng: arrivee_coords[1]
            }
        }
    ],
    departure_searches: [
        {
            id: 'departure-search',
            transportation: {
                type: 'public_transport'
            },
            departure_location_id: 'point-from',
            arrival_location_ids: [
                'point-to-1'
            ],
            departure_time: date_choisie,
            properties: [
                'travel_time',
                'route'
            ],
            range: {
                enabled: true,
                max_results: 5,
                width: 900
            }
        }
    ]
};
 let responseContent =[];
    try {
        const response = await fetch(routesApiUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(requestBody)
        });

        // Vérifier si la requête a été traitée avec succès
        if (response.ok) {
            //console.log('La requête a bien été traitée');
            responseContent = response.json();  
        } else {
            console.log(`Une erreur est survenue. Code de la réponse : ${response.status}`);
            console.log(response.json());  
        }
    } catch (error) {
        console.error('Erreur lors de la requête :', error);
    }


```

```js
let travel_time_hours;
let travel_time_minutes;

if (responseContent.results.length === 0 || responseContent.results[0].locations.length === 0) {
    travel_time_hours = Infinity;
} else {
    // Extraire les données de temps de trajet et trouver le temps de trajet minimum en heures
    const travel_times = responseContent.results[0].locations[0].properties.map(item => item.travel_time);
    const minTravelTimeInSeconds = Math.min(...travel_times);
    travel_time_hours = Math.floor(minTravelTimeInSeconds / 3600);
    travel_time_minutes = Math.floor((minTravelTimeInSeconds % 3600) / 60);

} 
```

Le temps de trajet est de **${travel_time_hours}** heures et **${travel_time_minutes}** minutes.

</div>
</div>