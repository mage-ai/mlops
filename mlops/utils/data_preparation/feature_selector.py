from typing import List, Optional

import pandas as pd

CATEGORICAL_FEATURES = ['PU_DO']
NUMERICAL_FEATURES = ['trip_distance']


def select_features(df: pd.DataFrame, features: Optional[List[str]] = None) -> pd.DataFrame:
    columns = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    if features:
        columns += features

    return df[columns]
