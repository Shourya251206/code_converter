from ollama_client import ask_codellama

def build_prompt(code, source_lang, target_lang):
    prompt = (
        f"You are a highly skilled software engineer.\n\n"
        f"Convert the following {source_lang} code to {target_lang}.\n"
        f"Only provide the translated code, without explanation or markdown.\n\n"
        f"```\n{code}\n```"
    )
    return prompt

def convert_code(code, source_lang, target_lang):
    prompt = build_prompt(code, source_lang, target_lang)
    result = ask_codellama(prompt)
    return result.strip()
