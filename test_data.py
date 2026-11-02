
from src.data_processor import load_job_data

df = load_job_data()

print("Total job postings:", len(df))
print("\nAll column names:")

for column in df.columns:
    print("-", column)

print("\nSample job title:")
print(df["job_title"].iloc[0])

print("\nSample required skills:")
print(df["skills_required"].iloc[0])