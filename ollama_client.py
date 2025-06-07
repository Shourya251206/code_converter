# ollama_client.py

import subprocess

def ask_codellama(prompt):
    """
    Sends the prompt to the locally running Code Llama model via Ollama CLI.
    Adjust this if you're using the Ollama Python API or different setup.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "codellama", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
