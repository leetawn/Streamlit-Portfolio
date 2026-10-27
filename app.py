"""
================================================================================
Autobiography and Portfolio - Streamlit Application
Course: CSIT 349 Applied AI
Style: Professional Engineering Portfolio
================================================================================
A personal website and academic portfolio built with Streamlit.
All editable student facts and placeholders are centralized in the DATA SECTION
below to make customization simple and direct.
================================================================================
"""

import os
import json
import random
import datetime
import pandas as pd
import numpy as np
import streamlit as st

# ==============================================================================
# 1. DATA SECTION (EDIT YOUR PERSONAL DETAILS & FACTS HERE)
# ==============================================================================
# All personal text and details are populated below.
# ==============================================================================

PERSONAL_INFO = {
    "name": "Ethan Benedict Labajo",
    "course": "CSIT 349 Applied AI",
    "section": "BSCS-3 F1",
    "program_and_year": "BS Computer Science 3rd Year",
    "school": "Cebu Institute of Technology - University",
    "tagline": "Larping my way through CS",
    "location": "Cebu City, Philippines",
    "short_bio": (
        "I am an aspiring IT professional with a strong foundation in software development, database management, and web technologies. My academic journey has equipped me with practical skills in Python, SQL, and full-stack development, complemented by hands-on experience in data analysis and machine learning. I am passionate about building scalable, user-centered applications that solve real-world problems and continuously seek to expand my technical expertise in artificial intelligence and emerging technologies."
    ),
    "contact_email": "ethan.labajo@cit.edu",
    "github_url": "https://github.com/leetawn",
    "leetcode_url": "https://leetcode.com/u/etawn",
    "goals": (
        "Develop scalable, responsive generative AI interfaces, master practical model evaluation and telemetry pipelines, "
        "and implement responsible, human-centered AI systems in real-world software engineering workflows."
    ),
}

AUTOBIOGRAPHY_DATA = {
    "background": (
        "I initially didn't plan to become a Computer Science student at all. I dreamt of being a scientist or an astronomer. However, everything changed during the pandemic when I got introduced to a JavaScript framework called p5.js. The idea of being able to create anything that you wish through code just intrigued me so much it wanted me to pursue Computer Science."
    ),
    "education": (
        """
            I am currently enrolled as a BS Computer Science student in my third year at Cebu Institute of Technology - University. 
            I've always had a knack for math and problem-solving, which led me to explore programming during the pandemic. 
            What started as a hobby quickly evolved into a passion, and I've since delved into various aspects of computer science, 
            including software development, database management, and machine learning. I'm particularly interested in AI and its applications, 
            and I'm excited to continue learning and growing in this field.
        """
    ),
    "interests": (
        "I have a deep interest in Competitive Programming and problem solving in general. As for non-technical stuff, I love playing the electric guitar and used to speedcube (although I'm quite washed)."
    ),
    "milestones": [
        {
            "Year": "2020",
            "Milestone": "My First Ever Hello World!",
            "Category": "Personal"
        },
        {
            "Year": "2024",
            "Milestone": "Managed to survive Sir Serato's DSA and DAA classes. Also managed to implement Dijkstra from scratch, allowing me to pass the laboratory exam!",
            "Category": "Academic"
        },
        {
            "Year": "2025",
            "Milestone": "Hit 1500 questions solved on LeetCode.",
            "Category": "Programming"
        },
    ],
    "fun_facts": [
        "I currently have 1714 problems solved on LeetCode and counting...",
        "I ranked 6th in a Cebu Speedcubing Competition. My best time for 3x3 is 9 seconds!",
        "I am quite decent at guitar. I love Jazz Fusion so I try to study music theory to play jazz fusion, but I just can't seem to improvise a solo for it properly.",
    ]
}

# Skill ratings (0-100) calibrated to personal competency levels.
SKILLS_DATA = [
    {
        "Skill": "Python",
        "Category": "Programming Languages",
        "Level": 95,
        "Description": "I can write Python code for competitive programming, machine learning, data science, and more."
    },
    {
        "Skill": "SQL & Relational DBs",
        "Category": "Programming Languages",
        "Level": 68,
        "Description": "I can write SQL queries, design relational databases, and optimize them for performance."
    },
    {
        "Skill": "JavaScript / Web Basics",
        "Category": "Programming Languages",
        "Level": 75,
        "Description": "I used to spend so much time on p5.js (a JavaScript framework). Other than that framework, I know basic HTML, CSS, and JS."
    },
    {
        "Skill": "Machine Learning",
        "Category": "AI & Data Science",
        "Level": 85,
        "Description": "I wrote a feedforward neural network from scratch in C. I had to write everything including matrix operations, activation functions, and backpropagation."
    },
    {
        "Skill": "Data Analysis",
        "Category": "AI & Data Science",
        "Level": 75,
        "Description": "We've recently done data science and analysis on this course. I have experience on classification and k-means clustering on datasets like the spotify tracks dataset."
    },
    {
        "Skill": "Git & Collaborative GitHub",
        "Category": "Frameworks & Tools",
        "Level": 70,
        "Description": "I know the basics, but not the other collaborative commands because I don't get to collaborate with other people much other than during school projects."
    },
]

