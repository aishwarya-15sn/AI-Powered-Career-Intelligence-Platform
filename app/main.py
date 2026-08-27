import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import streamlit as st

from modules.resume_parser import extract_text_from_pdf
from modules.skill_extractor import extract_skills
from modules.role_analyzer import get_job_roles, get_role_skills
from modules.skill_gap import calculate_skill_gap
from modules.recommender import recommend_resources


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Placify | Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(99, 102, 241, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 0% 45%,
                rgba(236, 72, 153, 0.08),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #f5f3ff 45%,
                #f8fafc 100%
            );
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(99, 102, 241, 0.18),
                transparent 25%
            ),
            linear-gradient(
                180deg,
                #090d24 0%,
                #0f1535 50%,
                #090d20 100%
            );

        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-logo {
        font-size: 30px;
        font-weight: 950;
        letter-spacing: -1.5px;
        margin-top: 8px;
    }

    .sidebar-subtitle {
        color: #94a3b8 !important;
        font-size: 12px;
        margin-top: 3px;
        margin-bottom: 30px;
    }

    .sidebar-heading {
        color: #818cf8 !important;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .sidebar-active {
        padding: 12px 14px;
        margin: 7px 0;
        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.22),
                rgba(139, 92, 246, 0.12)
            );

        border: 1px solid rgba(129, 140, 248, 0.30);

        color: #ffffff !important;
        font-size: 12px;
        font-weight: 750;

        box-shadow:
            0 5px 18px rgba(79, 70, 229, 0.08);

        transition: all 0.2s ease;
    }

    .review2-heading {
        color: #ef4444 !important;
    }

    .sidebar-future {
        padding: 10px 13px;
        margin: 7px 0;
        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                rgba(239, 68, 68, 0.22),
                rgba(185, 28, 28, 0.12)
            );

        border: 1px solid rgba(248, 113, 113, 0.38);

        color: #fecaca !important;
        font-size: 11px;
        font-weight: 700;

        box-shadow:
            0 5px 18px rgba(239, 68, 68, 0.08);
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08);
        margin-top: 25px;
    }

    /* ========================================================
       TOP NAV
       ======================================================== */

    .top-nav {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(18px);

        border: 1px solid rgba(226, 232, 240, 0.90);
        border-radius: 18px;

        padding: 13px 20px;
        margin-bottom: 20px;

        box-shadow:
            0 8px 30px rgba(15, 23, 42, 0.06);
    }

    .top-logo {
        color: #111827;
        font-size: 22px;
        font-weight: 950;
        letter-spacing: -1px;
    }

    .top-badge {
        display: inline-block;

        margin-left: 10px;
        padding: 5px 10px;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #eef2ff,
                #f5f3ff
            );

        border: 1px solid #ddd6fe;

        color: #4f46e5;

        font-size: 9px;
        font-weight: 950;
        letter-spacing: .5px;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        background:
            radial-gradient(
                circle at 88% 25%,
                rgba(236, 72, 153, 0.40),
                transparent 22%
            ),
            radial-gradient(
                circle at 75% 90%,
                rgba(56, 189, 248, 0.25),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #090d2e 0%,
                #172554 48%,
                #4c1d95 100%
            );

        border-radius: 28px;

        padding: 48px 50px;

        color: white;

        margin-bottom: 26px;

        box-shadow:
            0 25px 65px rgba(49, 46, 129, 0.25);
    }

    .hero::after {
        content: "";
        position: absolute;

        width: 300px;
        height: 300px;

        right: -90px;
        top: -100px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(255, 255, 255, 0.12),
                transparent 65%
            );
    }

    .hero-badge {
        display: inline-block;

        padding: 7px 13px;

        border-radius: 999px;

        background: rgba(255, 255, 255, 0.12);

        border: 1px solid rgba(255, 255, 255, 0.18);

        color: #e0e7ff;

        font-size: 10px;
        font-weight: 900;

        letter-spacing: .8px;
    }

    .hero-title {
        font-size: clamp(42px, 5vw, 66px);

        line-height: .98;

        font-weight: 950;

        letter-spacing: -4px;

        margin-top: 20px;
    }

    .hero-title span {
        background:
            linear-gradient(
                90deg,
                #f9a8d4,
                #c4b5fd,
                #67e8f9
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        max-width: 760px;

        color: #dbeafe;

        font-size: 16px;
        line-height: 1.7;

        margin-top: 18px;
    }

    .hero-chip {
        display: inline-block;

        padding: 8px 12px;

        margin: 20px 7px 0 0;

        border-radius: 999px;

        background: rgba(255, 255, 255, 0.09);

        border: 1px solid rgba(255, 255, 255, 0.14);

        color: #f1f5f9;

        font-size: 10px;
        font-weight: 800;
    }

    /* ========================================================
       STREAMLIT HERO ELEMENTS
       ======================================================== */

    .stApp h1 {
        color: #172554;
        font-weight: 950;
        letter-spacing: -2px;
    }

    .stApp h2 {
        color: #1e293b;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .stApp h3 {
        color: #1e293b;
        font-weight: 850;
    }

    /* ========================================================
       INFO / FEATURE CARDS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
        border: 1px solid #dbeafe !important;

        background:
            linear-gradient(
                135deg,
                rgba(239, 246, 255, 0.95),
                rgba(238, 242, 255, 0.95)
            ) !important;

        box-shadow:
            0 7px 22px rgba(79, 70, 229, 0.06);

        color: #334155 !important;
    }

    /* ========================================================
       JOURNEY / METRICS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.82);

        border: 1px solid #e2e8f0;

        border-radius: 17px;

        padding: 16px 10px;

        box-shadow:
            0 7px 24px rgba(15, 23, 42, 0.045);

        transition: transform .2s ease,
                    box-shadow .2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        box-shadow:
            0 12px 30px rgba(79, 70, 229, 0.10);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 750;
    }

    div[data-testid="stMetricValue"] {
        color: #4338ca !important;
        font-weight: 950;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.90) !important;
        border: 1px solid #e2e8f0 !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #818cf8 !important;

        box-shadow:
            0 0 0 3px rgba(99, 102, 241, 0.10);
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;

        background: rgba(255, 255, 255, 0.90) !important;

        border-color: #e2e8f0 !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #818cf8 !important;
    }

    /* ========================================================
       RESUME UPLOADER
       ======================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        border-radius: 18px !important;

        border: 2px dashed #c4b5fd !important;

        background:
            linear-gradient(
                135deg,
                #fafaff,
                #f5f3ff
            ) !important;

        min-height: 125px;

        box-shadow:
            inset 0 0 30px rgba(99, 102, 241, 0.025);
    }

    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #818cf8 !important;

        background:
            linear-gradient(
                135deg,
                #f5f3ff,
                #eef2ff
            ) !important;
    }

    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    div.stButton > button {
        border-radius: 14px !important;

        min-height: 54px;

        font-weight: 900;

        font-size: 14px;

        border: none !important;

        transition:
            transform .2s ease,
            box-shadow .2s ease;
    }

    div.stButton > button[kind="primary"] {
        background:
            linear-gradient(
                90deg,
                #4f46e5 0%,
                #7c3aed 50%,
                #db2777 100%
            ) !important;

        color: white !important;

        box-shadow:
            0 10px 28px rgba(124, 58, 237, 0.24);
    }

    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);

        box-shadow:
            0 15px 34px rgba(124, 58, 237, 0.30);
    }

    /* ========================================================
       REVIEW-II WARNING CARDS
       ======================================================== */

    .future-card {
        background:
            linear-gradient(
                145deg,
                #fff1f2 0%,
                #fee2e2 100%
            );

        border: 1px solid #fca5a5;

        border-radius: 18px;

        padding: 20px;

        min-height: 175px;

        box-shadow:
            0 7px 24px rgba(127, 29, 29, 0.055);

        transition:
            transform .2s ease,
            box-shadow .2s ease;
    }

    .future-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 14px 30px rgba(127, 29, 29, 0.10);
    }

    .future-icon {
        font-size: 27px;
        margin-bottom: 9px;
    }

    .future-title {
        color: #991b1b;

        font-size: 15px;

        font-weight: 900;
    }

    .future-text {
        color: #7f1d1d;

        font-size: 11px;

        line-height: 1.55;

        margin-top: 6px;
    }

    .future-label {
        display: inline-block;

        margin-top: 12px;

        padding: 5px 9px;

        border-radius: 999px;

        background: #dc2626;

        color: #ffffff;

        font-size: 8px;

        font-weight: 950;

        letter-spacing: .6px;
    }

    /* ========================================================
       ROLE BANNER
       ======================================================== */

    .role-banner {
        background:
            linear-gradient(
                90deg,
                #eef2ff,
                #f5f3ff,
                #fdf4ff
            );

        border: 1px solid #ddd6fe;

        border-radius: 16px;

        padding: 16px 18px;

        color: #4338ca;

        margin: 15px 0;
    }

    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    div[data-testid="stProgress"] > div {
        background: #e0e7ff;
        border-radius: 999px;
    }

    div[data-testid="stProgress"] > div > div {
        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed,
                #ec4899
            );

        border-radius: 999px;
    }

    /* ========================================================
       SKILL PANELS
       ======================================================== */

    .skill-panel {
        background: rgba(255, 255, 255, 0.90);

        border: 1px solid #e2e8f0;

        border-radius: 18px;

        padding: 20px;

        min-height: 180px;

        box-shadow:
            0 7px 24px rgba(15, 23, 42, 0.04);
    }

    .skill-heading {
        color: #0f172a;

        font-size: 15px;

        font-weight: 900;

        margin-bottom: 12px;
    }

    .skill {
        display: inline-block;

        padding: 7px 10px;

        border-radius: 999px;

        margin: 3px;

        font-size: 10px;

        font-weight: 750;
    }

    .skill-green {
        background: #ecfdf5;

        color: #047857;

        border: 1px solid #a7f3d0;
    }

    .skill-red {
        background: #fff1f2;

        color: #be123c;

        border: 1px solid #fecdd3;
    }

    /* ========================================================
       RESOURCE CARDS
       ======================================================== */

    .resource-card {
        background: rgba(255, 255, 255, 0.92);

        border: 1px solid #e2e8f0;

        border-radius: 16px;

        padding: 18px;

        margin-bottom: 11px;

        box-shadow:
            0 6px 20px rgba(15, 23, 42, 0.035);
    }

    .resource-skill {
        color: #6366f1;

        font-size: 9px;

        font-weight: 950;

        letter-spacing: .8px;
    }

    .resource-title {
        color: #0f172a;

        font-size: 15px;

        font-weight: 850;

        margin-top: 5px;
    }

    /* ========================================================
       REVIEW NOTE
       ======================================================== */

    .review-note {
        background:
            linear-gradient(
                135deg,
                #fffbeb,
                #fff7ed
            );

        border: 1px solid #fde68a;

        border-radius: 14px;

        padding: 13px 15px;

        color: #92400e;

        font-size: 11px;

        line-height: 1.55;

        margin: 15px 0;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 10px;

        margin-top: 55px;

        padding-top: 22px;

        border-top: 1px solid #e2e8f0;
    }

    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">🎯 PLACIFY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Career Intelligence Platform'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-heading">Working in Review-I</div>',
        unsafe_allow_html=True,
    )

    current_items = [
        "👤 Career Profile",
        "📄 Resume Analysis",
        "🧠 ESCO Skill Intelligence",
        "🎯 Target Role Analysis",
        "📚 Learning Recommendations",
    ]

    for item in current_items:

        st.markdown(
            f'<div class="sidebar-active">✓ &nbsp; {item}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sidebar-heading review2-heading">REVIEW-II</div>',
        unsafe_allow_html=True,
    )

    future_items = [
        "🌐 Multi-Domain Careers",
        "📋 Job Description Intelligence",
        "🧠 Advanced Skill Matching",
        "📝 Technical Assessment",
        "🧮 Aptitude Assessment",
        "🎤 Interview Preparation",
        "📅 Personalized Study Plan",
        "📈 Progress Tracking",
        "🎯 Placement Readiness",
        "📊 Career Dashboard",
    ]

    for item in future_items:

        st.markdown(
            f'<div class="sidebar-future">🔴 {item}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.caption(
        "Review-I Working Prototype"
    )

