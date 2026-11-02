import re

from src.resume_analyzer import extract_resume_skills


SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "skills & technologies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
    ],
    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
    ],
    "education": [
        "education",
        "academic background",
        "qualifications",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "certification",
    ],
}


ACTION_VERBS = {
    "developed",
    "designed",
    "implemented",
    "built",
    "created",
    "analyzed",
    "integrated",
    "automated",
    "configured",
    "deployed",
    "tested",
    "optimized",
    "managed",
    "engineered",
    "performed",
    "applied",
    "conducted",
}


RELATED_SKILLS = {
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


def normalize_text(text):
    """Normalize resume text for analysis."""

    if not isinstance(text, str):
        return ""

    text = text.casefold()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def detect_sections(resume_text):
    """Detect standard resume sections."""

    text = normalize_text(resume_text)

    detected = {}

    for section, aliases in SECTION_ALIASES.items():
        detected[section] = any(
            re.search(
                rf"\b{re.escape(alias)}\b",
                text,
            )
            for alias in aliases
        )

    return detected


def calculate_parsing_score(resume_text):
    """
    Estimate how well the resume text can be parsed.

    This evaluates extracted text and standard sections.
    It does not judge visual design.
    """

    if not resume_text or not resume_text.strip():
        return 0

    sections = detect_sections(resume_text)

    score = 0

    if len(resume_text.strip()) >= 500:
        score += 5

    if len(resume_text.strip()) >= 1000:
        score += 5

    section_count = sum(
        sections.values()
    )

    score += min(
        section_count * 2,
        10,
    )

    return min(score, 20)


def calculate_completeness_score(resume_text):
    """Check whether important resume sections are present."""

    sections = detect_sections(resume_text)

    important_sections = [
        "skills",
        "experience",
        "projects",
        "education",
    ]

    present = sum(
        sections[section]
        for section in important_sections
    )

    return round(
        present / len(important_sections) * 10,
        1,
    )


def calculate_experience_score(resume_text):
    """Evaluate evidence of practical experience."""

    text = normalize_text(resume_text)

    sections = detect_sections(text)

    if not sections["experience"]:
        return 0

    score = 8

    experience_indicators = [
        "internship",
        "intern",
        "experience",
        "worked",
        "responsible",
        "developed",
        "implemented",
    ]

    matches = sum(
        1
        for indicator in experience_indicators
        if re.search(
            rf"\b{re.escape(indicator)}\b",
            text,
        )
    )

    score += min(
        matches,
        7,
    )

    return min(score, 15)


def calculate_project_score(resume_text):
    """Evaluate technical project evidence."""

    text = normalize_text(resume_text)

    sections = detect_sections(text)

    if not sections["projects"]:
        return 0

    score = 5

    project_indicators = [
        "developed",
        "built",
        "designed",
        "implemented",
        "created",
        "project",
        "tech stack",
        "technologies",
    ]

    matches = sum(
        1
        for indicator in project_indicators
        if re.search(
            rf"\b{re.escape(indicator)}\b",
            text,
        )
    )

    score += min(
        matches * 2,
        10,
    )

    return min(score, 15)


def calculate_content_quality_score(resume_text):
    """
    Evaluate basic evidence of strong resume writing.

    This is intentionally conservative and does not claim
    to understand the quality of every sentence.
    """

    text = normalize_text(resume_text)

    if not text:
        return 0

    score = 0

    action_matches = sum(
        1
        for verb in ACTION_VERBS
        if re.search(
            rf"\b{re.escape(verb)}\b",
            text,
        )
    )

    score += min(
        action_matches,
        5,
    )

    if re.search(
        r"\b\d+%|\b\d+\+|\b\d+\s*(users|projects|months|years|days)\b",
        text,
    ):
        score += 3

    word_count = len(text.split())

    if 300 <= word_count <= 1500:
        score += 2

    return min(score, 10)


def get_role_skills(df, target_role):
    """
    Get the distinct skills required for a target role.
    """

    if df is None or not target_role:
        return set()

    role_jobs = df[
        df["job_title"].str.casefold()
        == target_role.strip().casefold()
    ]

    if role_jobs.empty:
        return set()

    required_skills = set()

    for skill_text in role_jobs["skills_required"].dropna():
        for skill in skill_text.split("|"):
            skill = skill.strip().casefold()

            if skill:
                required_skills.add(skill)

    return required_skills


def expand_related_skills(skills):
    """
    Add legitimate related skills for matching.
    """

    expanded = {
        skill.strip().casefold()
        for skill in skills
        if skill.strip()
    }

    for skill in list(expanded):
        expanded.update(
            RELATED_SKILLS.get(skill, [])
        )

    return expanded


def calculate_keyword_score(
    resume_text,
    df,
    target_role,
):
    """
    Calculate the 30-point target-role keyword score.

    Each distinct required skill contributes equally.
    Related skills such as MySQL -> SQL are supported.
    """

    if not resume_text or not target_role:
        return 0

    required_skills = get_role_skills(
        df,
        target_role,
    )

    if not required_skills:
        return 0

    resume_skills = extract_resume_skills(
        resume_text
    )

    expanded_resume_skills = expand_related_skills(
        resume_skills
    )

    matched = {
        skill
        for skill in required_skills
        if skill in expanded_resume_skills
    }

    coverage = (
        len(matched)
        / len(required_skills)
    )

    return round(
        coverage * 30,
        1,
    )


def calculate_ats_score(
    resume_text,
    df=None,
    target_role=None,
):
    """
    Calculate a transparent ATS-style resume score.

    Maximum score: 100.

    The score is an estimate of compatibility with the
    selected role. It is not a prediction of whether a
    real ATS will accept or rank the resume.
    """

    scores = {
        "parsing": calculate_parsing_score(
            resume_text
        ),
        "keywords": calculate_keyword_score(
            resume_text,
            df,
            target_role,
        ),
        "experience": calculate_experience_score(
            resume_text
        ),
        "projects": calculate_project_score(
            resume_text
        ),
        "completeness": calculate_completeness_score(
            resume_text
        ),
        "content_quality": calculate_content_quality_score(
            resume_text
        ),
    }

    total = sum(
        scores.values()
    )

    return {
        "score": min(
            round(total),
            100,
        ),
        "components": scores,
    }