import mlflow
import pickle


mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("nec-taxi-experiment")

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
    # Specify your data exporting logic here
    dv, lr = data

    with mlflow.start_run():
        with open('dict_vectorizer.bin', 'wb') as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact('dict_vectorizer.bin')

        mlflow.sklearn.log_model(lr, 'model')
    
    print('DONE')