# ============================================================
# TOP NAV
# ============================================================

st.html(
    """
    <div class="top-nav">
        <span class="top-logo">🎯 Placify</span>
        <span class="top-badge">REVIEW-I • WORKING PROTOTYPE</span>
    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div style="
        background: linear-gradient(135deg, #111827, #312e81, #7c3aed);
        padding: 42px;
        border-radius: 28px;
        margin-bottom: 28px;
        color: white;
        box-shadow: 0 20px 50px rgba(79, 70, 229, 0.25);
    ">
        <div style="
            display: inline-block;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.22);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1px;
        ">
            ✦ AI-DRIVEN CAREER INTELLIGENCE
        </div>

        <div style="
            font-size: 48px;
            font-weight: 900;
            line-height: 1.05;
            margin-top: 20px;
            letter-spacing: -2px;
        ">
            Your career.
        </div>

        <div style="
            font-size: 48px;
            font-weight: 900;
            line-height: 1.05;
            margin-top: 4px;
            color: #c4b5fd;
            letter-spacing: -2px;
        ">
            More intentional.
        </div>

        <div style="
            max-width: 760px;
            margin-top: 18px;
            color: #e0e7ff;
            font-size: 15px;
            line-height: 1.7;
        ">
            Turn your resume into actionable career intelligence.
            Understand your strengths, discover the skills you
            need for your target role, and find what to learn next.
        </div>

        <div style="margin-top: 22px;">
            <span style="
                display: inline-block;
                padding: 9px 13px;
                margin-right: 7px;
                border-radius: 999px;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.16);
                font-size: 11px;
                font-weight: 700;
            ">
                📄 Resume Intelligence
            </span>

            <span style="
                display: inline-block;
                padding: 9px 13px;
                margin-right: 7px;
                border-radius: 999px;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.16);
                font-size: 11px;
                font-weight: 700;
            ">
                🧠 ESCO Skill Mapping
            </span>

            <span style="
                display: inline-block;
                padding: 9px 13px;
                margin-right: 7px;
                border-radius: 999px;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.16);
                font-size: 11px;
                font-weight: 700;
            ">
                🎯 Career Matching
            </span>

            <span style="
                display: inline-block;
                padding: 9px 13px;
                border-radius: 999px;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.16);
                font-size: 11px;
                font-weight: 700;
            ">
                📚 Learning Guidance
            </span>
        </div>
    </div>
    """
)

