from mage_ai.orchestration.triggers.api import trigger_pipeline

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def retrain(*args, **kwargs):
    trigger_pipeline(
        'xgboost_training',
        check_status=True,
        error_on_failure=True,
        schedule_name='Automatic retraining for XGBoost',
        verbose=True,
    )
