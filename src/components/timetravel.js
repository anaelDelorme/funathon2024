import { X_API_ID, X_API_KEY } from "./config.js";

export function getStationCoordinates(station, data, verbose = true) {
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
  };


export async function fetchTravelTime(depart_coords, arrivee_coords, date_choisie) {
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
                coords: { lat: depart_coords[0], lng: depart_coords[1] }
            },
            {
                id: 'point-to-1',
                coords: { lat: arrivee_coords[0], lng: arrivee_coords[1] }
            }
        ],
        departure_searches: [{
            id: 'departure-search',
            transportation: { type: 'public_transport' },
            departure_location_id: 'point-from',
            arrival_location_ids: ['point-to-1'],
            departure_time: date_choisie,
            properties: ['travel_time', 'route'],
            range: {
                enabled: true,
                max_results: 5,
                width: 900
            }
        }]
    };

    let responseContent = [];
    try {
        const response = await fetch(routesApiUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(requestBody)
        });

        if (response.ok) {
            responseContent = await response.json();
        } else {
          //  console.log(`Une erreur est survenue. Code de la réponse : ${response.status}`);
            return null; // ou gérer l'erreur comme vous préférez
        }
    } catch (error) {
//console.error('Erreur lors de la requête :', error);
        return null; // ou gérer l'erreur comme vous préférez
    }

    if (responseContent.results.length === 0 || responseContent.results[0].locations.length === 0) {
        return { hours: Infinity, minutes: Infinity };

    } else {
        const travel_times = responseContent.results[0].locations[0].properties.map(item => item.travel_time);
        const minTravelTimeInSeconds = Math.min(...travel_times);
        const hours = Math.floor(minTravelTimeInSeconds / 3600);
        const minutes = Math.floor((minTravelTimeInSeconds % 3600) / 60);
       /* console.log("travel_times",travel_times);
        console.log("minTravelTimeInSeconds",minTravelTimeInSeconds);
        console.log("hours",hours);
        console.log("minutes",minutes);*/

        return { hours, minutes };
    }
};




export function getAirTrafficBetweenCities(city1, city2, data) {
    // Convertir les noms de ville en minuscule pour les comparaisons insensibles à la casse
    const lowerCity1 = city1.toLowerCase();
    const lowerCity2 = city2.toLowerCase();

    // Filtrer les données pour inclure uniquement les vols entre city1 et city2 dans les deux sens
    const filteredData = data.filter(row => {

      const depCity = row.LSN_DEP_NOM.toLowerCase();
      const arrCity = row.LSN_ARR_NOM.toLowerCase();
      return (
        (depCity.includes(lowerCity1) && arrCity.includes(lowerCity2)) ||
        (depCity.includes(lowerCity2) && arrCity.includes(lowerCity1))
      );
    });
    
    //console.log("filteredData", filteredData);
    const passagers = filteredData.reduce((sum, row) => {
        return sum + row.LSN_PAX_loc
      }, 0);
    // Calculer le trafic total (PKT) en multipliant LSN_DIST par LSN_PAX_loc pour chaque ligne filtrée
    const totalTraffic = filteredData.reduce((sum, row) => {
      return sum + (row.LSN_DIST * row.LSN_PAX_loc);
    }, 0);
    //console.log("totalTraffic", filteredData);
    const GCO2_PER_PKT = 80;
    const gain_C02 = totalTraffic * GCO2_PER_PKT / 1000000;

    return {passagers, gain_C02};
  }