from langchain.prompts import PromptTemplate


def get_code_analysis_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["language", "file_path", "chunk_num", "total_chunks", "code"],
        template="""
You are an expert software engineer specializing in {language}.

You are analyzing a chunk of the source code from:
- File path: {file_path}
- Language: {language}
- Chunk: {chunk_num}/{total_chunks} (may be partial)

**DO NOT invent** any method names or functionality not explicitly visible in the chunk.

Follow these strict rules:
- If no methods are clearly defined, return an empty "methods" array.
- If a method is partially visible, summarize only what is shown.
- Do not add unrelated logic or structures.

Return ONLY a valid JSON object, no markdown or explanations:

Expected JSON:
{{
  "file_summary": "One-line summary of what the file does (technical + business-level insights if possible).",
  "file_complexity_estimate": "approximate cyclomatic complexity of the full file (if possible)",
  "methods": [
    {{
      "method_name": "name of the method",
      "signature": "full method signature",
      "description": "short, precise summary of what the method does",
      "complexity": "cyclomatic complexity estimate (optional)"
    }}
  ],
  "mocks": ["list any mocking frameworks or mock objects used"],
  "assertions": ["list any assertions or test validations used"],
  "noteworthy": [
    "boilerplate code",
    "code quality issues (e.g., long methods, duplication)",
    "naming or spelling issues",
    "security flaws (e.g., hardcoded secrets, weak hashing, SQL injection)",
    "performance problems",
    "refactoring suggestions"
  ]
}}

Here is the code:
-------------------
{code}
-------------------
"""
    )
