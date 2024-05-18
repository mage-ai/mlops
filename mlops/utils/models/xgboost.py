import json
import os
from typing import Callable, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
import scipy
import xgboost as xgb
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.metrics import mean_squared_error
from xgboost import Booster, DMatrix

from mlops.utils.hyperparameters.shared import build_hyperparameters_space

HYPERPARAMETERS_WITH_CHOICE_INDEX = []


def fit_model(
    training_set: np.ndarray,
    hyperparameters: Dict,
    verbose_eval: Union[bool, int] = 10,
) -> Booster:
    num_boost_round = int(hyperparameters.pop('num_boost_round'))

    model, _, _ = train_model(
        training_set,
        training_set,
        early_stopping_rounds=1,
        hyperparameters=hyperparameters,
        num_boost_round=num_boost_round,
        verbose_eval=verbose_eval,
    )

    return model


def build_data(
    X: scipy.sparse._csr.csr_matrix, y: Optional[pd.Series] = None
) -> np.ndarray:
    return DMatrix(X, y)


def train_model(
    training_set: np.ndarray,
    validation_set: np.ndarray,
    early_stopping_rounds: Optional[int] = 50,
    hyperparameters: Dict = {},
    num_boost_round: int = 1000,
    verbose_eval: Union[bool, int] = 10,
) -> Tuple[Booster, Dict[str, float], np.ndarray]:
    if 'max_depth' in hyperparameters:
        hyperparameters['max_depth'] = int(hyperparameters['max_depth'])

    model = xgb.train(
        hyperparameters,
        training_set,
        early_stopping_rounds=early_stopping_rounds,
        evals=[(validation_set, 'validation')],
        num_boost_round=num_boost_round,
        verbose_eval=verbose_eval,
    )

    y_pred = model.predict(validation_set)

    y_val = validation_set.get_label()  # Corrected to extract labels from DMatrix
    rmse = mean_squared_error(y_val, y_pred, squared=False)
    mse = mean_squared_error(y_val, y_pred, squared=True)

    return model, dict(mse=mse, rmse=rmse), y_pred


def tune_hyperparameters(
    training_set: np.ndarray,
    validation_set: np.ndarray,
    callback: Optional[Callable[..., None]] = None,
    early_stopping_rounds: int = 50,
    max_evaluations: int = 50,
    random_state: int = 42,
    verbose_eval: int = 10,
    verbosity: int = 1,
    **kwargs,
) -> Dict:
    def __objective(
        params: Dict,
        early_stopping_rounds=early_stopping_rounds,
        training_set=training_set,
        validation_set=validation_set,
        verbosity=verbosity,
    ) -> Dict[str, Union[float, str]]:
        # Separate the num_boost_round from the normal hyperparameters because it's not a
        # hyperparameter but instead a parameter of the train function.
        num_boost_round = int(params.pop('num_boost_round'))

        model, metrics, predictions = train_model(
            training_set,
            validation_set,
            early_stopping_rounds=early_stopping_rounds,
            hyperparameters={**params, **dict(verbosity=verbosity)},
            num_boost_round=num_boost_round,
            verbose_eval=verbose_eval,
        )

        if callback:
            callback(
                hyperparameters=params,
                metrics=metrics,
                model=model,
                predictions=predictions,
            )

        return dict(loss=metrics['rmse'], status=STATUS_OK)

    space, choices = build_hyperparameters_space(Booster, random_state=random_state)

    best_hyperparameters: Dict = fmin(
        algo=tpe.suggest,
        fn=__objective,
        max_evals=max_evaluations,
        space=space,
        trials=Trials(),
    )

    # Convert choice index to choice value.
    for key in HYPERPARAMETERS_WITH_CHOICE_INDEX:
        if key in best_hyperparameters and key in choices:
            idx = int(best_hyperparameters[key])
            best_hyperparameters[key] = choices[key][idx]

    # fmin will return max_depth as a float for some reason
    if 'max_depth' in best_hyperparameters:
        best_hyperparameters['max_depth'] = int(best_hyperparameters['max_depth'])

    return best_hyperparameters


def load_model(model_dir: str, model_filename: str, config_filename: str) -> Booster:
    model_path = os.path.join(model_dir, model_filename)
    model = Booster()
    model.load_model(model_path)

    config_path = os.path.join(model_dir, config_filename)
    with open(config_path, 'r') as file:
        model_config = json.load(file)

    model_config_str = json.dumps(model_config)
    model.load_config(model_config_str)

    return model
