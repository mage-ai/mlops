from mlops.utils.deploy.terraform.cli import terraform_destroy

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(*args, **kwargs):
    if kwargs.get('destroy'):
        terraform_destroy()
    else:
        print('Skipping Terraform destroy...')