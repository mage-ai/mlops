from mlops.utils.deploy.aws import (
    IAM_USER_NAME,
    POLICY_NAME_TERRAFORM_APPLY_DEPLOY_MAGE,
    POLICY_NAME_TERRAFORM_DESTROY_DELETE_RESOURCES,
    TERRAFORM_APPLY_URL,
    TERRAFORM_DESTROY_URL,
    attach_policy_to_user,
    create_access_key_for_user,
    create_policy,
    create_user,
    reset,
    save_credentials_to_file,
)

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def setup(*args, **kwargs):
    reset(IAM_USER_NAME)

    # Create IAM Policies
    terraform_apply_policy_arn = create_policy(
        POLICY_NAME_TERRAFORM_APPLY_DEPLOY_MAGE, TERRAFORM_APPLY_URL
    )
    terraform_destroy_policy_arn = create_policy(
        POLICY_NAME_TERRAFORM_DESTROY_DELETE_RESOURCES, TERRAFORM_DESTROY_URL
    )

    # Create the user MageDeployer
    create_user(IAM_USER_NAME)

    # Attach policies to the user MageDeployer
    attach_policy_to_user(IAM_USER_NAME, terraform_apply_policy_arn)
    attach_policy_to_user(IAM_USER_NAME, terraform_destroy_policy_arn)

    # Create access key
    access_key, secret_key = create_access_key_for_user(IAM_USER_NAME)
    save_credentials_to_file(IAM_USER_NAME, access_key, secret_key)
