import pandas as pd
import sys
from create_data_list import create_data_list
from clean_dataframe import clean_dataframe

urls = create_data_list("./sources.yml")
col_types = {
  "ANMOIS": "str",
  "LSN": "str",
  "LSN_DEP_NOM": "str",
  "LSN_ARR_NOM": "str",
  "LSN_SCT": "str",
  "LSN_FSC": "str"
}

liaisons_all = pd.concat([
        pd.read_csv(file, delimiter = ';', dtype = col_types)
        for file in list(urls['liaisons'].values())
        ])
liaisons_all = clean_dataframe(liaisons_all)


liaisons_all.to_csv(sys.stdout)
