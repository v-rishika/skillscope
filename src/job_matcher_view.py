import streamlit as st

from src.job_matcher import (
    extract_jd_skills,
    match_resume_text_to_jd,
)

from src.resume_parser import (
    extract_resume_text,
)


def render_job_matcher():

    st.markdown(
        "## Job Description Matcher"
    )

    st.markdown(
        "Upload a job description or paste it manually, "
        "then compare it with your resume."
    )

    # --------------------------------------------------
    # RESUME
    # --------------------------------------------------

    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        key="jd_resume",
        help="Supported formats: PDF and DOCX.",
    )

    # --------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------

    st.markdown(
        "### Job description"
    )

    jd_file = st.file_uploader(
        "Upload a job description",
        type=["pdf", "docx"],
        key="job_description_file",
        help="Supported formats: PDF and DOCX.",
    )

    st.caption(
        "Or paste the job description below."
    )

    pasted_job_description = st.text_area(
        "Job description",
        height=300,
        placeholder=(
            "Paste the complete job description here..."
        ),
        label_visibility="collapsed",
    )

    # --------------------------------------------------
    # GET JOB DESCRIPTION TEXT
    # --------------------------------------------------

    job_description = ""

    if jd_file is not None:

        try:

            job_description = extract_resume_text(
                jd_file
            )

            if job_description:
                st.success(
                    "Job description uploaded successfully."
                )

        except ValueError as error:

            st.error(
                f"Could not read the uploaded job description: {error}"
            )

            return

    # Uploaded JD takes priority over pasted JD.
    if not job_description.strip():

        job_description = (
            pasted_job_description.strip()
        )

    # --------------------------------------------------
    # WAIT FOR INPUT
    # --------------------------------------------------

    if resume_file is None:
        return

    if not job_description.strip():
        return

    # --------------------------------------------------
    # ANALYZE
    # --------------------------------------------------

    if st.button(
        "Analyze job match"
    ):

        try:

            # Extract resume text.
            resume_text = extract_resume_text(
                resume_file
            )

            # Check whether the JD contains
            # recognizable skills.
            jd_skills = extract_jd_skills(
                job_description
            )

            if not jd_skills:

                st.warning(
                    "We couldn't find enough job requirements "
                    "to analyze this job description. Try "
                    "uploading a text-based PDF/DOCX or paste "
                    "the job description directly."
                )

                return

            # Run matching engine.
            result = match_resume_text_to_jd(
                resume_text,
                job_description,
            )

            # --------------------------------------------------
            # JOB MATCH
            # --------------------------------------------------

            st.markdown(
                "### Job match"
            )

            score_col, strength_col = st.columns(
                [2, 1]
            )

            with score_col:

                st.metric(
                    "Resume ↔ JD match",
                    f"{result['match_percentage']:.1f}%",
                )

            with strength_col:

                st.metric(
                    "Match strength",
                    result["match_strength"],
                )

            st.caption(
                f"{result['matched_count']} of "
                f"{len(result['jd_skills'])} identified "
                "skills match your resume."
            )

            # --------------------------------------------------
            # EXPLANATION
            # --------------------------------------------------

            st.info(
                result["explanation"]
            )

            # --------------------------------------------------
            # SKILL ANALYSIS
            # --------------------------------------------------

            matched_col, missing_col = st.columns(
                2
            )

            # ----------------------------------------------
            # MATCHED SKILLS
            # ----------------------------------------------

            with matched_col:

                st.markdown(
                    "**Skills you have**"
                )

                if result["matched_skills"]:

                    for skill in result[
                        "matched_skills"
                    ]:

                        st.write(
                            f"✓ {skill}"
                        )

                else:

                    st.write(
                        "No matching skills detected."
                    )

            # ----------------------------------------------
            # MISSING SKILLS
            # ----------------------------------------------

            with missing_col:

                st.markdown(
                    "**Skills to explore next**"
                )

                if result["missing_skills"]:

                    for skill in result[
                        "missing_skills"
                    ]:

                        if skill in result[
                            "required_missing"
                        ]:

                            st.write(
                                f"🔴 {skill} · Required"
                            )

                        elif skill in result[
                            "preferred_missing"
                        ]:

                            st.write(
                                f"🟡 {skill} · Preferred"
                            )

                        else:

                            st.write(
                                f"+ {skill}"
                            )

                else:

                    st.write(
                        "No major skill gaps detected."
                    )

            # --------------------------------------------------
            # REQUIREMENT BREAKDOWN
            # --------------------------------------------------

            with st.expander(
                "View requirement breakdown"
            ):

                required_col, preferred_col = st.columns(
                    2
                )

                # ------------------------------------------
                # REQUIRED
                # ------------------------------------------

                with required_col:

                    st.markdown(
                        "**Required skills**"
                    )

                    if result[
                        "required_skills"
                    ]:

                        for skill in result[
                            "required_skills"
                        ]:

                            if skill in result[
                                "matched_skills"
                            ]:

                                st.write(
                                    f"✓ {skill}"
                                )

                            else:

                                st.write(
                                    f"○ {skill}"
                                )

                    else:

                        st.write(
                            "No explicitly required "
                            "skills identified."
                        )

                # ------------------------------------------
                # PREFERRED
                # ------------------------------------------

                with preferred_col:

                    st.markdown(
                        "**Preferred skills**"
                    )

                    if result[
                        "preferred_skills"
                    ]:

                        for skill in result[
                            "preferred_skills"
                        ]:

                            if skill in result[
                                "matched_skills"
                            ]:

                                st.write(
                                    f"✓ {skill}"
                                )

                            else:

                                st.write(
                                    f"○ {skill}"
                                )

                    else:

                        st.write(
                            "No explicitly preferred "
                            "skills identified."
                        )

            # --------------------------------------------------
            # SCORE EXPLANATION
            # --------------------------------------------------

            st.caption(
                "Required skills have greater weight than "
                "preferred skills when calculating the match. "
                "The score measures skill overlap and is not "
                "a hiring probability or guarantee."
            )

        except ValueError as error:

            st.error(
                str(error)
            )