# ============================================================
# CAREER JOURNEY
# ============================================================

st.subheader("Your Placify Journey")

journey_cols = st.columns(6)

journey_steps = [
    ("01", "👤", "Profile"),
    ("02", "📄", "Resume"),
    ("03", "🧠", "Skills"),
    ("04", "🎯", "Target Role"),
    ("05", "🔍", "Skill Gaps"),
    ("06", "📚", "Learn"),
]

for column, (number, icon, title) in zip(
    journey_cols,
    journey_steps,
):
    with column:

        st.html(
            f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 18px 8px;
                text-align: center;
                min-height: 105px;
                box-shadow: 0 8px 24px rgba(15,23,42,0.06);
            ">
                <div style="
                    font-size: 24px;
                    margin-bottom: 6px;
                ">
                    {icon}
                </div>

                <div style="
                    color: #475569;
                    font-size: 11px;
                    font-weight: 800;
                ">
                    {title}
                </div>

                <div style="
                    color: #4f46e5;
                    font-size: 25px;
                    font-weight: 900;
                    margin-top: 4px;
                ">
                    {number}
                </div>
            </div>
            """
        )


# ============================================================
# PROFILE
# ============================================================

st.header("👤 Build your career profile")

st.write(
    "Start with the basics. Your profile becomes the foundation "
    "of your Placify career journey."
)

profile_col1, profile_col2 = st.columns(2)

with profile_col1:

    student_name = st.text_input(
        "Full Name",
        placeholder="e.g. XYZ",
    )

with profile_col2:

    education = st.text_input(
        "Education",
        placeholder="e.g. B.E. Electronics & Communication Engineering",
    )


# ============================================================
# FUTURE CAREER DOMAINS
# ============================================================

st.header("🌐 Explore your career domain")

st.write(
    "Placify is designed to expand across multiple academic and "
    "professional domains."
)

domain_cols = st.columns(4)

future_domains = [
    (
        "⚙️",
        "Engineering & Technology",
        "Technical careers, engineering roles and placement preparation.",
    ),
    (
        "🏨",
        "Hotel Management",
        "Hospitality careers, service skills and role preparation.",
    ),
    (
        "💼",
        "Business & Management",
        "Business, finance, operations and management pathways.",
    ),
    (
        "🎨",
        "Design & Creative",
        "Design, media, creative technology and portfolio careers.",
    ),
]

for col, (icon, title, description) in zip(
    domain_cols,
    future_domains,
):
    with col:

        st.html(
            f"""
            <div style="
                background: linear-gradient(145deg, #fff1f2, #fee2e2);
                border: 1px solid #fca5a5;
                border-radius: 18px;
                padding: 20px;
                min-height: 185px;
                box-shadow: 0 8px 25px rgba(185,28,28,0.08);
            ">
                <div style="
                    font-size: 28px;
                    margin-bottom: 10px;
                ">
                    {icon}
                </div>

                <div style="
                    color: #991b1b;
                    font-size: 15px;
                    font-weight: 900;
                ">
                    {title}
                </div>

                <div style="
                    color: #7f1d1d;
                    font-size: 11px;
                    line-height: 1.55;
                    margin-top: 7px;
                ">
                    {description}
                </div>

                <div style="
                    display: inline-block;
                    margin-top: 14px;
                    padding: 5px 9px;
                    border-radius: 999px;
                    background: #dc2626;
                    color: white;
                    font-size: 8px;
                    font-weight: 900;
                    letter-spacing: .6px;
                ">
                    🔴 UPCOMING
                </div>
            """
        )


# ============================================================
# RESUME
# ============================================================

st.header("📄 Upload your resume")

st.write(
    "Upload your PDF resume and let Placify understand your "
    "experience, skills and career profile."
)

uploaded_file = st.file_uploader(
    "Upload your PDF resume",
    type=["pdf"],
    label_visibility="collapsed",
)


resume_text = ""


if uploaded_file:

    temp_resume_path = BASE_DIR / "temp_resume.pdf"

    try:

        with open(temp_resume_path, "wb") as file:
            file.write(
                uploaded_file.getbuffer()
            )

        resume_text = extract_text_from_pdf(
            str(temp_resume_path)
        )

        st.success(
            f"✓ Resume ready — {uploaded_file.name}"
        )

    except Exception as error:

        st.error(
            f"Resume processing failed: {error}"
        )


# ============================================================
# TARGET ROLE
# ============================================================

st.header("🎯 Select a role you want to ace")

st.write(
    "Choose the role you’re targeting."
)

try:

    roles = get_job_roles()

    role_names = [
        role[1]
        for role in roles
    ]

    selected_role_name = st.selectbox(
        "Roles",
        role_names,
        index=None,
        placeholder="Select a role",
    )

    selected_role = None

    if selected_role_name:

        selected_role = next(
            role
            for role in roles
            if role[1] == selected_role_name
        )

except Exception as error:

    st.error(
        f"Unable to load roles: {error}"
    )

    selected_role = None


# ============================================================
# ANALYZE
# ============================================================

st.markdown("")

analyze = st.button(
    "✨ Generate My Career Intelligence",
    type="primary",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    # PROFILE VALIDATION

    if not student_name.strip() and not education.strip():

        st.warning(
            "Please enter your full name and education before continuing."
        )

        st.stop()

    if not student_name.strip():

        st.warning(
            "Please enter your full name before continuing."
        )

        st.stop()

    if not education.strip():

        st.warning(
            "Please enter your education before continuing."
        )

        st.stop()


    # RESUME VALIDATION

    if uploaded_file is None:

        st.warning(
            "Please upload your resume before continuing."
        )

        st.stop()

    if not resume_text.strip():

        st.warning(
            "No readable text was found in the uploaded resume."
        )

        st.stop()


    # ROLE VALIDATION

    if selected_role is None:

        st.warning(
            "Please select a role you want to ace."
        )

        st.stop()


    with st.spinner(
        "✨ Building your career intelligence..."
    ):

        resume_skills = extract_skills(
            resume_text
        )

        required_skills = get_role_skills(
            selected_role[0]
        )

        analysis = calculate_skill_gap(
            resume_skills,
            required_skills,
        )

        recommendations = recommend_resources(
            analysis["missing"],
            limit=5,
        )


    # ========================================================
    # RESULT HEADER
    # ========================================================

    st.markdown("---")

    st.header("✨ Your Career Intelligence")

    st.info(
        f"🎯 Targeting: {selected_role_name}"
    )


    # ========================================================
    # METRICS
    # ========================================================

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="Skill Coverage",
            value=f'{analysis["match_percentage"]}%'
        )

    with c2:
        st.metric(
            label="Skills Detected",
            value=len(resume_skills)
        )

    with c3:
        st.metric(
            label="Skills Matched",
            value=len(analysis["matched"])
        )

    with c4:
        st.metric(
            label="Skill Gaps",
            value=len(analysis["missing"])
        )

    # ========================================================
    # SKILL COVERAGE
    # ========================================================

    st.write(
        "How closely your current resume aligns with the "
        "selected target role."
    )

    st.progress(
        min(
            analysis["match_percentage"] / 100,
            1.0,
        )
    )


    # ========================================================
    # SKILLS
    # ========================================================

    st.header("🧠 Your Skill Intelligence")

    left, right = st.columns(2)


    # MATCHED
    with left:

        st.subheader("🟢 Skills you already have")

        if analysis["matched"]:

            for skill in analysis["matched"]:

                st.success(
                    f'✓ {skill["skill_name"]}'
                )

            st.markdown("")

        else:

            st.info(
                "No matching skills identified yet."
            )


    # GAPS
    with right:

        st.subheader("🔴 Skills to develop")

        if analysis["missing"]:

            for skill in analysis["missing"][:20]:

                st.warning(
                    f'+ {skill["skill_name"]}'
                )

            st.markdown("")

        else:

            st.success(
                "Excellent! No identified skill gaps."
            )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.header("📚 Your next steps")

    st.write(
        "Placify connects identified skill gaps with relevant "
        "learning resources to help you decide what to learn next."
    )


    if recommendations:

        for recommendation in recommendations:

            skill = recommendation["skill"]
            resource = recommendation["resource"]

            resource_title = None

            for key, value in resource.items():

                if (
                    "title" in key.lower()
                    or "course" in key.lower()
                    or "name" in key.lower()
                ):

                    if value and str(value) != "nan":

                        resource_title = str(value)
                        break

            if not resource_title:

                resource_title = (
                    "Recommended learning resource"
                )


            st.info(
                f"🎓 {resource_title}\n\n"
                f"Recommended for: {skill}"
            )

    else:

        st.info(
            "No matching resources were found for "
            "the current skill gaps."
        )


    # ========================================================
    # REVIEW-II ROADMAP
    # ========================================================

    st.markdown("---")

    st.header("🚀 What Placify will become")

    st.write(
        "The following capabilities represent the planned expansion "
        "of Placify beyond the Review-I working prototype."
    )

    future_modules = [

        (
            "🌐",
            "Multi-Domain Career Intelligence",
            "Expand career guidance across Engineering, Hotel Management, "
            "Business, Design and additional domains.",
        ),

        (
            "📋",
            "Job Description Intelligence",
            "Analyze job descriptions and identify employer requirements.",
        ),

        (
            "🧠",
            "Advanced Skill Matching",
            "Improve skill normalization and semantic matching.",
        ),

        (
            "📝",
            "Technical Assessment",
            "Role-specific technical questions, scoring and performance analysis.",
        ),

        (
            "🧮",
            "Aptitude Assessment",
            "Quantitative, logical, verbal and technical aptitude evaluation.",
        ),

        (
            "🎤",
            "Interview Preparation",
            "Personalized technical and HR interview preparation.",
        ),

        (
            "📅",
            "Personalized Study Plan",
            "Convert skill gaps into a structured learning roadmap.",
        ),

        (
            "📈",
            "Progress Tracking",
            "Track learning and assessment progress over time.",
        ),

        (
            "🎯",
            "Placement Readiness",
            "Generate a future readiness indicator from multiple signals.",
        ),

        (
            "📊",
            "Career Dashboard",
            "Bring profile, skills, learning and readiness into one dashboard.",
        ),


    ]

    future_cols = st.columns(3)

    for index, (icon, title, description) in enumerate(
        future_modules
    ):

        with future_cols[index % 3]:

            st.html(
                f"""
                <div class="future-card">

                    <div class="future-icon">
                        {icon}
                    </div>

                    <div class="future-title">
                        {title}
                    </div>

                    <div class="future-text">
                        {description}
                    </div>

                    <div class="future-label">
                        🔴 REVIEW-II • UPCOMING
                    </div>

                </div>
                """
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎯 PLACIFY · AI-Driven Career Intelligence"
)

st.caption(
    "Review-I Working Prototype"
)

st.caption(
    "Resume Intelligence · ESCO Skill Mapping · Career Analysis"
)

st.caption(
    "🔴 Additional career, assessment, learning and tracking "
    "capabilities are planned for subsequent development phases."
)