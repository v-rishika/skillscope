# SkillScope — Career Intelligence Platform

**See the skills behind every role.**

SkillScope is a career intelligence web application designed to help students and early-career professionals understand their skills, explore career opportunities, evaluate their resumes, and identify skill gaps for their target roles.

Built with Python and Streamlit, SkillScope combines job-market data, resume analysis, and AI-powered career guidance in one platform.

## ✨ Features

### 1. Skill Analyzer
- Enter your existing technical skills.
- Discover the top five job roles that match your skills.
- Explore matched skills and missing skills for each role.
- Identify skills worth learning for your target career.

### 2. AI Career Guide
- Get personalized career guidance using Google's Gemini AI.
- Ask questions about career paths, technical skills, and interview preparation.
- Receive practical learning plans and recommendations.
- Create and revisit saved conversations.

### 3. Resume Analyzer
- Upload your resume in PDF or DOCX format.
- Extract technical skills from your resume.
- Discover suitable career roles based on your skills.
- View an ATS-style compatibility score for a selected role.
- Review the score breakdown, matched keywords, and missing keywords.

### 4. Job Description Matcher
- Upload a job description or paste its text.
- Compare the job requirements with your resume.
- Identify matching skills and missing skills.
- Understand how your current skill set aligns with a specific opportunity.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application interface |
| Pandas | Job-market data processing |
| Google Gemini API | AI-powered career guidance |
| SQLite | Persistent conversation storage |
| PyPDF | PDF resume text extraction |
| python-docx | DOCX resume text extraction |
| HTML and CSS | Interface styling |
| Git and GitHub | Version control and source code hosting |

## 📁 Project Structure

```text
ai-job-market-analyzer/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   └── job_postings.csv
│
└── src/
    ├── ai_career_guide.py
    ├── ats_analyzer.py
    ├── career_guide_view.py
    ├── chat_storage.py
    ├── data_processor.py
    ├── home_view.py
    ├── job_matcher.py
    ├── job_matcher_view.py
    ├── results_view.py
    ├── resume_analyzer.py
    ├── resume_parser.py
    ├── resume_view.py
    ├── skill_analyzer.py
    └── styles.py
```

## 🚀 Getting Started

Follow these steps to run SkillScope locally.

### Prerequisites

- Python 3.10 or a compatible Python version supported by the project dependencies.
- Git
- A Google Gemini API key for AI Career Guide functionality.

### 1. Clone the repository

```bash
git clone https://github.com/v-rishika/skillscope.git
cd skillscope
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project root directory:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security note:** Never commit your `.env` file or publish your API key. Keep secrets out of your source code and GitHub repository.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can access SkillScope in your browser.

## 📊 About the Analysis

SkillScope uses a job-market dataset to identify skills associated with different roles and compare those requirements with user-provided skills or resume content.

The application provides skill-overlap indicators and ATS-style compatibility estimates to help users understand potential areas for improvement.

These scores are **estimates, not hiring probabilities**. Actual hiring decisions and ATS behavior vary across employers and recruitment systems.

## 🔐 Privacy and Security

- Keep API keys and other secrets out of version control.
- Avoid uploading resumes containing sensitive information unless you are comfortable processing them through the application.
- Review the configuration of any external AI service before submitting personal information.

## 🎯 Project Goals

SkillScope aims to make career exploration more practical by helping users:

- Understand their existing technical skills.
- Discover roles aligned with their current abilities.
- Identify skill gaps.
- Evaluate resume alignment with target roles.
- Receive AI-assisted career guidance.

## 👩‍💻 Author

**Rishika V**

B.Tech Student | Aspiring Software Developer & Cybersecurity Professional

GitHub: [@v-rishika](https://github.com/v-rishika)

---

*SkillScope — See the skills behind every role.*