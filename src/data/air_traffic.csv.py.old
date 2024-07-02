import pandas as pd
import sys
from create_data_list import create_data_list
from clean_dataframe import clean_dataframe

urls = create_data_list("./sources.yml")

airTraffic = pd.concat([
        pd.read_csv(file, delimiter = ';')
        for file in list(urls['airtraffic'].values())
        ])
airTraffic = clean_dataframe(airTraffic)

airTraffic.to_csv(sys.stdout)
