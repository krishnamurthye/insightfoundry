import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # put your key in a `.env` file
# LOCAL_REPO_PATH = "/home//workspace/assesment/SakilaProject"

LOCAL_REPO_BASE_PATH = os.environ.get("REPO_PATH", "./repo/")
USE_OPENAI = False
MODEL_NAME = "gpt-3.5-turbo" if USE_OPENAI else "codellama"
MAX_TOKENS = 600

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rb": "Ruby",
    ".cpp": "C++",
    ".cs": "C#",
    ".php": "PHP",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".html": "Html"
}

IGNORE_FILE_FOLDERS = {
    "README.md",
    ".gitignore",
    "output",
    "mvnw",
}

MODEL_LIMITS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4o": 128000,
    "codellama:": 8192,
}

# CHUNK_SIZE = 1024
CHUNK_OVERLAP = 100
MAX_INPUT_TOKENS = 8000  # headroom for response
BUFFER_TOKENS = 200  # Safety margin for unexpected token expansion

OUTPUT_FOLDER = "output/"
OUTPUT_FILE_LEVEL_SUMMERY_NAME = "_file_level_summary.json"
OUTPUT_PROJECT_LEVEL_SUMMERY_NAME = "_project_summary.json"
