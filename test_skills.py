
from src.data_processor import load_job_data
from src.skill_analyzer import get_skills_for_role

df = load_job_data()

roles_to_test = [
    "Data Analyst",
    "Software Engineer",
    "Cybersecurity Analyst",
    "DevOps Engineer",
]

for role in roles_to_test:
    print(f"\n--- {role} ---")

    results = get_skills_for_role(df, role, limit=5)

    if results:
        for skill, count in results:
            print(f"{skill}: {count} job postings")
    else:
        print("No matching job postings found.")