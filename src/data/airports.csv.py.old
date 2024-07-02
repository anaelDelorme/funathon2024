import pandas as pd
import sys
from create_data_list import create_data_list
from clean_dataframe import clean_dataframe

urls = create_data_list("./sources.yml")
col_types = {
    "ANMOIS": "str",  
    "APT": "str",     
    "APT_NOM": "str", 
    "APT_ZON": "str",
}

pax_apt_all = pd.concat([
        pd.read_csv(file, delimiter = ';', dtype = col_types)
        for file in list(urls['airports'].values())
        ])
pax_apt_all = clean_dataframe(pax_apt_all)

pax_apt_all['trafic'] = pax_apt_all['apt_pax_dep'] + \
  pax_apt_all['apt_pax_tr'] + \
  pax_apt_all['apt_pax_arr']

pax_apt_all['date'] = pd.to_datetime(
  pax_apt_all['anmois'] + '01', format='%Y%m%d'
)


pax_apt_all.to_csv(sys.stdout)
