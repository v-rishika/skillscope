import re

from src.skill_analyzer import SKILL_ALIASES, analyze_skill_gap


RESUME_SKILLS = {
    # Programming languages
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "go",
    "rust",
    "php",
    "ruby",

    # Web development
    "html",
    "css",
    "react",
    "react.js",
    "angular",
    "vue",
    "node.js",
    "node",
    "express",
    "django",
    "flask",
    "jsp",
    "servlets",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "oracle",
    "firebase",
    "firestore",
    "jdbc",

    # Data / Python ecosystem
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "tensorflow",
    "pytorch",

    # Cloud
    "aws",
    "amazon web services",
    "azure",
    "google cloud",
    "gcp",

    # DevOps / tools
    "git",
    "github",
    "gitlab",
    "docker",
    "kubernetes",
    "jenkins",
    "ci/cd",
    "linux",
    "windows",

    # Cybersecurity
    "cybersecurity",
    "information security",
    "ethical hacking",
    "penetration testing",
    "vulnerability assessment",
    "vulnerability scanning",
    "threat detection",
    "network security",
    "web security",
    "application security",
    "soc",
    "siem",
    "wireshark",
    "burp suite",
    "nmap",
    "kali linux",
    "metasploit",
    "metasploitable",

    # Servers / frameworks
    "apache tomcat",
    "tomcat",
    "spring",
    "spring boot",

    # AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "computer vision",

    # General technical skills
    "data structures",
    "algorithms",
    "object oriented programming",
    "oop",
    "rest api",
    "rest apis",
    "api",
}


RELATED_SKILLS = {
    "mysql": ["sql"],
    "postgresql": ["sql"],
    "postgres": ["sql"],
    "oracle": ["sql"],

    "react.js": ["react"],
    "node.js": ["node"],

    "github": ["git"],
    "gitlab": ["git"],

    "amazon web services": ["aws"],
    "gcp": ["google cloud"],

    "kali linux": ["linux"],
}


def extract_resume_skills(resume_text):
    """
    Detect technical skills from resume text.
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        return []

    text = resume_text.casefold()

    skill_candidates = set(RESUME_SKILLS)

    for alias, canonical in SKILL_ALIASES.items():
        skill_candidates.add(alias)

    detected_skills = set()

    sorted_skills = sorted(
        skill_candidates,
        key=len,
        reverse=True,
    )

    for skill in sorted_skills:
        skill = skill.strip()

        if not skill:
            continue

        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text):
            canonical = SKILL_ALIASES.get(skill, skill)
            detected_skills.add(canonical)

    return sorted(detected_skills)


def _expand_related_skills(resume_skills):
    """
    Add related skills for role matching without changing
    the original skills detected from the resume.
    """

    expanded_skills = set(resume_skills)

    for skill in resume_skills:
        related = RELATED_SKILLS.get(skill, [])

        for related_skill in related:
            expanded_skills.add(related_skill)

    return sorted(expanded_skills)


def _get_skill_source(skill, resume_skills):
    """
    Explain whether a role skill is directly present or
    supported by a related resume skill.
    """

    if skill in resume_skills:
        return skill

    for resume_skill in resume_skills:
        related = RELATED_SKILLS.get(resume_skill, [])

        if skill in related:
            return f"{skill} (via {resume_skill})"

    return skill


def recommend_roles(df, resume_skills, top_n=5):
    """
    Recommend job roles using a hybrid role-fit score.

    70% of the score comes from unique skill coverage.
    30% comes from posting-frequency-weighted skill coverage.
    """

    if not resume_skills:
        return []

    roles = (
        df["job_title"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    expanded_skills = _expand_related_skills(
        resume_skills
    )

    recommendations = []

    for role in roles:
        result = analyze_skill_gap(
            df,
            role,
            expanded_skills,
        )

        if result["total_postings"] == 0:
            continue

        matched = result["matched_skills"]
        missing = result["missing_skills"]

        total_unique_skills = len(matched) + len(missing)

        unique_coverage = (
            len(matched) / total_unique_skills * 100
            if total_unique_skills
            else 0.0
        )

        weighted_coverage = result["match_percentage"]

        role_fit_score = (
            unique_coverage * 0.70
            + weighted_coverage * 0.30
        )

        matched_skills = [
            _get_skill_source(
                skill,
                resume_skills,
            )
            for skill, _ in matched
        ]

        recommendations.append(
            {
                "role": result["role"],
                "match_percentage": round(
                    role_fit_score,
                    1,
                ),
                "matched_skills": matched_skills,
                "missing_skills": [
                    skill
                    for skill, _ in missing
                ],
            }
        )

    recommendations.sort(
        key=lambda item: item["match_percentage"],
        reverse=True,
    )

    return recommendations[:top_n]