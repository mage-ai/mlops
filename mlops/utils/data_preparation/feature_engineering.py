from typing import Dict, List, Union

from pandas import DataFrame


def combine_features(df: Union[List[Dict], DataFrame]) -> Union[List[Dict], DataFrame]:
    if isinstance(df, DataFrame):
        df['PU_DO'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)
    elif isinstance(df, list) and len(df) >= 1 and isinstance(df[0], dict):
        arr = []
        for row in df:
            row['PU_DO'] = str(row['PULocationID']) + '_' + str(row['DOLocationID'])
            arr.append(row)
        return arr
    return df
