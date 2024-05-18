from mlops.utils.deploy.aws import update_boto3_client
from mlops.utils.deploy.terraform.cli import terraform_apply

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def deploy(*args, **kwargs):
    update_boto3_client()
    terraform_apply()