# At least three projects, each with title, role, tools, summary, and outcome or link.
PROJECTS_DATA = [
    {
        "id": "proj_1",
        "title": "Feedforward Neural Network in C",
        "role": "Everything",
        "tools": ["C"],
        "summary": "I wrote a feedforward neural network from scratch in C. I had to write everything including matrix operations, activation functions, and backpropagation.",
        "outcome": "It just made me more confused as to how AI like Claude and ChatGPT works. It doesn't occur to me that a bunch of random numbers and tweaking those numbers a bit can result into something so powerful.",
        "link": "https://github.com/leetawn/feedforward-nn-sgd", 
        "featured": True
    },
    {
        "id": "proj_2",
        "title": "MIRE Protocol Zero",
        "role": "Networking and Multiplayer, Game Mechanics",
        "tools": ["Godot", "GDScript"],
        "summary": "MIRE Protocol Zero is a 2D multiplayer game we created for the DOST Game Jam. We unfortunately did not win, but a lot of people enjoyed playing our game during the showcase!",
        "outcome": "Made me realize how important code architecture and structure is depending on the project being made. For our game, we prioritized components over inheritance!",
        "link": "https://github.com/leetawn/MIRE-Protocol-Zero",
        "featured": True
    },
    {
        "id": "proj_3",
        "title": "CodeChum++",
        "role": "Backend Logic, File Management System",
        "tools": ["Java", "Java Swing"],
        "summary": "CodeChum++ is our OOP1 Capstone Project. It is basically an offline version of CodeChum which allows for problem sharing among students.",
        "outcome": "Made me learn how tedious creating a File Management System is.",
        "link": "https://github.com/leetawn/CodeChum-plus-plus",
        "featured": True
    }
]


# ==============================================================================
# 2. HELPER FUNCTIONS & ASSET MANAGEMENT
# ==============================================================================

def get_or_create_photo(photo_path: str = "assets/photo.png") -> str:
    """
    Returns path to photo.png. If missing, generates a clearly labeled
    'STAND-IN PHOTO' placeholder image with Pillow.
    """
    if os.path.exists(photo_path):
        return photo_path
    
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (400, 400), color=(17, 24, 39))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 390, 390], outline=(55, 65, 81), width=2)
        draw.rectangle([16, 16, 384, 384], outline=(31, 41, 55), width=1)
        draw.ellipse([130, 80, 270, 220], fill=(31, 41, 55), outline=(55, 65, 81), width=2)
        draw.ellipse([80, 250, 320, 430], fill=(31, 41, 55), outline=(55, 65, 81), width=2)
        draw.line([(100, 290), (300, 290)], fill=(56, 189, 248), width=2)
        draw.rectangle([60, 305, 340, 345], fill=(31, 41, 55), outline=(56, 189, 248), width=1)
        draw.text((115, 317), "STAND-IN PHOTO", fill=(243, 244, 246))
        draw.text((125, 360), "PROFILE PLACEHOLDER", fill=(156, 163, 175))
        img.save(photo_path, "PNG")
        return photo_path
    except Exception:
        return photo_path


def init_session_state() -> None:
    """Initializes all necessary session_state values if not present."""
    if "project_likes" not in st.session_state:
        st.session_state.project_likes = {p["id"]: 0 for p in PROJECTS_DATA}
    if "liked_projects" not in st.session_state:
        st.session_state.liked_projects = set()
    if "feedback_messages" not in st.session_state:
        st.session_state.feedback_messages = []
    if "current_fun_fact_idx" not in st.session_state:
        st.session_state.current_fun_fact_idx = 0


# ==============================================================================
# 3. PAGE CONFIGURATION & SLEEK CODING DESIGN SYSTEM
# ==============================================================================

