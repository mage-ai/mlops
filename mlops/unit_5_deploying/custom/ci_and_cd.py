from mlops.utils.deploy.aws import (
    IAM_USER_NAME_CICD,
    POLICY_NAME_GITHUB_ACTIONS_DEPLOY_MAGE,
    GITHUB_ACTIONS_DEPLOY_URL,
    attach_policy_to_user,
    create_access_key_for_user,
    create_policy,
    create_user,
    save_credentials_to_file,
)

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def setup(*args, **kwargs):
    # Create IAM policy ContinuousIntegrationContinuousDeployment
    policy_arn = create_policy(
        POLICY_NAME_GITHUB_ACTIONS_DEPLOY_MAGE, GITHUB_ACTIONS_DEPLOY_URL
    )

    # Create the user MageContinuousIntegrationDeployer
    create_user(IAM_USER_NAME_CICD)

    # Attach policy to the user MageContinuousIntegrationDeployer
    attach_policy_to_user(IAM_USER_NAME_CICD, policy_arn)

    # Create access key
    access_key, secret_key = create_access_key_for_user(IAM_USER_NAME_CICD)
    save_credentials_to_file(IAM_USER_NAME_CICD, access_key, secret_key)