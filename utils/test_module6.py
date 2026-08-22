from resume_parser import parse_resume


PDF_PATH = "../data/resumes/sample_resume.pdf"


result = parse_resume(PDF_PATH)


print("\n" + "=" * 60)
print("CAREERPILOT AI - RESUME ANALYSIS")
print("=" * 60)


print("\nEmail:")
print(result["email"])


print("\nPhone:")
print(result["phone"])


print("\nEducation:")
print(result["education"])


print("\nSkills:")
print(result["skills"])


print("\nExperience:")
print(result["experience"])


print("\nPredicted Career:")
print(result["predicted_career"])


print("\nNamed Entities:")
print(result["entities"])


print("\n" + "=" * 60)