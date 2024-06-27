---
theme: dashboard
title:  Temps de trajet
toc: false
---

<!-- Load and transform the data -->

```js
import { X_API_ID, X_API_KEY } from "./components/config.js";
import { getStationCoordinates, fetchTravelTime, getAirTrafficBetweenCities } from "./components/timetravel.js";
const air_traffic = FileAttachment("data/air_traffic.csv").csv({typed: true});

const gare = FileAttachment("data/liste-des-gares.csv").dsv({delimiter: ";", typed: true});
const gare_geo = FileAttachment("data/liste-des-gares.geojson").json();
const grandesGares = ["Paris-Nord","Paris-Montparnasse","Paris-Gare-de-Lyon","Lyon-Perrache", "Marseille-St-Charles", "Toulouse-Matabiau", "Lille-Flandres", "Bordeaux-St-Jean", "Nice-Ville", "Nantes", "Strasbourg-Ville" , "Montpellier-St-Roch"];
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
const now = new Date();
const maxDate = new Date(now.getTime() + (14 * 24 * 60 * 60 * 1000)); // 2 semaines après aujourd'hui
const minDate = new Date(now.getTime() - (21 * 24 * 60 * 60 * 1000)); // 3 semaines avant aujourd'hui


const date_choisie = view(Inputs.datetime({
    label: "Choisir le départ: ",
    value: now.toISOString().slice(0, 16) ,
    min: minDate,
    max: maxDate
}));
```

```js
let depart_coords = getStationCoordinates(choix_gare_depart, stations_data, false);
let arrivee_coords = getStationCoordinates(choix_gare_arrivee, stations_data, false);
```
```js
const travel_time = fetchTravelTime(depart_coords, arrivee_coords, date_choisie)
```
```js
let travel_time_hours = travel_time.hours;
let travel_time_minutes = travel_time.minutes;
```
Le temps de trajet est de **${travel_time_hours}** heures et **${travel_time_minutes}** minutes.

```js
const city1 = choix_gare_depart.split('-')[0].trim();
const city2 = choix_gare_arrivee.split('-')[0].trim();

const airTraffic_entre_gare_choisie = getAirTrafficBetweenCities(city1, city2, air_traffic);

const passagersFormatted = airTraffic_entre_gare_choisie.passagers.toLocaleString();
const gainC02Formatted = airTraffic_entre_gare_choisie.gain_C02.toLocaleString();

```

🌍🌡️ En 2019, le trafic arérien entre ${city1} et ${city2} est de ${passagersFormatted} personnes.  ✈️   
Si toutes ces personnes avaient pris le train, ${gainC02Formatted} tonnes d'équivalent CO2 auraient été économisés! 💚

</div>

</div>



