
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    

    independent_variable = ["PULocationID", "DOLocationID"]
    target_variable = ["duration"]


    dataset_dict = data[independent_variable].to_dict(orient="records")

    dict_vectorizer = DictVectorizer()

    X_train = dict_vectorizer.fit_transform(dataset_dict)

    print(X_train.shape)
    print(X_train.shape)

    Y_train = data[target_variable].values
    
    print("Train_shape: ", X_train.shape)
    print("Y_train_shape: ", Y_train.shape)

    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    print(model.intercept_)

    return dict_vectorizer, model


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'