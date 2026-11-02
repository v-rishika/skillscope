import streamlit as st

from src.ats_analyzer import (
    RELATED_SKILLS,
    calculate_ats_score,
    expand_related_skills,
    get_role_skills,
)
from src.data_processor import load_job_data
from src.resume_analyzer import (
    extract_resume_skills,
    recommend_roles,
)
from src.resume_parser import extract_resume_text


def render_resume_analyzer():
    st.markdown("## Resume Analyzer")

    st.markdown(
        "Upload your resume to discover roles that match "
        "your current skills."
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX",
    )

    if uploaded_file is None:
        return

    try:
        resume_text = extract_resume_text(uploaded_file)

        df = load_job_data()

        resume_skills = extract_resume_skills(
            resume_text
        )

        recommendations = recommend_roles(
            df,
            resume_skills,
        )

        st.success("Resume analyzed successfully.")

        # ----------------------------------------
        # ATS SCORE + TARGET ROLE
        # ----------------------------------------

        st.markdown("### ATS-style resume analysis")

        role_options = sorted(
            df["job_title"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        ats_col, role_col = st.columns([1, 1])

        with role_col:
            target_role = st.selectbox(
                "Choose a target role",
                role_options,
                key="ats_target_role",
            )

        ats_result = calculate_ats_score(
            resume_text,
            df,
            target_role,
        )

        score = ats_result["score"]
        components = ats_result["components"]

        with ats_col:
            st.metric(
                "ATS-style compatibility",
                f"{score}/100",
            )

        st.caption(
            "This is an estimate of how well your resume "
            "matches the selected role. It is not a prediction "
            "of how a specific company's ATS will rank your resume."
        )

        # ----------------------------------------
        # BEST-FIT ROLES
        # ----------------------------------------

        st.markdown("### Best-fit roles")

        st.caption(
            "Based on the skills detected in your resume."
        )

        if recommendations:
            top_recommendations = recommendations[:3]

            role_columns = st.columns(3)

            for rank, recommendation in enumerate(
                top_recommendations,
                start=1,
            ):
                with role_columns[rank - 1]:
                    with st.container(border=True):
                        st.markdown(
                            f"### {rank:02d} "
                            f"{recommendation['role']}"
                        )

                        st.metric(
                            "Skill coverage",
                            f"{recommendation['match_percentage']:.1f}%",
                        )

                        st.progress(
                            min(
                                max(
                                    recommendation[
                                        "match_percentage"
                                    ] / 100,
                                    0,
                                ),
                                1,
                            )
                        )

                        with st.expander("Why this role?"):
                            matched = recommendation[
                                "matched_skills"
                            ]

                            missing = recommendation[
                                "missing_skills"
                            ]

                            st.markdown("**Skills you have**")

                            if matched:
                                for skill in matched[:5]:
                                    st.write(
                                        f"✓ {skill}"
                                    )
                            else:
                                st.write(
                                    "No overlapping skills found."
                                )

                            st.markdown(
                                "**Skills to explore next**"
                            )

                            if missing:
                                for skill in missing[:5]:
                                    st.write(
                                        f"+ {skill}"
                                    )
                            else:
                                st.write(
                                    "No additional skills identified."
                                )

                            st.caption(
                                "Skill coverage measures overlap "
                                "between your resume and the role "
                                "requirements. It is not a hiring "
                                "probability or a guarantee of "
                                "qualification."
                            )

        else:
            st.info(
                "We couldn't find suitable role matches "
                "from the skills detected in your resume."
            )

        # ----------------------------------------
        # ATS SCORE BREAKDOWN
        # ----------------------------------------

        st.markdown("### ATS analysis")

        breakdown_col1, breakdown_col2 = st.columns(2)

        with breakdown_col1:
            st.write(
                f"**Parsing & structure** "
                f"{components['parsing']}/20"
            )

            st.progress(
                components["parsing"] / 20
            )

            st.write(
                f"**Target-role keywords** "
                f"{components['keywords']}/30"
            )

            st.progress(
                components["keywords"] / 30
            )

            st.write(
                f"**Experience** "
                f"{components['experience']}/15"
            )

            st.progress(
                components["experience"] / 15
            )

        with breakdown_col2:
            st.write(
                f"**Projects** "
                f"{components['projects']}/15"
            )

            st.progress(
                components["projects"] / 15
            )

            st.write(
                f"**Completeness** "
                f"{components['completeness']}/10"
            )

            st.progress(
                components["completeness"] / 10
            )

            st.write(
                f"**Content quality** "
                f"{components['content_quality']}/10"
            )

            st.progress(
                components["content_quality"] / 10
            )

        # ----------------------------------------
        # TARGET-ROLE KEYWORDS
        # ----------------------------------------

        st.markdown("### Target-role keyword analysis")

        required_skills = get_role_skills(
            df,
            target_role,
        )

        expanded_resume_skills = expand_related_skills(
            resume_skills
        )

        matched_keywords = sorted(
            required_skills & expanded_resume_skills
        )

        missing_keywords = sorted(
            required_skills - expanded_resume_skills
        )

        matched_col, missing_col = st.columns(2)

        with matched_col:
            st.markdown("**Keywords found**")

            if matched_keywords:
                for skill in matched_keywords:
                    source = skill

                    for resume_skill in resume_skills:
                        related_skills = RELATED_SKILLS.get(
                            resume_skill,
                            [],
                        )

                        if skill in related_skills:
                            source = (
                                f"{skill} "
                                f"(via {resume_skill})"
                            )
                            break

                    st.write(f"✓ {source}")

            else:
                st.write(
                    "No target-role keywords matched."
                )

        with missing_col:
            st.markdown("**Keywords to consider**")

            if missing_keywords:
                for skill in missing_keywords[:10]:
                    st.write(f"+ {skill}")
            else:
                st.write(
                    "No major target-role keyword gaps identified."
                )

    except ValueError as error:
        st.error(str(error))