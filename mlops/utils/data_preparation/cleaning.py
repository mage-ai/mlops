import pandas as pd


def clean(
    df: pd.DataFrame,
    include_extreme_durations: bool = False,
) -> pd.DataFrame:
    # Convert pickup and dropoff datetime columns to datetime type
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    # Calculate the trip duration in minutes
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    if not include_extreme_durations:
        # Filter out trips that are less than 1 minute or more than 60 minutes
        df = df[(df.duration >= 1) & (df.duration <= 60)]

    # Convert location IDs to string to treat them as categorical features
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    return df
