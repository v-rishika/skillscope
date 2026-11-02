import re

from src.resume_analyzer import (
    RESUME_SKILLS,
    extract_resume_skills,
)

from src.skill_analyzer import SKILL_ALIASES


RELATED_SKILLS = {
    "mysql": ["sql"],
    "postgresql": ["sql"],
    "postgres": ["sql"],
    "oracle": ["sql"],
    "microsoft sql server": ["sql"],
    "github": ["git"],
    "gitlab": ["git"],
    "bitbucket": ["git"],
    "amazon web services": ["aws"],
    "amazon aws": ["aws"],
    "gcp": ["google cloud"],
    "google cloud platform": ["google cloud"],
    "kali linux": ["linux"],
    "react.js": ["react"],
    "node.js": ["node"],
}


COMMON_JD_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "oracle",
    "mongodb",
    "redis",
    "firebase",
    "html",
    "css",
    "react",
    "react.js",
    "angular",
    "vue",
    "node",
    "node.js",
    "express",
    "spring",
    "spring boot",
    "django",
    "flask",
    "fastapi",
    "rest",
    "rest api",
    "rest apis",
    "api",
    "apis",
    "git",
    "github",
    "gitlab",
    "docker",
    "kubernetes",
    "aws",
    "amazon web services",
    "azure",
    "microsoft azure",
    "google cloud",
    "gcp",
    "linux",
    "unix",
    "windows",
    "kali linux",
    "wireshark",
    "burp suite",
    "nmap",
    "cybersecurity",
    "cyber security",
    "ethical hacking",
    "penetration testing",
    "penetration test",
    "vulnerability assessment",
    "vulnerability management",
    "threat detection",
    "threat hunting",
    "incident response",
    "security operations",
    "soc",
    "siem",
    "splunk",
    "microsoft sentinel",
    "sentinel",
    "defender",
    "microsoft defender",
    "active directory",
    "entra id",
    "identity and access management",
    "iam",
    "network security",
    "firewalls",
    "firewall",
    "tcp/ip",
    "dns",
    "http",
    "https",
    "networking",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "data analytics",
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
    "excel",
    "jenkins",
    "ci/cd",
    "terraform",
    "ansible",
    "microservices",
    "agile",
    "scrum",
}


REQUIRED_MARKERS = (
    "required",
    "must have",
    "must-have",
    "essential",
    "mandatory",
    "minimum",
    "need to have",
    "you must",
    "strong knowledge",
    "strong experience",
    "required skills",
    "required qualifications",
    "essential skills",
    "essential qualifications",
)


PREFERRED_MARKERS = (
    "preferred",
    "preferably",
    "nice to have",
    "nice-to-have",
    "good to have",
    "good-to-have",
    "bonus",
    "plus",
    "desired",
    "desirable",
    "preferred skills",
    "preferred qualifications",
)


def normalize_text(text):
    """Normalize text for reliable matching."""

    if not isinstance(text, str):
        return ""

    text = text.casefold()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("’", "'")

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def canonicalize_skill(skill):
    """Convert a skill into its canonical form."""

    skill = skill.strip().casefold()

    aliases = {
        **SKILL_ALIASES,
        "cyber security": "cybersecurity",
        "amazon web services": "aws",
        "amazon aws": "aws",
        "microsoft azure": "azure",
        "google cloud platform": "google cloud",
        "react.js": "react",
        "node.js": "node",
        "rest api": "rest apis",
        "restful api": "rest apis",
        "restful apis": "rest apis",
        "apis": "api",
    }

    return aliases.get(
        skill,
        skill,
    )


def get_skill_candidates():
    """Return all skills the matcher knows about."""

    candidates = set(RESUME_SKILLS)

    candidates.update(
        SKILL_ALIASES.keys()
    )

    candidates.update(
        COMMON_JD_SKILLS
    )

    return candidates


def extract_jd_skills(job_description):
    """Extract recognizable technical skills from a JD."""

    text = normalize_text(job_description)

    if not text:
        return []

    detected_skills = set()

    for skill in sorted(
        get_skill_candidates(),
        key=len,
        reverse=True,
    ):
        skill = skill.strip().casefold()

        if not skill:
            continue

        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text):
            detected_skills.add(
                canonicalize_skill(skill)
            )

    return sorted(detected_skills)


def expand_related_skills(skills):
    """Expand skills using known relationships."""

    expanded = {
        canonicalize_skill(skill)
        for skill in skills
        if skill.strip()
    }

    for skill in list(expanded):
        expanded.update(
            RELATED_SKILLS.get(
                skill,
                [],
            )
        )

    return expanded


def get_skill_context(
    job_description,
    skill,
):
    """
    Determine whether a skill appears in required,
    preferred, or general JD wording.
    """

    text = normalize_text(job_description)

    skill = canonicalize_skill(skill)

    # Look for the skill in the original text.
    matches = list(
        re.finditer(
            rf"(?<!\w){re.escape(skill)}(?!\w)",
            text,
        )
    )

    # Also check common aliases.
    if not matches:
        for alias, canonical in SKILL_ALIASES.items():

            if canonicalize_skill(alias) != skill:
                continue

            matches = list(
                re.finditer(
                    rf"(?<!\w){re.escape(alias.casefold())}(?!\w)",
                    text,
                )
            )

            if matches:
                break

    if not matches:
        return "general"

    for match in matches:
        start = max(
            0,
            match.start() - 100,
        )

        end = min(
            len(text),
            match.end() + 100,
        )

        context = text[start:end]

        if any(
            marker in context
            for marker in REQUIRED_MARKERS
        ):
            return "required"

        if any(
            marker in context
            for marker in PREFERRED_MARKERS
        ):
            return "preferred"

    return "general"


