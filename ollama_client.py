import subprocess

def ask_codellama(prompt: str, model="codellama"):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout
    except Exception as e:
        return f"Error querying Code Llama: {e}"
