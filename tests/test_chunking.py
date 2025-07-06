# tests/test_chunking.py
from utils.token_aware_chunking import get_available_code_tokens
from prompts.language_prompts import get_code_analysis_prompt

def test_token_budget_allocation():
    template = get_code_analysis_prompt()
    prompt_input = {
        "language": "java",
        "file_path": "/home/user/test",
        "chunk_num": 1,
        "total_chunks": 100,  # max placeholder
        "code": ""
    }
    tokens = get_available_code_tokens(template, prompt_input)
    assert tokens >= 100  # Ensure fallback safety works
