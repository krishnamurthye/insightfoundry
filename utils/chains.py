import json

from config import MODEL_NAME, MAX_TOKENS, USE_OPENAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain.schema.output_parser import StrOutputParser
from prompts.language_prompts import get_code_analysis_prompt
from prompts.project_summary_prompt import get_project_summary_prompt
from utils.logging_utils import setup_logger

logger = setup_logger()


def build_chain(prompt):
    llm = get_llm()
    logger.info(f"Using model: {MODEL_NAME} (OpenAI: {USE_OPENAI})")
    return RunnableSequence(prompt | llm | StrOutputParser())


def get_llm():
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.2, max_tokens=MAX_TOKENS) if USE_OPENAI else ChatOllama(
        model=MODEL_NAME, temperature=0.2)
    return llm


def build_chain_for_language():
    return build_chain(get_code_analysis_prompt())


def build_chain_for_project():
    return build_chain(get_project_summary_prompt())
