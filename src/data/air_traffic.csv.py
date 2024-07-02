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
url_airtraffics = urls.get("airtraffic", {}).get("Tout")


# Télécharger le fichier Parquet
response = requests.get(url_airtraffics)

with open("asp-lsn.parquet", "wb") as parquet_file:
    parquet_file.write(response.content)

# Lire les données depuis le fichier Parquet
airtraffic = pd.read_parquet("asp-lsn.parquet")
# Nettoyer les données (si nécessaire)
airtraffic = clean_dataframe(airtraffic)

# print(airtraffic.columns)
# Exporter les données au format CSV (ou autre format si nécessaire)
airtraffic.to_csv(sys.stdout, index=False)

