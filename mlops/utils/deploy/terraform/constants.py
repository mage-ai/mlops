import os

from mage_ai.settings.repo import get_repo_path

ENV_VARS_KEY = 'env_vars'
TERRAFORM_REPO_URL = 'https://github.com/mage-ai/mage-ai-terraform-templates.git'
TERRAFORM_DIR_NAME = 'terraform'
TERRAFORM_AWS_NAME = 'aws'
TERRAFORM_FULL_PATH = os.path.join(
    os.getenv('MAGE_CODE_PATH', get_repo_path(root_project=True)), TERRAFORM_DIR_NAME
)
TERRAFORM_AWS_FULL_PATH = os.path.join(TERRAFORM_FULL_PATH, TERRAFORM_AWS_NAME)
