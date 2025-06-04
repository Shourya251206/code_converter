from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os

from dependency_analyzer import get_dependencies
from chunker import split_code_with_dependencies  # NEW FUNCTION
from converter import convert_code

app = FastAPI()

@app.post("/convert/")
async def convert_file(file: UploadFile = File(...), target_language: str = Form(...)):
    # Step 0: Read the uploaded file
    contents = await file.read()
    code = contents.decode("utf-8")
    lines = code.splitlines()

    # Step 1: Analyze dependencies
    func_defs, func_calls = get_dependencies(code)

    # Step 2: Chunk the code with dependency injection
    chunks = split_code_with_dependencies(lines, func_defs, func_calls)

    # Step 3: Convert each chunk
    converted_chunks = []
    for chunk in chunks:
        converted = convert_code(chunk, target_language)
        converted_chunks.append(converted)

    # Step 4: Merge all converted chunks
    converted_code = "\n\n".join(converted_chunks)

    # Step 5: Save the result to a file
    filename = file.filename.rsplit(".", 1)[0]
