from pathlib import Path

from utils.resume_parser import parse_resume


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SAMPLE RESUME
# ============================================================

PDF_PATH = (
    BASE_DIR
    / "data"
    / "resumes"
    / "sample_resume.pdf"
)


# ============================================================
# CHECK FILE
# ============================================================

if not PDF_PATH.exists():

    print(
        f"Resume not found: {PDF_PATH}"
    )

    raise SystemExit


# ============================================================
# PARSE RESUME
# ============================================================

result = parse_resume(
    PDF_PATH
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("=" * 60)

print(
    "CAREERPILOT AI - RESUME ANALYSIS"
)

print("=" * 60)


print("\nEmail:")
print(
    result["email"]
)


print("\nPhone:")
print(
    result["phone"]
)


print("\nEducation:")
print(
    result["education"]
)


print("\nSkills:")
print(
    result["skills"]
)


print("\nExperience:")
print(
    result["experience"]
)


print("\nPredicted Career:")
print(
    result["predicted_career"]
)


print("\nNamed Entities:")
print(
    result["entities"]
)


print("\nResume text length:")
print(
    len(result["resume_text"])
)


print("=" * 60)