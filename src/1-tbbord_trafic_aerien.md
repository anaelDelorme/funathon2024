---
theme: dashboard
title:  Trafic aérien
toc: false
---
```js
import * as echarts from "npm:echarts";
```

# Tableau de bord du trafic aérien ✈️

<!-- Load and transform the data -->

```js
const airports = FileAttachment("data/airports.csv").csv({typed: true});
const companies = FileAttachment("data/companies.csv").csv({typed: true});
const liaisons = FileAttachment("data/liaisons.csv").csv({typed: true});
let airports_location = FileAttachment("data/airports_location.json").json();
```


<div class="grid grid-cols-2">
  <div class="card  grid-colspan-2">
<h1>Fréquentation des Aéroports</h1>

```js
// Fonction pour capitaliser la première lettre de chaque mot et après chaque tiret
function capitalizeName(name) {
    return name
        .toLowerCase()
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('-');
}

const uniqueAptNoms = airports
    .map((airport) => capitalizeName(airport.apt_nom)) // Transformer les noms
    .filter((value, index, self) => self.indexOf(value) === index); // Garder uniquement les noms uniques

uniqueAptNoms.sort(); // Trier les noms

const choix_aeroport = view(Inputs.select(uniqueAptNoms, { value: "Toulouse-Blagnac", label: "Choisir l'aéroport" }));

```

```js
const filteredAirports = airports.filter((airport) => airport.apt_nom === choix_aeroport.toUpperCase());
const myChart = echarts.init(display(html`<div style="width: 100%; height:400px;"></div>`));
let data = filteredAirports;
data = data.map(entry => ({ date: entry.date, trafic: entry.trafic }));
data.forEach((entry) => {
  entry.date = Date.parse(entry.date);
});
const option = {
  title: {
    text: 'Trafic de '+ choix_aeroport,
  },
  tooltip: {
    formatter: function (params) {
      const date = new Date(params.value[0]);
      const formattedDate = "Date: "+ `${date.getMonth() + 1}-${date.getFullYear()}`; // Format MM-AAAA
      const trafic = params.value[1];
      const formattedTrafic = trafic.toLocaleString('fr-FR');
      return `${formattedDate} <br/> Trafic: ${formattedTrafic}`;
    },
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'time',
    axisLabel: {
      formatter: function (value) {
        const date = new Date(value);
        const day = date.getDate();
        const month = date.getMonth() + 1; // Les mois sont indexés à partir de 0
        const year = date.getFullYear();
        return `${month}-${year}`;
      },
    },
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: function (value) {
        return value.toLocaleString('fr-FR');
      }
    }
  },
  series: [
    {
      name: "Trafic",
      type: 'line',
      itemStyle: {
        color: 'rgb(120,44,241)'
      },
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(120, 44, 241)'
          },
          {
            offset: 1,
            color: 'rgb(248,248,248)'
          }
        ])
      },
      data: data.map(entry => [entry.date, entry.trafic]),
    },
  ],
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      start: 0,
      end: 100
    }
  ],
};
myChart.setOption(option);

```

  
  </div>
<div class="card">
  
<h1>Statistiques de fréquentations par mois</1>

```js
// Liste déroulante pour choisir le mois
const moisAnUniques = [...new Set(airports.map(item => `${item.mois}-${item.an}`))];
const choix_date = view(Inputs.select(moisAnUniques, { label: "Choisir le mois: " }));
```

```js
// Tableau filtré
const [mois, an] = choix_date.split('-');
const airports_filtres = airports.filter((airport) => airport.mois === parseInt(mois) && airport.an === parseInt(an));

```

```js
//Fonction pour afficher les barres horizontales proportionnelles dans le tableau
function sparkbar(max) {
  return (x) => htl.html`<div style="
    background: lightsteelblue;
    color: black;
    width: ${100 * x / max}%;
    float: right;
    padding-right: 3px;
    box-sizing: border-box;
    overflow: visible;
    display: flex;
    justify-content: end;">${(Math.round(x / 100)*100).toLocaleString('fr-FR', { useGrouping: true })}`
}



