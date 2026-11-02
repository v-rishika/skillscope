
import streamlit as st


def render_home():
    brand_left, brand_right = st.columns([3, 1])

    with brand_left:
        st.markdown(
            '<div class="brand"><span class="brand-mark">◈</span>'
            'SKILLSCOPE</div>',
            unsafe_allow_html=True,
        )

    with brand_right:
        st.markdown(
            '<div style="text-align:right;color:#72766F;'
            'font-size:.78rem;padding-top:.25rem;">'
            'CAREER INTELLIGENCE · 01</div>',
            unsafe_allow_html=True,
        )

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("""
        <div class="hero">
            <div class="eyebrow">Your skills. Your next move.</div>
            <div class="hero-title">
                See the skills<br>behind <em>every role.</em>
            </div>
            <div class="hero-copy">
                Turn what you know into a clearer career direction.
                Discover how your current skills connect with different roles
            </div>
            <div class="hero-note">
                Built around skills, role-level demand, and transparent
                comparisons — not vague career guesses.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='height:2.1rem'></div>",
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-label">'
            '01 / Start with your skills</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### What do you already know?")
        st.markdown(
            "<p style='color:#72766F;line-height:1.7;'>"
            "Enter your technical skills to discover roles that "
            "overlap with your current skill set.</p>",
            unsafe_allow_html=True,
        )

        with st.form("skill_input_form"):
            skills = st.text_area(
                "Your skills",
                value=st.session_state.skill_input,
                placeholder="Python, SQL, Docker, AWS, Git...",
                height=145,
                label_visibility="collapsed",
            )
            st.caption("TIP · Start with skills you can actually use.")

            submitted = st.form_submit_button(
                "Find my matching roles  →",
                use_container_width=True,
            )

        if submitted:
            st.session_state.skill_input = skills
            st.session_state.results_ready = True
            st.rerun()