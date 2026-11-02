import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap'
        );


        /* =========================================================
           ROOT
        ========================================================= */

        :root {
            --paper: #F6F2E9;
            --ink: #172B4D;
            --muted: #72766F;
            --line: #DCD6C9;
            --accent: #C16D4A;
            --white: #FFFEFA;
        }


        /* =========================================================
           APP
        ========================================================= */

        .stApp {
            background: var(--paper);
            color: var(--ink);
            font-family: 'DM Sans', sans-serif;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1220px;
            padding: 2rem 2rem 5rem;
        }


        /* =========================================================
           TYPOGRAPHY
        ========================================================= */

        h1,
        h2,
        h3 {
            color: var(--ink) !important;
            font-family: 'Playfair Display', Georgia, serif !important;
            letter-spacing: -0.035em;
        }

        p,
        label,
        li,
        .stMarkdown {
            color: var(--ink);
        }


        /* =========================================================
           EDITORIAL ELEMENTS
        ========================================================= */

        .eyebrow {
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.17em;
            text-transform: uppercase;
        }

        .brand {
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            color: var(--ink);
        }

        .brand-mark {
            color: var(--accent);
            font-size: 1.35rem;
            margin-right: 0.45rem;
        }

        .hero {
            padding: 4.3rem 0 3.3rem;
            border-bottom: 1px solid var(--line);
        }

        .hero-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(3rem, 6vw, 5.4rem);
            line-height: 1.02;
            letter-spacing: -0.055em;
            color: var(--ink);
            margin: 1rem 0;
        }

        .hero-title em {
            color: var(--accent);
            font-weight: 500;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.8;
            max-width: 460px;
        }

        .hero-note {
            border-left: 2px solid var(--accent);
            padding: 0.25rem 0 0.25rem 1rem;
            margin-top: 1.6rem;
            color: var(--muted);
            font-size: 0.85rem;
            line-height: 1.7;
        }

        .section-label {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--muted);
        }


        /* =========================================================
           TEXT AREA
        ========================================================= */

        .stTextArea textarea {
            background: var(--white) !important;
            color: var(--ink) !important;
            border: 1px solid var(--line) !important;
            border-radius: 4px !important;
            font-size: 1rem !important;
            line-height: 1.8 !important;
        }

        .stTextArea textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }


        /* =========================================================
           ALL STREAMLIT BUTTONS

           No hover / active / focus color change.
        ========================================================= */

        .stButton > button,
        .stFormSubmitButton > button {
            background: var(--ink) !important;
            color: var(--white) !important;
            border: 1px solid var(--ink) !important;
            border-radius: 3px !important;
            min-height: 44px;
            padding: 0.65rem 1.2rem !important;
            font-weight: 600 !important;
            opacity: 1 !important;
            visibility: visible !important;
            box-shadow: none !important;
            transform: none !important;
        }

        .stButton > button:hover,
        .stButton > button:active,
        .stButton > button:focus,
        .stButton > button:focus-visible,
        .stFormSubmitButton > button:hover,
        .stFormSubmitButton > button:active,
        .stFormSubmitButton > button:focus,
        .stFormSubmitButton > button:focus-visible {
            background: var(--ink) !important;
            color: var(--white) !important;
            border: 1px solid var(--ink) !important;
            box-shadow: none !important;
            outline: none !important;
            transform: none !important;
        }

        .stButton > button *,
        .stFormSubmitButton > button * {
            color: var(--white) !important;
            -webkit-text-fill-color: var(--white) !important;
            opacity: 1 !important;
            visibility: visible !important;
        }


        /* =========================================================
           FILE UPLOADER

           White Upload text + icon.
           No hover change.
        ========================================================= */

        .stFileUploader button {
            background: transparent !important;
            color: var(--white) !important;
            border: 1px solid var(--line) !important;
            box-shadow: none !important;
            transform: none !important;
        }

        .stFileUploader button:hover,
        .stFileUploader button:active,
        .stFileUploader button:focus,
        .stFileUploader button:focus-visible {
            background: transparent !important;
            color: var(--white) !important;
            border: 1px solid var(--line) !important;
            box-shadow: none !important;
            outline: none !important;
            transform: none !important;
        }

        .stFileUploader button span,
        .stFileUploader button p,
        .stFileUploader button div,
        .stFileUploader button label {
            color: var(--white) !important;
            -webkit-text-fill-color: var(--white) !important;
        }

        .stFileUploader button:hover span,
        .stFileUploader button:hover p,
        .stFileUploader button:hover div,
        .stFileUploader button:hover label {
            color: var(--white) !important;
            -webkit-text-fill-color: var(--white) !important;
        }

        .stFileUploader button svg {
            color: var(--white) !important;
            fill: var(--white) !important;
            stroke: var(--white) !important;
        }

        .stFileUploader button:hover svg {
            color: var(--white) !important;
            fill: var(--white) !important;
            stroke: var(--white) !important;
        }


        /* =========================================================
           DATA EDITOR
        ========================================================= */

        div[data-testid="stDataEditor"] {
            border: 1px solid var(--line);
            border-radius: 4px;
            overflow: hidden;
        }


        /* =========================================================
           ALERTS
        ========================================================= */

        div[data-testid="stAlert"] {
            border-radius: 4px;
        }


        /* =========================================================
           METRICS
        ========================================================= */

        div[data-testid="stMetric"] {
            background: var(--white);
            padding: 1rem;
            border: 1px solid var(--line);
            border-radius: 4px;
        }


        /* =========================================================
           EXPANDERS
        ========================================================= */

        div[data-testid="stExpander"] details summary {
            background-color: transparent !important;
            color: var(--ink) !important;
            border: 1px solid var(--line) !important;
        }

        div[data-testid="stExpander"] details summary:hover {
            background-color: transparent !important;
            color: var(--ink) !important;
        }

        div[data-testid="stExpander"] details summary p {
            color: var(--ink) !important;
        }

        div[data-testid="stExpander"] details summary:hover p {
            color: var(--ink) !important;
        }


        /* =========================================================
           AI CAREER GUIDE INPUT
        ========================================================= */

        .stChatInput,
        .stChatInput > div,
        .stChatInput textarea {
            background-color: #FFFFFF !important;
        }

        .stChatInput textarea,
        .stChatInput textarea:focus {
            color: #17243A !important;
            -webkit-text-fill-color: #17243A !important;
            caret-color: #17243A !important;
            opacity: 1 !important;
        }

        .stChatInput textarea::placeholder {
            color: #6B7280 !important;
            -webkit-text-fill-color: #6B7280 !important;
            opacity: 1 !important;
        }


        /* =========================================================
           PREVIOUS CONVERSATION SELECTOR

           Remove the I-beam mouse cursor and the blinking text
           caret from the BaseWeb select, while keeping the
           dropdown clickable (hand cursor everywhere).
        ========================================================= */

        /* Hand cursor + no caret + no text selection on the whole select */
        .stApp div[data-baseweb="select"],
        .stApp div[data-baseweb="select"] *,
        .stApp .stSelectbox,
        .stApp .stSelectbox *,
        .stApp div[data-testid="stSelectbox"],
        .stApp div[data-testid="stSelectbox"] * {
            cursor: pointer !important;
            caret-color: transparent !important;
            -webkit-user-select: none !important;
            user-select: none !important;
        }

        /* Hide the internal search input and make it ignore the mouse,
           so clicks go to the select itself (no I-beam, no caret) */
        .stApp div[data-baseweb="select"] input,
        .stApp div[data-baseweb="select"] input[role="combobox"],
        .stApp div[data-baseweb="select"] input[aria-autocomplete],
        .stApp div[data-baseweb="select"] input[aria-autocomplete="list"],
        .stApp div[data-baseweb="select"] input:focus {
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            min-width: 1px !important;
            min-height: 1px !important;

            padding: 0 !important;
            margin: 0 !important;

            opacity: 0 !important;
            pointer-events: none !important;

            border: 0 !important;
            outline: none !important;

            color: transparent !important;
            caret-color: transparent !important;
            -webkit-text-fill-color: transparent !important;

            cursor: pointer !important;
        }

        /* Displayed selected value */
        .stApp div[data-baseweb="select"] [role="combobox"] {
            cursor: pointer !important;
            caret-color: transparent !important;
            outline: none !important;
        }

        /* Dropdown list is rendered in a portal outside the select */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] *,
        ul[role="listbox"],
        ul[role="listbox"] *,
        li[role="option"] {
            cursor: pointer !important;
            caret-color: transparent !important;
        }


        /* =========================================================
           DIVIDERS
        ========================================================= */

        hr {
            border-color: var(--line) !important;
        }


        /* =========================================================
           FOOTER
        ========================================================= */

        .footer {
            border-top: 1px solid var(--line);
            padding-top: 1rem;
            margin-top: 4rem;
            color: var(--muted);
            font-size: 0.78rem;
        }


        /* =========================================================
           MOBILE
        ========================================================= */

        @media (max-width: 700px) {

            .block-container {
                padding: 1.2rem 1rem 3rem;
            }

            .hero {
                padding: 2.5rem 0 2rem;
            }

            .hero-title {
                font-size: 3.1rem;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )