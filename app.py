from flask import Flask, render_template, request, jsonify
from converter import convert_code
from language_detector import detect_language_from_extension

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        uploaded_file = request.files.get("file")
        target_language = request.form.get("target_language")

        if not uploaded_file:
            return jsonify({"error": "No file uploaded"}), 400

        if not target_language:
            return jsonify({"error": "No target language specified"}), 400

        code = uploaded_file.read().decode("utf-8")
        source_language = detect_language_from_extension(uploaded_file.filename)

        if source_language == "Unknown":
            return jsonify({"error": "Unsupported file type"}), 400

        converted_code = convert_code(code, source_language, target_language)

        if not converted_code or converted_code.lower().startswith("error"):
            return jsonify({"error": "Conversion failed"}), 500

        return jsonify({
            "source_language": source_language,
            "converted_code": converted_code
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
