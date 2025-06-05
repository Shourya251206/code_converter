from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

from language_detector import detect_language_from_extension
from converter import convert_code
from utils import read_uploaded_file

app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Web frontend
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Backend conversion API
@app.post("/convert/")
async def convert(
    file: UploadFile = File(...),
    target_language: str = Form(...)
):
    code = read_uploaded_file(file)  # ✅ If you're using utils.py
    source_language = detect_language_from_extension(file.filename)

    if source_language == "Unknown":
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    converted = convert_code(code, source_language, target_language)
    return {"source_language": source_language, "converted_code": converted}
