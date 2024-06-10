import requests
from io import BytesIO
from typing import List

import pandas as pd


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    response = requests.get("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet")

    if response.status_code != 200:
        raise Exception(response.text)

    df = pd.read_parquet(BytesIO(response.content))
    
    return df