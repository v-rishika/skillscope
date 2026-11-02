
from pathlib import Path
import pandas as pd

# Locate the project folder automatically
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "job_postings.csv"


def load_job_data():
    """Load and validate the job postings dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Check the minimum columns needed
    required_columns = {"job_title", "skills_required"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(sorted(missing))}. "
            f"Available columns: {', '.join(df.columns)}"
        )

    # Remove rows without job titles or skill information
    df = df.dropna(
        subset=["job_title", "skills_required"]
    ).copy()

    df["job_title"] = df["job_title"].astype(str).str.strip()
    df["skills_required"] = (
        df["skills_required"].astype(str).str.strip()
    )

    df = df[
        df["job_title"].ne("")
        & df["skills_required"].ne("")
    ]

    return df.reset_index(drop=True)