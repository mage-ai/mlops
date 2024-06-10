import os
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression 
import joblib

# Set experiment id
mlflow.set_experiment('mage_lr_experiment')

# Set tracking uri
# mlflow.set_tracking_uri('http://localhost:5000')

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your transformation logic here
    df_train = data

    # turn dictionary into vector
    dv = DictVectorizer()
    train_dicts = df_train[['PULocationID', 'DOLocationID']].to_dict(orient='records')

    # Feature matrix
    X_train = dv.fit_transform(train_dicts)

    # Target matrix
    target = 'duration'
    y_train = df_train[target].values   

    # Build model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Specify artifact_path
    artifact_directory = 'mlflow_artifacts'

    # Create directory if it doesnt exist
    os.makedirs(artifact_directory, exist_ok=True)

    # Save and log the artifact (DictVectorizer)
    artifact_path =  os.path.join(artifact_directory, "dv_artifact.pkl")

    with open(artifact_path, 'wb') as f:
        joblib.dump(dv, f)

    # Log the linear regression model with MLflow
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "linear_regression_model")
        mlflow.log_param("intercept", model.intercept_)
        mlflow.log_artifact(artifact_path)
    
    return model, dv