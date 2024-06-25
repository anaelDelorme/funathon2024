#!/bin/bash

# Lire le fichier sources.yml
file="sources.yml"

# Rechercher la ligne du geojson airport
geojson_line=$(grep "geojson:$" "$file" -A1 | tail -n1 | tr -d ' ')

# Extraire l'URL du geojson airport
geojson_url=$(echo "$geojson_line" | cut -d '"' -f 2)

# Faire un curl de l'URL du geojson airport
curl "$geojson_url"