import sys
import os

from config import MODEL_NAME, USE_OPENAI, IGNORE_FILE_FOLDERS, OUTPUT_FOLDER, \
    OUTPUT_FILE_LEVEL_SUMMERY_NAME, OUTPUT_PROJECT_LEVEL_SUMMERY_NAME, LOCAL_REPO_BASE_PATH
from utils.file_utils import get_code_files, infer_language_from_path, write_json, get_project_name_from_path
from runners.summarize_code import summarize_code
from runners.summarize_project import summarize_project
from utils.git_utils import clone_repo
from utils.logging_utils import setup_logger
from utils.ollama_util import stop_ollama_model


def main():
    logger = setup_logger()
    repo_url = sys.argv[1] if len(sys.argv) > 1 else None
    project_name = "repo"
    project_path = LOCAL_REPO_BASE_PATH
    if repo_url:
        project_name, project_path = clone_repo(repo_url, LOCAL_REPO_BASE_PATH)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    logger.info(f"Scanning: {project_path}")
    files = get_code_files(project_path, IGNORE_FILE_FOLDERS)
    results = []

    for path in files:
        logger.info(f"\nProcessing: {path}")
        language = infer_language_from_path(path)
        logger.info(f"Language: {language}")

        if not language or language.lower() == "unknown":
            logger.warn(f"Skipping unsupported language: {path}")
            continue

        try:
            with open(path, encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            logger.error(f"Read error: {e}")
            continue

        if not code.strip():
            logger.warn(f"Skipping empty file: {path}")
            continue

        summaries = summarize_code(code, language, path)
        results.append(summaries)

    write_json({"project": project_name, "files": results},
               OUTPUT_FOLDER + project_name + OUTPUT_FILE_LEVEL_SUMMERY_NAME)

    logger.info("\nGenerating project-level summary...")
    project_summary = summarize_project(results)
    logger.info(f"\nProject Summary:\n{project_summary}")

    write_json({
        "project": project_name,
        "summary": project_summary,
    }, OUTPUT_FOLDER + project_name + OUTPUT_PROJECT_LEVEL_SUMMERY_NAME)

    if not USE_OPENAI:
        stop_ollama_model(MODEL_NAME)


if __name__ == "__main__":
    main()
