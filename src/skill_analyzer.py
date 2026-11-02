
from collections import Counter

# Verified aliases used for skill matching.
SKILL_ALIASES = {
    "js": "javascript",
    "amazon web services": "aws",
    "powerbi": "power bi",
    "ci cd": "ci/cd",
    "ci-cd": "ci/cd",
}


def parse_skills(skill_text):
    """Split a pipe-separated skill string into individual skills."""
    if not isinstance(skill_text, str):
        return []

    return [
        skill.strip()
        for skill in skill_text.split("|")
        if skill.strip()
    ]



def get_available_skills(df):
    """Return the distinct skills present in the dataset."""
    skills = set()

    for skill_text in df["skills_required"].dropna():
        skills.update(
            skill.strip().casefold()
            for skill in parse_skills(skill_text)
            if skill.strip()
        )

    return skills


def normalize_skill(skill, available_skills):
    """Normalize a skill using verified aliases and dataset vocabulary."""
    original = skill.strip()
    normalized = original.casefold()

    if not normalized:
        return "", "Empty"

    canonical = SKILL_ALIASES.get(normalized, normalized)

    # Only use an alias when its target exists in the dataset.
    if canonical in available_skills:
        return canonical, "Recognized"

    # The original name may exist even if the alias target doesn't.
    if normalized in available_skills:
        return normalized, "Recognized"

    return canonical, "Not found in dataset"


def build_skill_review(skill_text, available_skills):
    """Create a review list and remove duplicates after normalization."""
    if not isinstance(skill_text, str):
        return [], 0

    entries = [
        item.strip()
        for item in skill_text.replace("\n", ",").split(",")
        if item.strip()
    ]

    review = []
    seen = set()
    duplicates = 0

    for original in entries:
        canonical, status = normalize_skill(
            original, available_skills
        )

        if not canonical:
            continue

        if canonical in seen:
            duplicates += 1
            continue

        seen.add(canonical)

        review.append({
            "Skill": original,
            "Include": True,
            "Dataset match": (
                canonical if status == "Recognized" else "—"
            ),
            "Status": status,
        })

    return review, duplicates


def analyze_skill_gap(df, role, user_skills):
    """Calculate skill coverage for a role, including related skills."""

    role_jobs = df[
        df["job_title"].str.casefold() == role.strip().casefold()
    ]

    if role_jobs.empty:
        return {
            "role": role,
            "total_postings": 0,
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0.0,
        }

    required_skills = Counter()

    for skill_text in role_jobs["skills_required"].dropna():
        required_skills.update(
            skill.casefold()
            for skill in parse_skills(skill_text)
        )

    normalized_user_skills = {
        skill.strip().casefold()
        for skill in user_skills
        if skill.strip()
    }

    # Skills that can reasonably support another skill.
    related_skills = {
        "mysql": ["sql"],
        "postgresql": ["sql"],
        "postgres": ["sql"],
        "oracle": ["sql"],
        "github": ["git"],
        "gitlab": ["git"],
        "amazon web services": ["aws"],
        "gcp": ["google cloud"],
        "kali linux": ["linux"],
    }

    # Expand the user's skills for matching.
    expanded_user_skills = set(normalized_user_skills)

    for skill in normalized_user_skills:
        expanded_user_skills.update(
            related_skills.get(skill, [])
        )

    matched = {
        skill: count
        for skill, count in required_skills.items()
        if skill in expanded_user_skills
    }

    missing = {
        skill: count
        for skill, count in required_skills.items()
        if skill not in expanded_user_skills
    }

    total_mentions = sum(required_skills.values())
    matched_mentions = sum(matched.values())

    percentage = (
        matched_mentions / total_mentions * 100
        if total_mentions else 0.0
    )

    return {
        "role": role,
        "total_postings": len(role_jobs),
        "matched_skills": sorted(
            matched.items(),
            key=lambda item: item[1],
            reverse=True,
        ),
        "missing_skills": sorted(
            missing.items(),
            key=lambda item: item[1],
            reverse=True,
        ),
        "match_percentage": round(percentage, 2),
    }

