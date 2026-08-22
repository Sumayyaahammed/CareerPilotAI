import json

from resume_parser import parse_resume


PDF_PATH = "../data/resumes/sample_resume.pdf"

result = parse_resume(PDF_PATH)


# Resume text can be large, so remove it from JSON output
result.pop("resume_text", None)


with open(
    "../data/processed/resume_profile.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        result,
        file,
        indent=4,
        ensure_ascii=False
    )


print("Resume profile saved successfully.")