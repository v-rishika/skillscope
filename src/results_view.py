import streamlit as st

from src.skill_analyzer import analyze_skill_gap


ALIASES = {
    "js": "javascript",
    "amazon web services": "aws",
    "powerbi": "power bi",
    "ci cd": "ci/cd",
    "ci-cd": "ci/cd",
}


def render_results(df, available_skills):
    raw_skills = [
        item.strip()
        for item in st.session_state.skill_input.replace(
            "\n", ","
        ).split(",")
        if item.strip()
    ]

    skills = []
    seen = set()
    unknown = []

    for item in raw_skills:
        skill = ALIASES.get(
            item.casefold(),
            item.casefold(),
        )

        if skill in available_skills:
            if skill not in seen:
                skills.append(skill)
                seen.add(skill)
        elif item not in unknown:
            unknown.append(item)

    st.markdown(
        '<div class="eyebrow">02 / Your career landscape</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Roles that connect with your skills.")

    st.markdown(
        "Explore how your skills align with different career paths."
    )

    if not skills:
        st.warning(
            "We couldn't match those skills to the available job data. "
            "Try entering skills such as Python, SQL, AWS, or Docker."
        )

        if st.button("← Edit my skills"):
            st.session_state.results_ready = False
            st.rerun()

        return

    st.caption("Your skills · " + " · ".join(skills))

    if unknown:
        st.caption(
            "We couldn't match these skills: "
            + ", ".join(unknown)
            + ". Check their spelling or try related terms."
        )

    results = [
        analyze_skill_gap(
            df,
            role,
            skills,
        )
        for role in sorted(
            df["job_title"].dropna().unique()
        )
    ]

    results = [
        result
        for result in results
        if result["total_postings"] > 0
    ]

    results.sort(
        key=lambda result: result["match_percentage"],
        reverse=True,
    )

    st.markdown(
        '<div class="section-label">TOP 5 ROLE MATCHES</div>',
        unsafe_allow_html=True,
    )

    for rank, result in enumerate(
        results[:5],
        start=1,
    ):
        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.markdown(
                    f"### {rank:02d}  {result['role']}"
                )

            with right:
                st.metric(
                    "Skill coverage",
                    f"{result['match_percentage']:.1f}%",
                    help=(
                        f"{len(result['matched_skills'])} "
                        "skills overlap with this role's requirements."
                    ),
                )

            st.progress(
                min(
                    max(
                        result["match_percentage"] / 100,
                        0,
                    ),
                    1,
                ),
                text="Skill overlap with this role",
            )

            with st.expander(
                "Explore matched and missing skills"
            ):
                matched, missing = st.columns(2)

                with matched:
                    st.markdown("**Skills you have**")

                    if result["matched_skills"]:
                        for skill, _ in result["matched_skills"][:10]:
                            st.write(f"✓ {skill}")
                    else:
                        st.write(
                            "No overlapping skills found."
                        )

                with missing:
                    st.markdown(
                        "**Skills to explore next**"
                    )

                    if result["missing_skills"]:
                        for skill, _ in result["missing_skills"][:10]:
                            st.write(f"+ {skill}")
                    else:
                        st.write(
                            "No additional skills identified."
                        )

                st.caption(
                    "Suggested skills are ordered by how often "
                    "they appear in role requirements, not by "
                    "learning difficulty. Skill coverage is an "
                    "indicator of overlap, not a hiring probability "
                    "or a guarantee of qualification."
                )

    if len(results) > 5:
        with st.expander(
            "Explore all remaining roles"
        ):
            for result in results[5:]:
                st.write(
                    f"**{result['role']}** — "
                    f"{result['match_percentage']:.1f}% coverage"
                )

    if st.button("← Edit my skills"):
        st.session_state.results_ready = False
        st.rerun()