//Affichage du tableau formaté
display(Inputs.table(airports_filtres, {
  columns: [
    "apt_nom",
    "apt_pax_dep",
    "apt_pax_arr",
    "apt_pax_tr"
  ],
  header: {
    apt_nom: "Aéroport",
    apt_pax_dep: "Départ (nombre de passagers)",
    apt_pax_arr: "Arrivée (nombre de passagers)",
    apt_pax_tr: "Transit (nombre de passagers)"
  },
  sort: "apt_pax_dep", 
  reverse: true,
  format: {
    apt_nom: (x) => x.split(/[\s-]/).map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' '),
    apt_pax_dep: sparkbar(d3.max(airports_filtres, d => d.apt_pax_dep)),
    apt_pax_arr: sparkbar(d3.max(airports_filtres, d => d.apt_pax_arr)),
    apt_pax_tr: sparkbar(d3.max(airports_filtres, d => d.apt_pax_tr))
  }
  })
);

```

  
  </div>


  <div class="card">
  
<h1>Fréquentation des aéroports par mois</h1>

<i>Choix du mois dans les statistiques de fréquentations par mois</i>
 

```js
// logo à afficher
const img_airport = [
  FileAttachment("img/airport_green.png"),
  FileAttachment("img/airport_blue.png"),
  FileAttachment("img/airport_red.png")
];

const div = display(document.createElement("div"));
div.style = "height: 400px;";

const map = L.map(div).setView([51.505, -0.09], 4);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Fonction pour créer une couche GeoJSON
function createGeoJSONLayer(data) {
  return L.geoJSON(data, {
    pointToLayer: function (feature, latlng) {
      let iconUrl;
      const trafic = feature.properties.trafic;

      // Déterminer le tercile et sélectionner l'icône appropriée
      if (trafic <= terciles[0]) {
        iconUrl = img_airport[0].href;
      } else if (trafic <= terciles[1]) {
        iconUrl = img_airport[1].href;
      } else {
        iconUrl = img_airport[2].href;
      }

      return L.marker(latlng, {
        icon: L.icon({
          iconUrl: iconUrl,
          iconSize: [50, 50],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        })
      });
    },
    onEachFeature: function (feature, layer) {
      layer.bindPopup('<strong>' + feature.properties.Nom + '</strong><br>' +
        'Code IATA: ' + feature.properties['Code.IATA'] + '<br>' +
        'Code OACI: ' + feature.properties['Code.OACI'] + '<br>' +
        'Trafic: ' + feature.properties.trafic);
    }
  });
}

// Fonction pour calculer les terciles
function calculateTerciles(data) {
  const traficValues = data.features.map(feature => feature.properties.trafic);
  traficValues.sort((a, b) => a - b);

  const tercile1 = traficValues[Math.floor(traficValues.length / 3)];
  const tercile2 = traficValues[Math.floor(2 * traficValues.length / 3)];

  return [tercile1, tercile2];
}

// Initialisation des terciles
let terciles = calculateTerciles(airports_location);

// Initialisation de la couche GeoJSON
let geoJsonLayer = createGeoJSONLayer(airports_location);
geoJsonLayer.addTo(map);

// Fonction pour mettre à jour la couche GeoJSON
function updateGeoJSONLayer() {
  // Mettre à jour les propriétés des features
  airports_location.features.forEach(feature => {
    const codeOACI = feature.properties['Code.OACI'];
    const matchingAirport = airports_filtres.find(airport => airport.apt === codeOACI);
    if (matchingAirport) {
      feature.properties.trafic = matchingAirport.trafic;
    }
  });

  // Recalculer les terciles
  terciles = calculateTerciles(airports_location);

  // Supprimer l'ancienne couche
  map.removeLayer(geoJsonLayer);

  // Ajouter la nouvelle couche avec les données mises à jour
  geoJsonLayer = createGeoJSONLayer(airports_location);
  geoJsonLayer.addTo(map);
}

// Exemple d'appel de la fonction de mise à jour
updateGeoJSONLayer();


```



</div>




</div>

