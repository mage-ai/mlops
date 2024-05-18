import os
import shutil
from typing import Optional

from git import Repo


def git_clone(repo_url: str, target_dir: str):
    """
    Clone a GitHub repository to a specified directory.
    :param repo_url: str - GitHub repository URL.
    :param target_dir: str - Local target directory path for cloning.
    """
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    Repo.clone_from(repo_url, target_dir)
    print(f'Repository cloned into: {target_dir}')


def copy_files(source_dir: str, target_dir: str, file_extension: Optional[str] = None):
    """
    Copy selective files from a source directory to a target directory based on file extension.
    :param source_dir: str - The source directory from which files will be copied.
    :param target_dir: str - The target directory to which files will be copied.
    :param file_extension: str - The file extension to filter which files should be copied.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file_extension or file.endswith(file_extension):
                source_path = os.path.join(root, file)
                target_path = os.path.join(
                    target_dir, os.path.relpath(source_path, start=source_dir)
                )
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy(source_path, target_path)
                print(f'Copied: {source_path} -> {target_path}')


def remove_git_repository(repo_path: str):
    """
    Removes the cloned Git repository directory.
    """
    if os.path.isdir(repo_path):
        shutil.rmtree(repo_path)
        print(f'Repository at {repo_path} has been removed.')
