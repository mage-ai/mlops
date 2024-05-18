import json
import os
from typing import Optional

from mlops.utils.deploy.terraform.constants import (
    ENV_VARS_KEY,
    TERRAFORM_AWS_FULL_PATH,
)
from mlops.utils.deploy.terraform.main_variables import update_main_tf
from mlops.utils.deploy.terraform.variables import update_variables


def update_json_file(file_path, new_variables):
    """Update a JSON file with new variables, ensuring uniqueness by "name" key.

    Args:
        file_path (str): The path to the JSON file to update.
        new_variables (list): A list of dictionaries representing new variables to add.
    """

    # Read the current content of the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Convert list of dicts to dict for easy name-based lookup
    data_dict = {item['name']: item for item in data}

    # Append new variables to the current data if they do not exist
    for new_var in new_variables:
        if new_var['name'] not in data_dict:
            data_dict[new_var['name']] = new_var

    # Convert dict back to list
    updated_data = list(data_dict.values())

    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=2)

    print(f'JSON file at {file_path} has been updated.')


def set_environment_variables(
    password: Optional[str] = None,
    username: Optional[str] = None,
    smtp_email: Optional[str] = None,
    smtp_password: Optional[str] = None,
) -> None:
    os.environ['TF_VAR_database_password'] = password or 'password'
    os.environ['TF_VAR_database_user'] = username or 'postgres'

    variables = {}
    variables_main_tf = {}
    env_vars_to_add = []
    if smtp_email:
        os.environ['TF_VAR_smtp_email'] = smtp_email or ''
        variables['smtp_email'] = '""'
        variables_main_tf['smtp_email'] = 'var.smtp_email'
        env_vars_to_add.append(dict(name='SMTP_EMAIL', value='${smtp_email}'))

    if smtp_password:
        os.environ['TF_VAR_smtp_password'] = smtp_password or ''
        variables['smtp_password'] = '""'
        variables_main_tf['smtp_password'] = 'var.smtp_password'
        env_vars_to_add.append(dict(name='SMTP_PASSWORD', value='${smtp_password}'))

    if variables:
        update_variables(variables)

    if variables_main_tf:
        update_main_tf(
            os.path.join(TERRAFORM_AWS_FULL_PATH, 'main.tf'),
            variables_main_tf,
        )

    if env_vars_to_add:
        update_json_file(
            os.path.join(TERRAFORM_AWS_FULL_PATH, f'{ENV_VARS_KEY}.json'),
            env_vars_to_add,
        )

    print(
        'Environment variables have been set/updated in env_vars.json, main.tf, and variables.tf'
    )