def classify_jd_skills(
    job_description,
    jd_skills,
):
    """
    Classify JD skills into required, preferred and general.
    """

    required = []
    preferred = []
    general = []

    for skill in jd_skills:

        category = get_skill_context(
            job_description,
            skill,
        )

        if category == "required":
            required.append(skill)

        elif category == "preferred":
            preferred.append(skill)

        else:
            general.append(skill)

    return {
        "required": sorted(required),
        "preferred": sorted(preferred),
        "general": sorted(general),
    }


def get_match_strength(match_percentage):
    """Convert percentage into a simple match strength."""

    if match_percentage >= 80:
        return "Strong"

    if match_percentage >= 60:
        return "Good"

    if match_percentage >= 40:
        return "Moderate"

    return "Low"


def build_match_explanation(
    match_percentage,
    matched_skills,
    missing_skills,
    required_missing,
    preferred_missing,
):
    """Create a concise explanation of the match."""

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    if not matched_count:
        return (
            "Your resume does not currently show a strong "
            "overlap with the skills identified in this job description."
        )

    if not missing_count:
        return (
            "Your resume covers all of the technical skills "
            "identified in this job description."
        )

    if required_missing:
        return (
            f"You have {matched_count} matching skill"
            f"{'s' if matched_count != 1 else ''}, "
            f"but there "
            f"{'are' if len(required_missing) != 1 else 'is'} "
            f"{len(required_missing)} required skill"
            f"{'s' if len(required_missing) != 1 else ''} "
            "still missing. Prioritize those before the "
            "preferred skills."
        )

    if preferred_missing:
        return (
            f"You cover the identified required skills. "
            f"The remaining gap"
            f"{'s' if len(preferred_missing) != 1 else ''} "
            "are mainly preferred skills, so they are useful "
            "areas for strengthening your profile rather than "
            "core requirements."
        )

    return (
        f"You have {matched_count} matching skill"
        f"{'s' if matched_count != 1 else ''} "
        f"and {missing_count} remaining skill"
        f"{'s' if missing_count != 1 else ''} "
        "to explore."
    )


def match_resume_to_jd(
    resume_skills,
    job_description,
):
    """Compare resume skills against a job description."""

    jd_skills = set(
        extract_jd_skills(
            job_description
        )
    )

    normalized_resume_skills = {
        canonicalize_skill(skill)
        for skill in resume_skills
        if skill.strip()
    }

    expanded_resume_skills = expand_related_skills(
        normalized_resume_skills
    )

    matched_skills = sorted(
        jd_skills & expanded_resume_skills
    )

    missing_skills = sorted(
        jd_skills - expanded_resume_skills
    )

    classification = classify_jd_skills(
        job_description,
        jd_skills,
    )

    required_skills = set(
        classification["required"]
    )

    preferred_skills = set(
        classification["preferred"]
    )

    required_missing = sorted(
        required_skills - expanded_resume_skills
    )

    preferred_missing = sorted(
        preferred_skills - expanded_resume_skills
    )

    # Weighted score:
    # Required skills = 70%
    # Preferred skills = 20%
    # General skills = 10%
    #
    # If a category doesn't exist in the JD,
    # its weight is redistributed.

    categories = [
        (
            required_skills,
            expanded_resume_skills,
            70,
        ),
        (
            preferred_skills,
            expanded_resume_skills,
            20,
        ),
        (
            set(classification["general"]),
            expanded_resume_skills,
            10,
        ),
    ]

    active_categories = [
        category
        for category in categories
        if category[0]
    ]

    total_weight = sum(
        category[2]
        for category in active_categories
    )

    weighted_score = 0

    for skills, resume, weight in active_categories:

        category_match = (
            len(skills & resume)
            / len(skills)
        )

        weighted_score += (
            category_match
            * weight
        )

    match_percentage = (
        weighted_score
        / total_weight
        * 100
        if total_weight
        else 0
    )

    match_percentage = round(
        match_percentage,
        1,
    )

    match_strength = get_match_strength(
        match_percentage
    )

    explanation = build_match_explanation(
        match_percentage,
        matched_skills,
        missing_skills,
        required_missing,
        preferred_missing,
    )

    return {
        "jd_skills": sorted(jd_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
        "general_skills": sorted(
            classification["general"]
        ),
        "required_missing": required_missing,
        "preferred_missing": preferred_missing,
        "match_percentage": match_percentage,
        "match_strength": match_strength,
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "explanation": explanation,
    }


def match_resume_text_to_jd(
    resume_text,
    job_description,
):
    """Extract resume skills and compare them with a JD."""

    resume_skills = extract_resume_skills(
        resume_text
    )

    result = match_resume_to_jd(
        resume_skills,
        job_description,
    )

    result["resume_skills"] = sorted(
        resume_skills
    )

    return result