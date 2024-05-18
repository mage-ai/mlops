import json
import os
import re
from typing import Dict, List, Tuple, Union

from typing_extensions import Optional

from mlops.utils.deploy.terraform.constants import TERRAFORM_AWS_FULL_PATH


def parse_terraform_variables(lines: List[str]) -> Tuple[Dict, set]:
    attribute_keys = set()
    mapping = {}
    for text in lines:
        line = text
        pattern = r'variable\s*'
        line = line.strip()
        # Remove variable keyword
        line = re.sub(pattern, '', line).strip()
        pattern = r'"(\w+)"\s*\{'

        variable_match = re.match(pattern, line)
        variable_remove = variable_match.span(0)
        variable_extract = variable_match.span(1)
        variable = line[variable_extract[0] : variable_extract[1]]

        line = line[variable_remove[1] :]
        pattern = r'(.*?)\}'
        regex = re.compile(pattern, re.DOTALL)
        values_match = regex.findall(line)

        attributes = {}
        for matched_row in values_match:
            for x in matched_row.split('\n'):
                x = x.strip()
                if not x or x.startswith('#'):
                    continue
                key, value = x.split('=')
                key = key.strip()
                attributes[key] = value.strip()
                attribute_keys.add(key)

        mapping[variable] = attributes

    return mapping, attribute_keys


def parse_file(file_path: str) -> Tuple[Dict, set]:
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        content = f.read()

    lines = []
    current_idx = 0
    pattern = re.compile(r'\}')
    for match in pattern.finditer(content):
        start, end = match.span()
        lines.append(content[current_idx:end])
        current_idx = end

    mapping, attribute_keys = parse_terraform_variables(lines)

    return mapping, attribute_keys


def build_terraform_file_content(
    mapping: Dict[
        str,
        Dict[
            str,
            Union[
                float,
                int,
                str,
            ],
        ],
    ],
    attribute_keys: set,
    variables: Optional[Dict[str, Union[bool, float, int, str]]],
) -> str:
    mapping_new = {**mapping}
    variables = variables or {}

    for key, value in variables.items():
        var_type = 'string'
        var_value = value

        if isinstance(value, bool):
            var_type = 'bool'
            var_value = 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            var_type = 'number'
        elif isinstance(value, list):
            var_value = json.dumps(value)
            var_type = None
        elif value is None:
            var_value = '""'
            var_type = None
        elif value == '' or value == '':
            var_value = '""'

        if key not in mapping_new:
            mapping_new[key] = dict(
                description='"Dynamically added by the Mage Python script."',
            )
            print(f'Adding variable  : "{key}"')
        else:
            print(f'Updating variable: "{key}"')

        mapping_new[key]['default'] = var_value
        if var_type is not None:
            mapping_new[key]['type'] = var_type

    attribute_key_length = max(len(key) for key in attribute_keys)

    variable_rows = []
    for variable_uuid, attribute_mapping in mapping_new.items():
        arr = []
        for key, value in attribute_mapping.items():
            arr.append(f'  {key.ljust(attribute_key_length)} = {value}')
        text = f'variable "{variable_uuid}" ' + '{\n'
        body_text = '\n'.join(arr)
        text = text + body_text
        text = text + '\n}'
        variable_rows.append(text)

    content_new = '\n\n'.join(variable_rows)

    return content_new


def update_variables(variables: Optional[Dict] = None):
    file_path = os.path.join(TERRAFORM_AWS_FULL_PATH, 'variables.tf')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    mapping, attribute_keys = parse_file(file_path)
    content_new = build_terraform_file_content(mapping, attribute_keys, variables)

    with open(file_path, 'w') as f:
        f.write(content_new)

    if variables:
        print(f'{len(variables)} variables have been added/updated in {file_path}.')
