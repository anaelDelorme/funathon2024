#!/bin/bash

# Lire le fichier sources.yml
file="sources.yml"

# Rechercher la ligne du geojson airport
traveltime_line=$(grep "traveltime:$" "$file" -A1 | tail -n1 | tr -d ' ')

# Extraire l'URL du geojson airport
traveltime_url=$(echo "$traveltime_line" | cut -d '"' -f 2)

# Faire un curl de l'URL du geojson airport
curl "$traveltime_url" 