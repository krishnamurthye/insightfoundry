import json

from config import MAX_INPUT_TOKENS, BUFFER_TOKENS
from prompts.project_summary_prompt import get_project_summary_prompt
from utils.chains import build_chain_for_project

import re
from collections import defaultdict

from utils.token_aware_chunking import estimate_tokens
from utils.logging_utils import setup_logger

logger = setup_logger()


def get_summary_token_budget(template_str, placeholder_key="grouped_descriptions"):
    prompt_prefix = template_str.replace("{" + placeholder_key + "}", "")
    return MAX_INPUT_TOKENS - BUFFER_TOKENS - estimate_tokens(prompt_prefix)


def group_files_by_role(descriptions):
    structure = defaultdict(list)

    role_keywords = {
        "Tests": re.compile(r"(test|spec|mock|assert)", re.IGNORECASE),
        "Controllers / Routes": re.compile(r"(controller|route|handler)", re.IGNORECASE),
        "Models / Schemas": re.compile(r"(model|schema|entity|datatype)", re.IGNORECASE),
        "Services / Logic": re.compile(r"(service|usecase|logic|manager|processor)", re.IGNORECASE),
        "Database / Repositories": re.compile(r"(repo|dao|db|database|storage)", re.IGNORECASE),
        "Utilities / Helpers": re.compile(r"(util|helper|common|shared)", re.IGNORECASE)
    }

    for file_entry in descriptions:
        path = file_entry["file"].lower()
        summary = file_entry.get("description", {}).get("file_summary", "")
        matched = False

        for role, pattern in role_keywords.items():
            if pattern.search(path):
                structure[role].append({
                    "path": path,
                    "summary": summary
                })
                matched = True
                break

        if not matched:
            structure["Other"].append({
                "path": path,
                "summary": summary
            })

    return structure


def summarize_project(file_descriptions):
    grouped = group_files_by_role(file_descriptions)
    template = get_project_summary_prompt()  # returns PromptTemplate or str
    token_budget = get_summary_token_budget(template.template if hasattr(template, 'template') else template)

    grouped_descriptions = ""
    current_tokens = 0

    for role, summaries in grouped.items():
        if not summaries:
            continue

        header = f"\n### {role.title()} Files\n"
        header_tokens = estimate_tokens(header)

        chunk = ""
        chunk_tokens = header_tokens

        for s in summaries:
            summary_text = s.get("summary", "").strip()
            if summary_text:
                line = f"- {summary_text}\n"
                line_tokens = estimate_tokens(line)

                if current_tokens + chunk_tokens + line_tokens > token_budget:
                    break  # stop appending if we're about to go over budget

                chunk += line
                chunk_tokens += line_tokens

        if chunk:
            grouped_descriptions += header + chunk
            current_tokens += chunk_tokens

    # Build and call chain
    chain = build_chain_for_project()
    try:
        result = chain.invoke({"grouped_descriptions": grouped_descriptions})
        return json.loads(result)
    except Exception as e:
        logger.error(f"[Error] Failed generating project summary: {e}")
        return {
            "project": "UnknownProject",
            "error": str(e),
            "fallback_note": "LLM failed to generate project summary"
        }
