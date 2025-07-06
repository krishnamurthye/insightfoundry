# utils/git_utils.py
import subprocess
import os
import shutil
from urllib.parse import urlparse

from utils.logging_utils import setup_logger

logger = setup_logger()


def clone_repo(git_url: str, base_path: str = "."):
    repo_name = get_repo_name_from_url(git_url)
    clone_path = os.path.join(base_path, repo_name)

    if os.path.exists(clone_path):
        logger.debug(f"Removing existing repo at {clone_path}")
        shutil.rmtree(clone_path)

    logger.info(f"Cloning repo from {git_url} to {clone_path}")
    subprocess.run(["git", "clone", git_url, clone_path], check=True)
    return repo_name, clone_path


def get_repo_name_from_url(git_url: str) -> str:
    # Extract last part of the path, remove .git if present
    repo_name = os.path.splitext(os.path.basename(urlparse(git_url).path))[0]
    return repo_name or "repo"
