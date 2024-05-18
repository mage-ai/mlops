import subprocess

from mlops.utils.deploy.terraform.constants import (
    TERRAFORM_AWS_FULL_PATH,
)


def run_terraform_commands(subfolder: str) -> None:
    try:
        # Initialize the Terraform configuration in the specified subfolder
        subprocess.run(['terraform', '-chdir=' + subfolder, 'init'], check=True)
        # Apply the Terraform configuration in the specified subfolder
        subprocess.run(
            ['terraform', '-chdir=' + subfolder, 'apply', '-auto-approve'], check=True
        )
        print(f'Terraform init and apply executed successfully in {subfolder}')
    except subprocess.CalledProcessError as err:
        print(f'Error: {err}')
        raise err


def terraform_apply() -> None:
    run_terraform_commands(TERRAFORM_AWS_FULL_PATH)


def terraform_destroy() -> None:
    try:
        subprocess.run(
            [
                'terraform',
                '-chdir=' + TERRAFORM_AWS_FULL_PATH,
                'destroy',
                '-auto-approve',
            ],
            check=True,
        )
        print(f'Terraform destroy executed successfully in {TERRAFORM_AWS_FULL_PATH}')
    except subprocess.CalledProcessError as err:
        print(f'Error: {err}')
        raise err
