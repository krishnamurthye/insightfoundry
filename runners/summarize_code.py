from prompts.language_prompts import get_code_analysis_prompt
from utils.chains import build_chain_for_language, get_llm
from utils.token_aware_chunking import token_aware_chunking
from utils.complexity import  merge_complexity_estimates
from utils.extract import extract_json_objects
import re
import json

from utils.logging_utils import setup_logger

logger = setup_logger()


def deduplicate_summary(summary):
    lines = re.split(r'[.。!?]\s*', summary)
    seen = set()
    unique_lines = [line for line in lines if line and not (line in seen or seen.add(line))]
    return '. '.join(unique_lines).strip()


def deduplicate_methods(methods):
    seen = set()
    deduped = []
    for method in methods:
        key = (method.get("method_name"), method.get("signature"))
        if key not in seen:
            seen.add(key)
            deduped.append(method)
    return deduped


def deduplicate_flat_list(items):
    return list(dict.fromkeys(item.strip() for item in items if isinstance(item, str) and item.strip()))


def summarize_code(code, language, path):
    chunks = token_aware_chunking(code, language, path)
    chain = build_chain_for_language()
    results = []
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        try:
            logger.info(f"\nSummarizing chunk {i + 1}/{total_chunks}...")
            logger.debug(f"Chunk preview:\n{chunk[:500]}...")

            prompt_input = {
                "language": language,
                "file_path": path,
                "chunk_num": i + 1,
                "total_chunks": total_chunks,
                "code": chunk
            }
            logger.debug(f"\n>>> Prompt Input for Chunk {i + 1}:\n{json.dumps(prompt_input, indent=2)}\n")

            # result = run_with_llm(prompt_input)
            result = run_with_longchain(chain, prompt_input)
            logger.debug(f"\nRaw LLM Output:\n{result}\n")
            results.append(result)
        except Exception as e:
            logger.error(f"[Error] Failed summarizing chunk {i + 1}: {e}")

    json_blocks = extract_json_objects(results)
    logger.debug(f"\n result of extract_json_objects:\n{json_blocks}\n")

    merged = {"file_summary": "", "file_complexity_estimate": "", "methods": [], "mocks": [], "assertions": [],
              "noteworthy": []}

    try:
        if json_blocks:
            merged = {
                "file_summary": deduplicate_summary(" ".join(
                    str(j.get("file_summary", "")) for j in json_blocks).strip()),
                "file_complexity_estimate": merge_complexity_estimates(json_blocks),
                "methods": deduplicate_methods(sum((j.get("methods", []) for j in json_blocks), [])),
                "mocks": deduplicate_flat_list(sum((j.get("mocks", []) for j in json_blocks), [])),
                "assertions": deduplicate_flat_list(sum((j.get("assertions", []) for j in json_blocks), [])),
                "noteworthy": deduplicate_flat_list(sum((j.get("noteworthy", []) for j in json_blocks), [])),
            }
            logger.debug(f"\nMerged Summary: {merged}")
    except Exception as e:
        logger.error(f"[Error] Failed while merging or calculating complexity: {e}")

    return {"file": path, "description": merged}


def run_with_longchain(chain, prompt_input):
    result = chain.invoke(prompt_input)
    return result


# to debug the issue
def run_with_llm(prompt_input):
    llm = get_llm()
    prompt = get_code_analysis_prompt()
    prompt_text = prompt.format_prompt(**prompt_input).to_string()
    logger.debug(f"prompt_text: {prompt_text}")
    response = llm.invoke(prompt_text)
    return response
