import os
from tempfile import TemporaryDirectory
from typing import Optional

from mlops.utils.deploy.github import copy_files, git_clone, remove_git_repository
from mlops.utils.deploy.terraform.constants import (
    ENV_VARS_KEY,
    TERRAFORM_AWS_FULL_PATH,
    TERRAFORM_AWS_NAME,
    TERRAFORM_REPO_URL,
)
from mlops.utils.deploy.terraform.env_vars import update_json_file
from mlops.utils.deploy.terraform.variables import update_variables


def download_terraform_configurations():
    with TemporaryDirectory() as tmp_dir:
        git_clone(TERRAFORM_REPO_URL, tmp_dir)

        copy_files(
            os.path.join(tmp_dir, TERRAFORM_AWS_NAME),
            TERRAFORM_AWS_FULL_PATH,
        )


def setup_configurations(
    prevent_destroy_ecr: Optional[bool] = None,
    project_name: Optional[str] = None,
):
    if project_name:
        project_name = f'"{project_name}"'
    else:
        project_name = '"mlops"'

    docker_image = '"mageai/mageai:alpha"'

    print('Updating variables in variables.tf')
    print(f'  "app_name"            = {project_name}')
    print(f'  "docker_image"        = {docker_image}')
    print(f'  "enable_ci_cd"        = true')

    variables = dict(
        app_name=project_name,
        docker_image=docker_image,
        enable_ci_cd=True,
    )

    if prevent_destroy_ecr is not None:
        variables['prevent_destroy_ecr'] = prevent_destroy_ecr
        print(f'  "prevent_destroy_ecr" = {"true" if prevent_destroy_ecr else "false"}')

    update_variables(variables)

    update_json_file(
        os.path.join(TERRAFORM_AWS_FULL_PATH, f'{ENV_VARS_KEY}.json'),
        [
            dict(name='MAGE_PRESENTERS_DIRECTORY', value='mlops/presenters'),
        ],
    )