st.set_page_config(
    page_title="Autobiography and Portfolio | CSIT 349 Applied AI",
    page_icon="assets/photo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()
photo_file = get_or_create_photo("assets/photo.png")

# ── Sleek IDE Coding Theme CSS ────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* ── Local JetBrains Mono Font Declarations ──────────────── */
    @font-face {
        font-family: 'JetBrains Mono';
        src: url('/app/static/fonts/JetBrainsMono-Regular.woff2') format('woff2');
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'JetBrains Mono';
        src: url('/app/static/fonts/JetBrainsMono-Medium.woff2') format('woff2');
        font-weight: 500;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'JetBrains Mono';
        src: url('/app/static/fonts/JetBrainsMono-SemiBold.woff2') format('woff2');
        font-weight: 600;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'JetBrains Mono';
        src: url('/app/static/fonts/JetBrainsMono-Bold.woff2') format('woff2');
        font-weight: 700;
        font-style: normal;
        font-display: swap;
    }

    /* ── Base Theme & Canvas ─────────────────────────────────── */
    :root {
        --bg-canvas: #090C10;
        --bg-surface: #0E131F;
        --bg-surface-elevated: #141B2B;
        --border-subtle: #1E2738;
        --border-highlight: #2D3B54;
        --text-primary: #E6EDF3;
        --text-secondary: #8B949E;
        --text-muted: #57606A;
        --accent-violet: #818CF8;
        --accent-cyan: #38BDF8;
        --accent-emerald: #34D399;
        --accent-amber: #FBBF24;
    }

    /* Target background canvas */
    .stApp {
        background-color: #090C10 !important;
        background-image: 
            radial-gradient(rgba(30, 41, 59, 0.45) 1px, transparent 1px),
            linear-gradient(180deg, #090C10 0%, #0D111A 100%) !important;
        background-size: 24px 24px, 100% 100% !important;
        background-attachment: fixed !important;
        color: #E6EDF3 !important;
        font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', Consolas, monospace !important;
    }

    /* Streamlit top chrome cleanup */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    #MainMenu, footer { visibility: hidden !important; }

    /* ── Universal JetBrains Mono Typography ─────────────────── */
    *, html, body, .stApp, 
    [class*="css"], [class*="st-"], [class*="st"],
    h1, h2, h3, h4, h5, h6,
    p, span, label, li, a, em, strong,
    input, textarea, select, button,
    table, th, td, tr, caption,
    code, pre, kbd, samp,
    [data-testid], [data-baseweb],
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stMetricDelta"],
    [data-baseweb="tab"], [data-baseweb="tab-panel"],
    [data-testid="stSidebar"], [data-testid="stSidebar"] *,
    [data-testid="stWidgetLabel"], .stSlider label, .stRadio label,
    .sidebar-user-name, .sidebar-meta-row, .terminal-hero-title, .terminal-tagline {
        font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', Consolas, monospace !important;
    }

    h1 {
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        line-height: 1.25 !important;
        margin-bottom: 0.25rem !important;
        letter-spacing: -0.02em !important;
    }

    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #818CF8 !important;
        border-bottom: 1px solid #1E2738 !important;
        padding-bottom: 0.5rem !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.85rem !important;
        letter-spacing: -0.02em !important;
    }

    h3 {
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        color: #38BDF8 !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.01em !important;
    }

    p, .stMarkdown p, li, .stMarkdown li {
        color: #CBD5E1;
        font-size: 0.90rem;
        line-height: 1.68;
        letter-spacing: -0.01em;
    }

    /* ── Terminal Window Header Banner ───────────────────────── */
    .terminal-window {
        background: #0E131F;
        border: 1px solid #1E2738;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 24px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
    }

    .terminal-topbar {
        background: #0B0E17;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #1E2738;
    }

    .terminal-controls {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .t-dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        display: inline-block;
    }
    .t-dot-red    { background: #FF5F56; }
    .t-dot-yellow { background: #FFBD2E; }
    .t-dot-green  { background: #27C93F; }

    .terminal-path {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: #8B949E;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .terminal-branch {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #818CF8;
        background: rgba(129, 140, 248, 0.12);
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid rgba(129, 140, 248, 0.3);
    }

    .terminal-content {
        padding: 20px 24px;
    }

    .terminal-hero-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0 0 6px 0;
    }

    .terminal-tagline {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #94A3B8;
        font-style: italic;
        margin-bottom: 14px;
        line-height: 1.5;
    }

    .terminal-meta-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        padding-top: 12px;
        border-top: 1px solid #1E2738;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }

    .t-meta-item {
        color: #64748B;
    }
    .t-meta-item strong {
        color: #E2E8F0;
        font-weight: 600;
    }

    /* ── Metric Cards ────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: #0E131F !important;
        border: 1px solid #1E2738 !important;
        border-top: 2px solid #818CF8 !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        transition: transform 0.15s ease, border-color 0.15s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: #2D3B54 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        color: #8B949E !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        color: #38BDF8 !important;
    }

    /* ── VS Code Style Tabs ──────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: #0B0E17 !important;
        border: 1px solid #1E2738 !important;
        border-radius: 8px 8px 0 0 !important;
        gap: 0px !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #64748B !important;
        padding: 10px 22px !important;
        background: transparent !important;
        border-right: 1px solid #1E2738 !important;
        border-bottom: 2px solid transparent !important;
        border-top: 2px solid transparent !important;
        transition: all 0.15s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #E2E8F0 !important;
        background: #0E131F !important;
    }
    .stTabs [aria-selected="true"] {
        color: #818CF8 !important;
        background: #0E131F !important;
        border-bottom-color: #818CF8 !important;
        border-top-color: #818CF8 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: #0E131F !important;
        border: 1px solid #1E2738 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 24px !important;
    }

    /* ── Project & Bordered Cards ────────────────────────────── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #0E131F !important;
        border: 1px solid #1E2738 !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #2D3B54 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    }

    /* ── Technology Badges / Pills ───────────────────────────── */
    .tech-pill {
        display: inline-block;
        padding: 2px 9px;
        margin: 3px 5px 3px 0;
        font-size: 0.74rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 4px;
        letter-spacing: 0.02em;
    }
    .status-pill-green {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #34D399;
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 12px;
        padding: 2px 10px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* ── Buttons ─────────────────────────────────────────────── */
    .stButton > button, .stDownloadButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        background: #141B2B !important;
        color: #CBD5E1 !important;
        border: 1px solid #1E2738 !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: rgba(129, 140, 248, 0.12) !important;
        color: #818CF8 !important;
        border-color: #818CF8 !important;
    }
    [data-testid="stLinkButton"] > a {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        background: #141B2B !important;
        color: #38BDF8 !important;
        border: 1px solid #1E2738 !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stLinkButton"] > a:hover {
        background: rgba(56, 189, 248, 0.12) !important;
        color: #FFFFFF !important;
        border-color: #38BDF8 !important;
    }

    /* ── Form Inputs ─────────────────────────────────────────── */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        background: #0B0E17 !important;
        border: 1px solid #1E2738 !important;
        border-radius: 6px !important;
        color: #F8FAFC !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }

    /* ── Sidebar Component ───────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #0B0E17 !important;
        border-right: 1px solid #1E2738 !important;
    }
    .sidebar-profile-card {
        background: #0E131F;
        border: 1px solid #1E2738;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 16px;
    }
    .sidebar-user-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.08rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 8px 0 2px 0;
    }
    .sidebar-meta-row {
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        color: #57606A;
        margin-top: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid #141B2B;
        line-height: 1.5;
    }
    .sidebar-meta-row strong {
        display: block;
        color: #CBD5E1;
        font-size: 0.78rem;
        margin-top: 1px;
        word-break: break-word;
    }
    .sidebar-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin: 14px 0 6px 0;
    }
    .dev-profile-links-grid {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin: 6px 0 16px 0;
    }
    .dev-profile-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        background: #141B2B;
        border: 1px solid #1E2738;
        border-radius: 6px;
        padding: 8px 10px;
        color: #CBD5E1 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.76rem !important;
        font-weight: 500;
        text-decoration: none !important;
        transition: all 0.15s ease;
    }
    .dev-profile-btn:hover {
        background: #1A2338;
        border-color: #818CF8;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }
    .dev-profile-btn.leetcode-btn:hover {
        border-color: #FFA116;
        color: #FFA116 !important;
        background: rgba(255, 161, 22, 0.08);
    }
    .dev-profile-btn svg {
        flex-shrink: 0;
    }

    /* ── Tables & DataFrames ─────────────────────────────────── */
    table, [data-testid="stTable"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
        border: 1px solid #1E2738 !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }
    th {
        background-color: #141B2B !important;
        color: #818CF8 !important;
        font-weight: 600 !important;
        border: 1px solid #1E2738 !important;
        padding: 8px 12px !important;
    }
    td {
        border: 1px solid #1E2738 !important;
        padding: 8px 12px !important;
        color: #CBD5E1 !important;
    }

    /* ── Competency Matrix (st.dataframe): use Inter for readability ── */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] *,
    [data-testid="stDataFrame"] canvas,
    [data-testid="stDataFrameGlideDataEditor"],
    [data-testid="stDataFrameGlideDataEditor"] * {
        font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        font-size: 0.83rem !important;
        letter-spacing: 0 !important;
    }

    /* ── Global Material Symbols: restore icons across expanders, sidebar, alerts ── */
    [data-testid="stIconMaterial"],
    [data-testid*="Icon"],
    [data-testid="stExpanderToggleIcon"],
    [data-testid="stExpander"] [data-testid="stIconMaterial"],
    summary [data-testid="stIconMaterial"],
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
        font-feature-settings: 'liga' 1 !important;
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
        display: inline-block !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        vertical-align: middle !important;
    }

    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
    [data-testid*="Sidebar"] button [data-testid="stIconMaterial"] {
        font-size: 1.3rem !important;
        color: #8B949E !important;
    }

    /* ── Expander Component Layout & Spacing ──────────────────── */
    [data-testid="stExpander"] {
        background: #0E131F !important;
        border: 1px solid #1E2738 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"] summary {
        font-family: 'JetBrains Mono', monospace !important;
        background: #0E131F !important;
        color: #CBD5E1 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        gap: 10px !important;
        transition: background 0.15s ease, color 0.15s ease !important;
    }
    [data-testid="stExpander"] summary:hover {
        background: #141B2B !important;
        color: #818CF8 !important;
    }
    [data-testid="stExpander"] summary [data-testid="stIconMaterial"] {
        color: #818CF8 !important;
        font-size: 1.25rem !important;
        margin-right: 8px !important;
    }
    [data-testid="stExpanderDetails"] {
        border-top: 1px solid #1E2738 !important;
        padding: 14px 16px !important;
    }

    /* ── Multiselect: prevent tags from being clipped ────────── */
    .stMultiSelect [data-baseweb="select"] {
        flex-wrap: wrap !important;
        min-height: 42px !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        margin: 2px !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    .stMultiSelect {
        overflow: visible !important;
    }

    /* ── Progress Bar ────────────────────────────────────────── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #818CF8, #38BDF8) !important;
    }
    .stProgress > div > div {
        background: #141B2B !important;
    }

    /* ── Scrollbars ──────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #090C10; }
    ::-webkit-scrollbar-thumb { background: #1E2738; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2D3B54; }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================================================================
# 4. SIDEBAR COMPONENT (CLEAN DEVELOPER PROFILE)
# ==============================================================================

with st.sidebar:


    # Developer Identity Card
    st.markdown(
        f"""
        <div class="sidebar-profile-card">
            <div class="sidebar-user-name">{PERSONAL_INFO['name']}</div>
            <div style="color: #818CF8; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; margin: 4px 0 10px 0;">
                {PERSONAL_INFO['course']} &bull; {PERSONAL_INFO['section']}
            </div>
            <div class="sidebar-meta-row">
                Program
                <strong>{PERSONAL_INFO['program_and_year']}</strong>
            </div>
            <div class="sidebar-meta-row">
                Institution
                <strong>{PERSONAL_INFO['school']}</strong>
            </div>
            <div class="sidebar-meta-row" style="border-bottom: none; padding-bottom: 0;">
                Location
                <strong>{PERSONAL_INFO['location']}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-label">Developer Profiles</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="dev-profile-links-grid">
            <a href="{PERSONAL_INFO['github_url']}" target="_blank" class="dev-profile-btn" title="GitHub Profile">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                <span>GitHub</span>
            </a>
            <a href="{PERSONAL_INFO.get('leetcode_url', 'https://leetcode.com')}" target="_blank" class="dev-profile-btn leetcode-btn" title="LeetCode Profile">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
                    <path fill="#FFA116" d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.116 6.226l-3.854 4.126a5.266 5.266 0 0 0-1.209 2.104 5.35 5.35 0 0 0-.125.513 5.527 5.527 0 0 0 .062 2.362 5.83 5.83 0 0 0 .349 1.017 5.938 5.938 0 0 0 4.869 3.815c.291.033.585.048.877.045a5.838 5.838 0 0 0 4.093-1.748l3.418-3.418a1.31 1.31 0 0 0 0-1.854 1.31 1.31 0 0 0-1.854 0l-3.398 3.398a3.226 3.226 0 0 1-2.274.969 3.266 3.266 0 0 1-2.274-.969 3.226 3.226 0 0 1-.969-2.274 3.226 3.226 0 0 1 .969-2.274l3.854-4.126 5.406-5.788A1.374 1.374 0 0 0 13.483 0z"/>
                    <path fill="#94A3B8" d="M17.753 10.457a1.31 1.31 0 0 0-1.31 1.31v1.31a1.31 1.31 0 0 0 2.62 0v-1.31a1.31 1.31 0 0 0-1.31-1.31zM9.36 12.016a1.31 1.31 0 0 0-.927.384l-2.03 2.03a1.31 1.31 0 1 0 1.854 1.854l2.03-2.03a1.31 1.31 0 0 0-.927-2.238zm11.365 3.393h-5.24a1.31 1.31 0 0 0 0 2.62h5.24a1.31 1.31 0 0 0 0-2.62z"/>
                </svg>
                <span>LeetCode</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-label">Profile Controls</div>', unsafe_allow_html=True)
    if st.button("Display Perspective Note", key="btn_fun_fact", width="stretch"):
        facts = AUTOBIOGRAPHY_DATA["fun_facts"]
        new_idx = random.randint(0, len(facts) - 1)
        st.session_state.current_fun_fact_idx = new_idx
        st.toast("Perspective note updated.")

    fact_to_show = AUTOBIOGRAPHY_DATA["fun_facts"][st.session_state.current_fun_fact_idx]
    st.info(f"**Perspective Note:**\n\n{fact_to_show}")



    st.markdown("---")
    st.caption(f"Copyright {datetime.datetime.now().year} {PERSONAL_INFO['name']} • Section {PERSONAL_INFO['section']}")


# ==============================================================================
# 5. HEADER TERMINAL & TOP METRICS
# ==============================================================================

st.title("Autobiography and Portfolio")

# IDE Terminal Header Window
st.markdown(
    f"""
    <div class="terminal-window">
        <div class="terminal-topbar">
            <div class="terminal-controls">
                <span class="t-dot t-dot-red"></span>
                <span class="t-dot t-dot-yellow"></span>
                <span class="t-dot t-dot-green"></span>
                <span class="terminal-path">~/csit349-applied-ai/portfolio.py</span>
            </div>
            <div class="terminal-branch">git:main*</div>
        </div>
        <div class="terminal-content">
            <div class="terminal-hero-title">{PERSONAL_INFO['name']}</div>
            <div class="terminal-tagline">"{PERSONAL_INFO['tagline']}"</div>
            <div class="terminal-meta-grid">
                <div class="t-meta-item">Course: <strong>{PERSONAL_INFO['course']}</strong></div>
                <div class="t-meta-item">Section: <strong>{PERSONAL_INFO['section']}</strong></div>
                <div class="t-meta-item">Program: <strong>{PERSONAL_INFO['program_and_year']}</strong></div>
                <div class="t-meta-item">Institution: <strong>{PERSONAL_INFO['school']}</strong></div>
                <div class="t-meta-item">Location: <strong>{PERSONAL_INFO['location']}</strong></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Row of 4 Core Metrics
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(
        label="Projects Built",
        value=len(PROJECTS_DATA),
        help="Total software and applied AI projects documented in this portfolio."
    )
with m_col2:
    st.metric(
        label="Technical Skills",
        value=len(SKILLS_DATA),
        help="Cataloged competencies across programming, machine learning, and tooling."
    )
with m_col3:
    st.metric(
        label="Academic Standing",
        value="Year 3",
        delta="CSIT 349",
        help="Current degree progression."
    )
with m_col4:
    total_session_likes = sum(st.session_state.project_likes.values())
    st.metric(
        label="Project Endorsements",
        value=total_session_likes,
        delta=f"+{len(st.session_state.liked_projects)} session",
        help="Interactive endorsements recorded during this browser session."
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 6. MAIN NAVIGATION TABS (IDE BUFFER TABS)
# ==============================================================================

tab_about, tab_autobio, tab_skills, tab_projects, tab_contact = st.tabs([
    "About",
    "Autobiography",
    "Skills",
    "Projects",
    "Contact"
])


# ------------------------------------------------------------------------------
# TAB 1: ABOUT
# ------------------------------------------------------------------------------
with tab_about:
    st.header("About Me")
    col_photo, col_bio = st.columns([1, 2], gap="large")
    
    with col_photo:
        if os.path.exists(photo_file):
            st.image(photo_file, caption=PERSONAL_INFO["name"], width="stretch")
        else:
            st.warning("Stand-in photo file not found.")

    with col_bio:
        st.subheader(PERSONAL_INFO["name"])
        st.markdown(
            f"""
            - **Program & Year:** {PERSONAL_INFO['program_and_year']}
            - **Section:** {PERSONAL_INFO['section']}
            - **Institution:** {PERSONAL_INFO['school']}
            - **Course:** {PERSONAL_INFO['course']}
            - **Location:** {PERSONAL_INFO['location']}
            """
        )
        
        st.markdown("### Executive Summary")
        st.write(PERSONAL_INFO["short_bio"])
        
        st.markdown("### Core Objectives in Applied AI")
        st.write(PERSONAL_INFO["goals"])


# ------------------------------------------------------------------------------
# TAB 2: AUTOBIOGRAPHY
# ------------------------------------------------------------------------------
with tab_autobio:
    st.header("Autobiography")
    st.markdown("A structured overview of background, academic foundations, technical interests, and career milestones.")
    
    col_bg, col_edu = st.columns(2, gap="large")
    with col_bg:
        st.subheader("Background & Foundations")
        st.write(AUTOBIOGRAPHY_DATA["background"])
        
        st.subheader("Technical & Research Interests")
        st.write(AUTOBIOGRAPHY_DATA["interests"])

    with col_edu:
        st.subheader("Education & Curriculum")
        st.write(AUTOBIOGRAPHY_DATA["education"])
        
        st.subheader("Key Academic Milestones")
        st.write("Chronological journey through major learning thresholds and milestones:")
        milestones_df = pd.DataFrame(AUTOBIOGRAPHY_DATA["milestones"])
        st.table(milestones_df)


# ------------------------------------------------------------------------------
# TAB 3: SKILLS
# ------------------------------------------------------------------------------
with tab_skills:
    st.header("Technical Competencies")
    st.markdown(
        "A breakdown of technical proficiencies across programming languages, machine learning frameworks, "
        "and developer tooling. Use the controls below to filter by category or minimum proficiency score."
    )
    
    skills_df = pd.DataFrame(SKILLS_DATA)
    all_categories = sorted(list(skills_df["Category"].unique()))

    # Interactive Controls — multiselect gets its own full-width row to avoid clipping
    selected_categories = st.multiselect(
        "Filter by Category",
        options=all_categories,
        default=all_categories,
        key="skills_category_multiselect"
    )

    f_col2, f_col3 = st.columns([3, 1], gap="medium")
    with f_col2:
        min_level = st.slider(
            "Minimum Proficiency Level",
            min_value=0,
            max_value=100,
            value=60,
            step=5,
            key="skills_level_slider"
        )
        show_top_tier_only = st.checkbox(
            "Highlight core proficiencies only (Level >= 85%)",
            value=False,
            key="skills_top_tier_checkbox",
            help="Filters matrix and visualization to showcase high-confidence technical skills."
        )
    with f_col3:
        chart_type = st.radio(
            "Visualization Style",
            options=["Bar Chart", "Area Chart"],
            key="skills_chart_radio"
        )

    # Filter data
    filtered_skills = skills_df[
        (skills_df["Category"].isin(selected_categories)) &
        (skills_df["Level"] >= min_level)
    ]
    if show_top_tier_only:
        filtered_skills = filtered_skills[filtered_skills["Level"] >= 85]

    if filtered_skills.empty:
        st.info("No competencies match the selected filter criteria. Adjust the minimum proficiency score or select additional categories.")
    else:
        avg_level = float(filtered_skills["Level"].mean())
        st.markdown(f"**Average Proficiency Level of Filtered Skills:** `{avg_level:.1f}%`")
        st.progress(avg_level / 100.0)

        st.subheader("Competency Matrix")
        st.dataframe(
            filtered_skills[["Skill", "Category", "Level"]],
            column_config={
                "Level": st.column_config.ProgressColumn(
                    "Proficiency Level",
                    help="Self-assessed skill proficiency score (0-100)",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                ),
                "Skill": st.column_config.TextColumn("Skill", width="medium"),
                "Category": st.column_config.TextColumn("Domain", width="medium"),
            },
            hide_index=True,
            width="stretch"
        )

        # Skill description cards — always visible, no expander needed
        st.markdown(
            "<div style='font-family:\"JetBrains Mono\",monospace; font-size:0.72rem; font-weight:600; "
            "text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin:20px 0 10px 0;'>"
            "Skill Descriptions</div>",
            unsafe_allow_html=True
        )
        card_cols = st.columns(2, gap="medium")
        for i, (_, row) in enumerate(filtered_skills.iterrows()):
            with card_cols[i % 2]:
                st.markdown(
                    f"""
                    <div style="background:#0E131F; border:1px solid #1E2738; border-left:3px solid #818CF8;
                                border-radius:6px; padding:14px 16px; margin-bottom:10px;">
                        <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#818CF8;
                                    font-weight:600; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:4px;">
                            {row['Category']}
                        </div>
                        <div style="font-family:'Inter','Segoe UI',system-ui,sans-serif; font-size:0.95rem;
                                    font-weight:700; color:#F8FAFC; margin-bottom:6px;">
                            {row['Skill']}
                            <span style="font-size:0.75rem; font-weight:500; color:#38BDF8; margin-left:6px;">{row['Level']}%</span>
                        </div>
                        <div style="font-family:'Inter','Segoe UI',system-ui,sans-serif; font-size:0.85rem;
                                    color:#94A3B8; line-height:1.65;">
                            {row['Description']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.subheader("Proficiency Distribution")
        chart_data = filtered_skills.set_index("Skill")[["Level"]]
        if chart_type == "Bar Chart":
            st.bar_chart(chart_data, width="stretch")
        else:
            st.area_chart(chart_data, width="stretch")


# ------------------------------------------------------------------------------
# TAB 4: PROJECTS
# ------------------------------------------------------------------------------
with tab_projects:
    st.header("Featured Projects")
    st.markdown("A portfolio of software systems and applied AI projects, detailing architecture, role, toolsets, and verifiable outcomes.")

    all_tools = sorted(list({tool for p in PROJECTS_DATA for tool in p["tools"]}))
    
    selected_tools = st.multiselect(
        "Filter Projects by Technology",
        options=all_tools,
        default=all_tools,
        key="projects_tool_filter"
    )

    filtered_projects = [
        p for p in PROJECTS_DATA
        if any(tool in selected_tools for tool in p["tools"])
    ]

    if not filtered_projects:
        st.warning("No projects match the selected technology filters. Please select at least one matching tool.")
    else:
        cols = st.columns(2, gap="medium")
        for i, project in enumerate(filtered_projects):
            col = cols[i % 2]
            with col:
                with st.container(border=True):
                    # Project Card Header
                    st.subheader(project["title"])
                    st.caption(f"Role: **{project['role']}**")
                    
                    # Tool Pills
                    pills = "".join([f'<span class="tech-pill">{t}</span>' for t in project["tools"]])
                    st.markdown(f"{pills}", unsafe_allow_html=True)
                    
                    st.markdown("### Summary")
                    st.write(project["summary"])
                    
                    st.markdown("### Verifiable Outcome")
                    st.markdown(
                        f"""
                        <div style="background:#141B2B; border-left: 3px solid #34D399; padding: 10px 14px; border-radius: 4px; margin-bottom: 12px; font-size: 0.88rem; color: #E2E8F0;">
                            {project['outcome']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    c_btn, c_like = st.columns([1, 1])
                    with c_btn:
                        st.link_button("View Repository", project["link"], width="stretch")
                    with c_like:
                        proj_id = project["id"]
                        current_likes = st.session_state.project_likes[proj_id]
                        has_liked = proj_id in st.session_state.liked_projects
                        
                        btn_label = f"Endorsed ({current_likes})" if has_liked else f"Endorse ({current_likes})"
                        if st.button(btn_label, key=f"like_{proj_id}", width="stretch"):
                            if has_liked:
                                st.session_state.project_likes[proj_id] -= 1
                                st.session_state.liked_projects.remove(proj_id)
                                st.toast(f"Endorsement removed for {project['title']}.")
                            else:
                                st.session_state.project_likes[proj_id] += 1
                                st.session_state.liked_projects.add(proj_id)
                                st.toast(f"Endorsement recorded for {project['title']}.")
                            st.rerun()


# ------------------------------------------------------------------------------
# TAB 5: CONTACT & FEEDBACK
# ------------------------------------------------------------------------------
with tab_contact:
    st.header("Contact & Feedback")
    st.markdown("Submit inquiries, academic evaluation notes, or project collaboration requests. Submissions update the live statistics below.")

    with st.form("contact_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            form_name = st.text_input("Full Name *", placeholder="Jane Doe")
            form_email = st.text_input("Email Address", placeholder="jane@example.com")
        with col_f2:
            form_topic = st.selectbox(
                "Inquiry Topic",
                options=[
                    "Project Collaboration",
                    "Applied AI Discussion",
                    "Coursework Evaluation",
                    "Technical Feedback",
                    "General Inquiry"
                ]
            )
            form_rating = st.slider("Portfolio Assessment Score (1 = Needs Work, 5 = Outstanding)", 1, 5, 5)

        form_message = st.text_area("Message *", placeholder="Type your message or constructive feedback here...")
        submitted = st.form_submit_button("Submit Feedback", width="stretch")

        if submitted:
            if not form_name.strip():
                st.error("Please enter your name before submitting.")
            elif not form_message.strip():
                st.error("Please provide a message or comment before submitting.")
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_msg = {
                    "Name": form_name.strip(),
                    "Email": form_email.strip() if form_email.strip() else "Not provided",
                    "Topic": form_topic,
                    "Rating": form_rating,
                    "Message": form_message.strip(),
                    "Submitted At": timestamp
                }
                st.session_state.feedback_messages.append(new_msg)
                st.success(f"Thank you, {form_name}. Your message regarding '{form_topic}' was successfully received.")
                st.toast("Message received successfully.")
                
                if form_rating == 5:
                    st.balloons()

    st.markdown("---")
    
    st.subheader("Feedback & Submissions Summary")
    fb_col1, fb_col2 = st.columns(2)
    with fb_col1:
        st.metric(
            label="Total Received Submissions",
            value=len(st.session_state.feedback_messages),
            help="Total messages sent via this form during the active session."
        )
    with fb_col2:
        if st.session_state.feedback_messages:
            ratings = [m["Rating"] for m in st.session_state.feedback_messages]
            avg_rating = sum(ratings) / len(ratings)
            st.metric(
                label="Average Evaluation Score",
                value=f"{avg_rating:.2f} / 5.0",
                help="Mean rating given by respondents in this session."
            )
        else:
            st.metric(
                label="Average Evaluation Score",
                value="N/A",
                help="No submissions recorded yet."
            )

    with st.expander("Received Feedback & Submissions Log", expanded=False):
        if st.session_state.feedback_messages:
            msgs_df = pd.DataFrame(st.session_state.feedback_messages)
            st.dataframe(msgs_df, width="stretch", hide_index=True)
        else:
            st.write("No messages received in this session yet. Submissions will appear here once recorded.")

    st.markdown("---")
    
    st.subheader("Data Exports")
    st.markdown("Export portfolio content and skill matrices in standardized data formats.")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        portfolio_summary = {
            "Student": PERSONAL_INFO["name"],
            "Course": PERSONAL_INFO["course"],
            "Section": PERSONAL_INFO["section"],
            "Program": PERSONAL_INFO["program_and_year"],
            "Tagline": PERSONAL_INFO["tagline"],
            "Short_Bio": PERSONAL_INFO["short_bio"],
            "Total_Projects": len(PROJECTS_DATA),
            "Projects": PROJECTS_DATA,
            "Total_Skills": len(SKILLS_DATA),
            "Export_Date": datetime.datetime.now().isoformat()
        }
        json_data = json.dumps(portfolio_summary, indent=2)
        st.download_button(
            label="Download Portfolio Summary (JSON)",
            data=json_data,
            file_name="portfolio_summary.json",
            mime="application/json",
            width="stretch"
        )
    
    with d_col2:
        skills_csv = pd.DataFrame(SKILLS_DATA).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Skills Matrix (CSV)",
            data=skills_csv,
            file_name="skills_data.csv",
            mime="text/csv",
            width="stretch"
        )


# ==============================================================================
# 7. FOOTER SECTION
# ==============================================================================

st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #57606A; padding: 1.5rem 0 1rem 0; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace;">
        <p style="margin: 0;">
            Autobiography and Portfolio • Developed for <strong>{PERSONAL_INFO['course']}</strong>
        </p>
        <p style="margin: 0.35rem 0 0 0; color: #8B949E;">
            <strong>{PERSONAL_INFO['name']}</strong> | Section: <strong>{PERSONAL_INFO['section']}</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

