from flask import Flask, render_template, request
from converter import convert_code
from language_detector import detect_language_from_extension

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    uploaded_file = request.files["file"]
    target_language = request.form["target_language"]
    code = uploaded_file.read().decode("utf-8")
    print("Received code:\n", code)

    source_language = detect_language_from_extension(uploaded_file.filename)

    if source_language == "Unknown":
        return {"error": "Unsupported file type"}, 400

    converted_code = convert_code(code, source_language, target_language)
    return {"source_language": source_language, "converted_code": converted_code}

if __name__ == "__main__":
    app.run(debug=True)
