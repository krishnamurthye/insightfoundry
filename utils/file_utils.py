import json
import os
from typing import Set, List
from config import EXTENSION_LANGUAGE_MAP

from utils.logging_utils import setup_logger

logger = setup_logger()


def is_valid_file(path):
    # Skip hidden files/folders (like .mvn, .git, .github, etc.)
    parts = path.split(os.sep)
    for part in parts:
        if part.startswith("."):
            return False
    return True


def get_code_files(base_path: str, ignore_set: Set[str]) -> List[str]:
    code_files = []

    for root, dirs, files in os.walk(base_path):
        # Skip hidden or ignored dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ignore_set]

        for f in files:
            if f.startswith(".") or f in ignore_set:
                logger.warn(f"Skipping hidden or ignored file: {f}")
                continue

            full_path = os.path.join(root, f)

            # Skip files inside ignored paths (e.g., output/log.txt)
            rel_parts = os.path.relpath(full_path, base_path).split(os.sep)
            if any(part in ignore_set for part in rel_parts):
                logger.warn(f"Skipping due to hidden/ignored path: {full_path}")
                continue

            code_files.append(full_path)

    return code_files


def write_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def infer_language_from_path(file_path):
    for ext, lang in EXTENSION_LANGUAGE_MAP.items():
        if file_path.endswith(ext):
            return lang
    return "Unknown"


def get_project_name_from_path(path):
    return os.path.basename(os.path.normpath(path)) or "UnknownProject"
