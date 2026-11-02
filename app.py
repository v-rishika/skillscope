
import streamlit as st
from src.resume_view import render_resume_analyzer
from src.data_processor import load_job_data
from src.skill_analyzer import get_available_skills
from src.styles import apply_styles
from src.home_view import render_home
from src.results_view import render_results
from src.career_guide_view import render_career_guide
from src.job_matcher_view import render_job_matcher

st.set_page_config(
    page_title="SkillScope — Career Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_styles()

try:
    df = load_job_data()
    available_skills = get_available_skills(df)
except Exception:
    st.error(
        "We couldn't load the job-market data. "
        "Please check the dataset file and try again."
    )
    st.stop()

if "skill_input" not in st.session_state:
    st.session_state.skill_input = ""

if "results_ready" not in st.session_state:
    st.session_state.results_ready = False


from src.career_guide_view import render_career_guide

page = st.radio(
    "Navigate",
    ["Skill Analyzer", "AI Career Guide", "Resume Analyzer", "Job Description Matcher"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "AI Career Guide":
    render_career_guide()
elif page == "Resume Analyzer":
    render_resume_analyzer()
elif page == "Job Description Matcher":
    render_job_matcher()
elif st.session_state.results_ready:
    render_results(df, available_skills)
else:
    render_home()