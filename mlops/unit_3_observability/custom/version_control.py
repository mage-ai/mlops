if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def git(*args, **kwargs):
    pass