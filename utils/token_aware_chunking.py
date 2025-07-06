from config import CHUNK_OVERLAP, MAX_INPUT_TOKENS, BUFFER_TOKENS, MODEL_LIMITS, MODEL_NAME
from langchain.text_splitter import RecursiveCharacterTextSplitter

from prompts.language_prompts import get_code_analysis_prompt
from utils.logging_utils import setup_logger

logger = setup_logger()


def get_model_context_limit(model_name: str) -> int:
    # Default to MAX_INPUT_TOKENS if unknown
    return MODEL_LIMITS.get(model_name.lower(), MAX_INPUT_TOKENS)


def estimate_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    from tiktoken import encoding_for_model
    enc = encoding_for_model(model_name)
    return len(enc.encode(text))


def get_available_code_tokens(prompt_template, prompt_input):
    temp_input = prompt_template.format_prompt(
        **{**prompt_input, "code": ""}
    ).to_string()
    system_tokens = estimate_tokens(temp_input)
    max_input_tokens = get_model_context_limit(MODEL_NAME) - BUFFER_TOKENS
    budget = max_input_tokens - system_tokens

    # Adjust for overlap — assume overlap is duplicated in every chunk
    effective_budget = budget - CHUNK_OVERLAP
    return max(100, effective_budget)  # safeguard


def split_code_to_chunks(code, token_budget):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=token_budget,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(code)


def get_token_budget(language, path):
    prompt_template = get_code_analysis_prompt()
    token_budget = get_available_code_tokens(prompt_template, {
        "language": language,
        "file_path": path,
        "chunk_num": 1,
        "total_chunks": 100,  # max placeholder
        "code": ""
    })
    return token_budget


def token_aware_chunking(code, language, path):
    token_budget = get_token_budget(language, path)
    logger.info(f"Estimated available token budget: {token_budget}")
    return split_code_to_chunks(code, token_budget)
