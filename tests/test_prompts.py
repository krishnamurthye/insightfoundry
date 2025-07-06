import pytest
from prompts.project_summary_prompt import get_project_summary_prompt


def test_prompt_template_has_correct_variable():
    """Ensure the input variable 'grouped_descriptions' is present."""
    prompt = get_project_summary_prompt()
    assert "grouped_descriptions" in prompt.input_variables


def test_prompt_contains_required_sections():
    """Ensure all expected output fields are mentioned in the prompt template."""
    prompt = get_project_summary_prompt()
    template = prompt.template

    expected_sections = [
        "project_name",
        "business_purpose",
        "main_features",
        "technology_stack",
        "testing_and_mocks",
        "architecture_and_patterns"
    ]

    for section in expected_sections:
        assert section in template, f"Missing section in prompt: {section}"


def test_prompt_includes_instruction_to_return_json_only():
    """Check if the prompt explicitly asks to return ONLY JSON."""
    prompt = get_project_summary_prompt()
    assert "Return ONLY a valid JSON object." in prompt.template
