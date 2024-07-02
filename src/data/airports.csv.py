import pandas as pd
import sys
import yaml
import requests
from create_data_list import create_data_list
from clean_dataframe import clean_dataframe

# Charger les URLs à partir du fichier YAML
with open("./sources.yml", "r") as yaml_file:
    urls = yaml.safe_load(yaml_file)

# Récupérer l'URL des aéroports (parquet)
url_airports = urls.get("airports", {}).get("Tout")


# Télécharger le fichier Parquet
response = requests.get(url_airports)

with open("asp-lsn.parquet", "wb") as parquet_file:
    parquet_file.write(response.content)

# Lire les données depuis le fichier Parquet
pax_apt_all = pd.read_parquet("asp-lsn.parquet")
# Nettoyer les données (si nécessaire)
pax_apt_all = clean_dataframe(pax_apt_all)

# Calculer la colonne 'trafic'
pax_apt_all['trafic'] = pax_apt_all['APT_PAX_dep'] + \
                        pax_apt_all['APT_PAX_tr'] + \
                        pax_apt_all['APT_FRP_arr']

# Convertir la colonne 'anmois' en chaîne de caractères
pax_apt_all['ANMOIS'] = pax_apt_all['ANMOIS'].astype(str)

# Convertir la colonne 'anmois' en datetime
pax_apt_all['date'] = pd.to_datetime(pax_apt_all['ANMOIS'] + '01', format='%Y%m%d')

# Exporter les données au format CSV (ou autre format si nécessaire)
pax_apt_all.to_csv(sys.stdout, index=False)
