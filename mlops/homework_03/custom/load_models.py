from typing import List, Dict, Tuple

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def models(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    model_names: str = kwargs.get(
        "models", 'linear_model.LinearRegression'
    )
    child_data: List[str] = [
        model_name.strip() for model_name in model_names.split(',')
    ]

    child_metadata: List[Dict] = [
        dict(block_uuid=model_name.split('.')[-1]) for model_name in child_data
    ]
    
    return child_data, child_metadata


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
