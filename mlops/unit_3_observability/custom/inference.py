from typing import Dict, List, Tuple, Union

from sklearn.feature_extraction import DictVectorizer
from xgboost import Booster

from mlops.utils.data_preparation.feature_engineering import combine_features
from mlops.utils.models.xgboost import build_data

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

DEFAULT_INPUTS = [
    {
        # target = "duration": 11.5
        'DOLocationID': 239,
        'PULocationID': 236,
        'trip_distance': 1.98,
    },
    {
        # target = "duration" 20.8666666667
        'DOLocationID': '170',
        'PULocationID': '65',
        'trip_distance': 6.54,
    },
]


@custom
def predict(
    model_settings: Dict[str, Tuple[Booster, DictVectorizer]],
    **kwargs,
) -> List[float]:
    inputs: List[Dict[str, Union[float, int]]] = kwargs.get('inputs', DEFAULT_INPUTS)
    inputs = combine_features(inputs)

    DOLocationID = kwargs.get('DOLocationID')
    PULocationID = kwargs.get('PULocationID')
    trip_distance = kwargs.get('trip_distance')

    if DOLocationID is not None or PULocationID is not None or trip_distance is not None:
        inputs = [
            {
                'DOLocationID': DOLocationID,
                'PULocationID': PULocationID,
                'trip_distance': trip_distance,
            },
        ]
    
    model, vectorizer = model_settings['xgboost']
    vectors = vectorizer.transform(inputs)

    predictions = model.predict(build_data(vectors))

    for idx, input_feature in enumerate(inputs):
        print(f'Prediction of duration using these features: {predictions[idx]}')
        for key, value in inputs[idx].items():
            print(f'\t{key}: {value}')

    return predictions.tolist()
