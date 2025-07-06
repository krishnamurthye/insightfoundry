import subprocess
from utils.logging_utils import setup_logger

logger = setup_logger()


def stop_ollama_model(model):
    try:
        subprocess.run(["ollama", "stop", model], check=True)
        logger.info(f"Stopped Ollama model: {model}")
    except:
        logger.error(f"Could not stop model: {model}")
