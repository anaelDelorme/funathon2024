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
const airports_location = FileAttachment("data/airports_location.json").json()
```

<div class="grid grid-cols-2">
  <div class="card">
<h1>Fréquentation des Aéroports</h1>

```js
const uniqueAptNoms = airports
    .map((airport) => airport.apt_nom)
    .filter((value, index, self) => self.indexOf(value) === index);
uniqueAptNoms.sort();
const choix_aeroport = view(Inputs.select(uniqueAptNoms, { value: "TOULOUSE-BLAGNAC", label: "Choisir l'aéroport" }));
```

```js
/*plot non affiché
const plot = Plot.plot({
  y: {grid: true},
  marks: [
    () => htl.svg`<defs>
      <linearGradient id="gradient" gradientTransform="rotate(90)">
        <stop offset="20%" stop-color="steelblue" stop-opacity="0.5" />
        <stop offset="100%" stop-color="brown" stop-opacity="0" />
      </linearGradient>
    </defs>`,
    Plot.areaY(filteredAirports, {x: "date", y: "trafic", fill: "url(#gradient)"}),
    Plot.lineY(filteredAirports, {x: "date", y: "trafic", stroke: "steelblue"}),
    Plot.ruleY([0])
  ]
})
*/
```

```js
const filteredAirports = airports.filter((airport) => airport.apt_nom === choix_aeroport);
const myChart = echarts.init(display(html`<div style="width: 600px; height:400px;"></div>`));
let data = filteredAirports;
data = data.map(entry => ({ date: entry.date, trafic: entry.trafic }));
data.forEach((entry) => {
  entry.date = Date.parse(entry.date);
});
console.log(data);
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
  
<h1>Carte</h1>

```js

const mergedTable = airports_location.join(airports, { on: 'apt' });


```


```js
const div = display(document.createElement("div"));
div.style = "height: 400px;";

const map = L.map(div)
  .setView([51.505, -0.09], 2);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})
  .addTo(map);

L.marker([51.5, -0.09])
  .addTo(map)
  .bindPopup("A nice popup<br> indicating a point of interest.")
  .openPopup();


L.geoJSON(airports_location, {
    // Définir les options de style des marqueurs
    pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {
            icon: L.icon({
                iconUrl: '_file/img/airport.png',
                iconSize: [50, 50],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            })
        });
    },
    // Ajouter un popup avec les informations de chaque point
    onEachFeature: function (feature, layer) {
        layer.bindPopup('<strong>' + feature.properties.Nom + '</strong><br>' +
            'Code IATA: ' + feature.properties['Code.IATA'] + '<br>' +
            'Code OACI: ' + feature.properties['Code.OACI'] + '<br>' +
            'Trafic: ' + feature.properties.trafic);
    }
}).addTo(map); 
```

</div>


<div class="card grid-colspan-2">
  
<h1>Statistique de fréquentations par mois</1>

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
    apt_pax_dep: "Passagers au départ",
    apt_pax_arr: "Passagers à l'arrivée",
    apt_pax_tr: "Passagers en transit"
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

</div>


## Compagnies

```js
Inputs.table(companies)
```

##  Liaisons

```js
Inputs.table(liaisons)
```
