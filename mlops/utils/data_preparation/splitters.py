from typing import List, Tuple, Union

from pandas import DataFrame, Index


def split_on_value(
    df: DataFrame,
    feature: str,
    value: Union[float, int, str],
    drop_feature: bool = True,
    return_indexes: bool = False,
) -> Union[Tuple[DataFrame, DataFrame], Tuple[Index, Index]]:
    df_train = df[df[feature] < value]
    df_val = df[df[feature] >= value]

    if return_indexes:
        return df_train.index, df_val.index

    if drop_feature:
        df_train = df_train.drop(columns=[feature])
        df_val = df_val.drop(columns=[feature])

    return df_train, df_val
