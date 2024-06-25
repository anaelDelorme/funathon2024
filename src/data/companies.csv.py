import pandas as pd
import sys
from create_data_list import create_data_list
from clean_dataframe import clean_dataframe

urls = create_data_list("./sources.yml")
col_types = {
  "ANMOIS": "str",
  "CIE": "str",
  "CIE_NOM": "str",
  "CIE_NAT": "str",
  "CIE_PAYS": "str"
}

compagnies_all = pd.concat([
        pd.read_csv(file, delimiter = ';', dtype = col_types)
        for file in list(urls['compagnies'].values())
        ])
compagnies_all = clean_dataframe(compagnies_all)


compagnies_all.to_csv(sys.stdout)
