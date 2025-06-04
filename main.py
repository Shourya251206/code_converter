from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import zipfile
import tempfile

from dependency_analyzer import get_dependencies
from chunker import split_code_with_dependencies  # NEW FUNCTION
from converter import convert_code

app = FastAPI()

@app.post("/convert/")
async def convert_file(file: UploadFile = File(...), target_language: str = Form(...)):
    contents = await file.read()
    code = contents.decode("utf-8")
    lines = code.splitlines()

    func_defs, class_defs, func_calls = get_dependencies(code)
    chunks = split_code_with_dependencies(lines, func_defs, class_defs, func_calls)

    converted_chunks = []
    for chunk in chunks:
        converted = convert_code(chunk, target_language)
        converted_chunks.append(converted)

    # Save & zip logic goes here...


        # Step 4: Save each converted file
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    converted_paths = []

    for idx, chunk_code in enumerate(converted_chunks):
        base_name = file.filename.rsplit(".", 1)[0]
        converted_name = f"{base_name}_converted.{target_language.lower()}"
        output_path = os.path.join(output_dir, converted_name)
        with open(output_path, "w") as f:
            f.write(chunk_code)
        converted_paths.append(output_path)

    # Step 5: Create ZIP archive
    zip_filename = f"{file.filename.rsplit('.', 1)[0]}_converted.zip"
    zip_path = os.path.join(output_dir, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file_path in converted_paths:
            arcname = os.path.basename(file_path)  # only file name in zip
            zipf.write(file_path, arcname=arcname)

    # Step 6: Return ZIP
    return FileResponse(zip_path, filename=zip_filename, media_type="application/zip")

