from typing import Dict, Tuple, Union

from pandas import Series
from scipy.sparse._csr import csr_matrix
from xgboost import Booster

from mlops.utils.models.xgboost import build_data, fit_model

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def train(
    training_set: Dict[str, Union[Series, csr_matrix]],
    settings: Tuple[
        Dict[str, Union[bool, float, int, str]],
        csr_matrix,
        Series,
    ],
    **kwargs,
) -> Tuple[Booster, csr_matrix, Series]:
    hyperparameters, X, y = settings

    # Test training a model with low max depth
    # so that the output renders a reasonably sized plot tree.
    if kwargs.get('max_depth'):
        hyperparameters['max_depth'] = int(kwargs.get('max_depth'))

    model = fit_model(
        build_data(X, y),
        hyperparameters,
        verbose_eval=kwargs.get('verbose_eval', 100),
    )

    # DictVectorizer to transform features for online inference.
    vectorizer = training_set['build'][6]
    return model, vectorizer
