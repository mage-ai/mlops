from typing import Dict, Tuple, Union

from pandas import Series
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator
from xgboost import Booster

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def source(
    training_results: Tuple[Booster, BaseEstimator],
    settings: Tuple[
        Dict[str, Union[bool, float, int, str]],
        csr_matrix,
        Series,
    ],
    **kwargs,
) -> Tuple[Booster, csr_matrix, csr_matrix]:
    model, _ = training_results
    _, X_train, y_train = settings

    return model, X_train, y_train
