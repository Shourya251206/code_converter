def detect_language_from_extension(filename):
    ext = filename.split('.')[-1].lower()
    mapping = {
        "py": "Python",
        "js": "JavaScript",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "cs": "C#",
        "rb": "Ruby",
        "php": "PHP",
        "go": "Go"
    }
    return mapping.get(ext, "Unknown")