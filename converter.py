from ollama_client import ask_codellama

def build_prompt(source_code: str, source_lang: str, target_lang: str) -> str:
    """
    Creates a prompt to send to Code Llama for code conversion.
    """
    return f"""You are a highly skilled software engineer.

Your task is to translate code from {source_lang} to {target_lang}.
Provide only the translated code, without any explanations, comments, or markdown formatting.

Here is the original {source_lang} code:

{source_code}
"""

def convert_code(source_code: str, source_lang: str, target_lang: str) -> str:
    """
    Uses Code Llama (via Ollama) to convert code to the desired language.
    """
    prompt = build_prompt(source_code, source_lang, target_lang)
    response = ask_codellama(prompt)
    return response.strip()
