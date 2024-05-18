import os
import re
from typing import Dict, Optional

from mlops.utils.deploy.terraform.constants import TERRAFORM_AWS_FULL_PATH


def extract_data(content: str) -> Optional[str]:
    pattern = r'data\s"template_file"\s"env_vars"\s\{\n(?:.*\n)*?\}'
    return re.search(pattern, content)


def extract_var(content: str) -> Optional[str]:
    pattern = r'vars\s*=\s*\{(?:[^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
    return re.search(pattern, content)


def extract_dict_string(content: str) -> Dict:
    pattern = r'\{((?:[^{}]*(?:\{[^{}]*\}[^{}]*)*))\}'
    return re.search(pattern, content)


def replace_by_index(original_string, start_index, end_index, replacement):
    before = original_string[:start_index]
    after = original_string[end_index:]
    return before + replacement + after


def update_text(content: str, variables: Optional[Dict]) -> str:
    stack = []

    data_section_match = extract_data(content)
    data_section_text = data_section_match.group(0)
    stack.insert(0, (data_section_match.span(0), content))

    var_match = extract_var(data_section_text)
    var_text = var_match.group(0)
    stack.insert(0, (var_match.span(0), data_section_text))

    dict_match = extract_dict_string(var_text)
    dict_text = dict_match.group(1)
    stack.insert(0, (dict_match.span(1), var_text))

    lines = dict_text.split('\n')

    variables = variables or {}
    mapping = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split('=')
        key = parts[0]
        value = '='.join(parts[1:]).strip()
        mapping[key.strip()] = value

    combined = {**mapping, **variables}
    lines_new = []

    for key, value in combined.items():
        if key in variables:
            text = variables[key]
        else:
            text = value
        lines_new.append(f'{key} = {text}')

    content_new = '\n'.join(lines_new)

    while stack:
        match, text = stack.pop(0)
        si, ei = match
        content_new = replace_by_index(text, si, ei, content_new)

    return content_new


def update_main_tf(file_path: Optional[str] = None, variables: Optional[Dict] = None):
    file_path = file_path or os.path.join(TERRAFORM_AWS_FULL_PATH, 'main.tf')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    content = ''
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()

    content = update_text(content, variables)
    with open(file_path, 'w') as file:
        file.write(content)
