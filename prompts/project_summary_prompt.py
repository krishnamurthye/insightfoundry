from langchain.prompts import PromptTemplate


def get_project_summary_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["grouped_descriptions"],
        template="""
You are analyzing a software project based on grouped summaries of its source code files. Below is a breakdown of the summaries grouped by role (e.g., entity classes, services, repositories, controllers, tests, etc.):

{grouped_descriptions}

Using this input, generate a comprehensive project-level JSON summary that includes:

- project_name: A placeholder name like "UnknownProject" or try to infer one.
- business_purpose: One paragraph explaining the high-level intent of the system.
- main_features: A bullet list of core modules or responsibilities.
- technology_stack: Inferred languages, frameworks, database tools, etc.
- testing_and_mocks: Any notes on testing patterns, mock usage.
- architecture_and_patterns: Structural insights like layered architecture, monolith vs microservices, and known design patterns used (e.g., Singleton, Factory, MVC).

Return ONLY a valid JSON object.
        """.strip()
    )
