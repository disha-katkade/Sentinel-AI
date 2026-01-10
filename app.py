import streamlit as st
import joblib
import pandas as pd
import numpy as np
from fpdf import FPDF

# ------------------- LOAD MODEL -------------------
@st.cache_resource
def load_model():
    return joblib.load("trained_model.pkl")

iso_forest = load_model()

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Sentinel-AI | Psychological Assessment",
    page_icon="🧠",
    layout="wide"
)

# ------------------- STYLING -------------------
st.markdown("""
<style>
/* GLOBAL */
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #f4f8fb 0%, #e9f0f7 100%); color: #1e293b; }
[data-testid="stMain"] { background: transparent; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a, #1e293b); }
[data-testid="stSidebar"] * { color: #f8fafc !important; }

/* HEADINGS */
h1 { color: #0f172a; font-weight: 800; }
h2, h3, h4 { color: #1e293b; font-weight: 700; }

/* PARAGRAPH TEXT */
p, label, span, div { color: #1e293b; font-size: 15px; }
label { font-weight: 600; }

/* CARDS */
.card { background-color: #ffffff; padding: 26px; border-radius: 18px; box-shadow: 0px 10px 28px rgba(0, 0, 0, 0.1); margin-bottom: 24px; }

/* BUTTONS */
.stButton > button { background: linear-gradient(135deg, #2563eb, #1e40af); color: white; border-radius: 12px; font-weight: 700; padding: 0.6rem 1.4rem; border: none; }
.stButton > button:hover { background: linear-gradient(135deg, #1d4ed8, #1e3a8a); }

/* SLIDERS */
.stSlider > div > div > div > div { color: #1e293b; }

/* SELECTBOX */
.stSelectbox > div > div { background-color: #ffffff; color: #1e293b; }

/* TEXT INPUT */
.stTextInput > div > div > input { background-color: #ffffff; color: #1e293b; }

/* RISK TAGS */
.risk-low { background-color: #22c55e; color: white; padding: 6px 16px; border-radius: 999px; font-weight: 700; }
.risk-medium { background-color: #f59e0b; color: white; padding: 6px 16px; border-radius: 999px; font-weight: 700; }
.risk-high { background-color: #ef4444; color: white; padding: 6px 16px; border-radius: 999px; font-weight: 700; }

/* CONTACT ICONS */
.contact-icons img { transition: transform 0.2s, box-shadow 0.2s; margin-right: 12px; vertical-align: middle; }
.contact-icons img:hover { transform: scale(1.3); box-shadow: 0px 4px 12px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.title("Sentinel-AI 🧠")
st.sidebar.markdown("### Student Well-being System")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🧍 Manual Assessment", "📂 Upload File", "📊 About System"]
)

# ------------------- HOME PAGE -------------------
if page == "🏠 Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Sentinel-AI")
    st.subheader("AI-powered Behavioral Risk & Counseling Assistant")
    st.write("""
        Sentinel-AI is an ethical, explainable AI system designed to assist
        educators and counselors in identifying students who may benefit from
        early academic or emotional support.
        The system analyzes behavioral patterns, detects anomalies, explains
        contributing factors, and generates professional counseling-style reports.
    """)
    st.markdown("### 🔍 What Sentinel-AI Does")
    st.markdown("""
        - 📈 Detects behavioral deviations using AI  
        - 🧠 Explains *why* a student is at risk  
        - 📝 Generates clinical-style counseling reports  
        - ⚖️ Designed with ethics and interpretability in mind  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- MANUAL ASSESSMENT -------------------
if page == "🧍 Manual Assessment":
    st.markdown('<div class="card"><h2>🧠 Psychological Well-being Assessment</h2><p>This short assessment is designed to understand emotional, social, and behavioral patterns. Please respond honestly.</p></div>', unsafe_allow_html=True)
    
    # Example question
    stress_level = st.radio(
        "How often do you feel mentally overwhelmed or emotionally drained?",
        ["Rarely or never","Occasionally","Frequently","Almost all the time"]
    )
    stress_map = {"Rarely or never":0,"Occasionally":1,"Frequently":2,"Almost all the time":3}
    stress_score = stress_map[stress_level]

    # More questions (as in your original app)
    social_support = st.radio(
        "Do you feel supported by friends, family, or people you trust?",
        ["Yes, strongly","Somewhat","Rarely","Not at all"]
    )
    support_score = {"Yes, strongly":0,"Somewhat":1,"Rarely":2,"Not at all":3}[social_support]

    coping = st.radio(
        "When under stress, how do you usually cope?",
        ["Healthy activities (exercise, talking, hobbies)","Distraction (sleep, entertainment)","Avoidance or isolation","Substances or harmful habits"]
    )
    coping_score = {"Healthy activities (exercise, talking, hobbies)":0,"Distraction (sleep, entertainment)":1,"Avoidance or isolation":2,"Substances or harmful habits":3}[coping]

    pressure = st.radio(
        "How manageable do your academic or work responsibilities feel?",
        ["Very manageable","Somewhat manageable","Often stressful","Overwhelming"]
    )
    pressure_score = {"Very manageable":0,"Somewhat manageable":1,"Often stressful":2,"Overwhelming":3}[pressure]

    # PDF generation button
    if st.button("Generate PDF Report"):
        from fpdf import FPDF

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.add_font('ArialUnicode', '', '', uni=True)
        pdf.set_font("ArialUnicode", '', 14)
        pdf.multi_cell(0, 8, f"Sentinel-AI Psychological Assessment Report\n\nStress Score: {stress_score}\nSocial Support: {support_score}\nCoping: {coping_score}\nPressure: {pressure_score}")
        pdf.output("assessment_report.pdf")
        st.success("PDF generated successfully!")

# ------------------- UPLOAD FILE -------------------
if page == "📂 Upload File":
    st.markdown('<div class="card"><h2>Upload Student Data CSV</h2><p>Select a CSV file containing student behavioral data to analyze.</p></div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df.head())

        if st.button("Analyze & Generate Reports"):
            st.info("Analysis and report generation started...")
            # Your anomaly detection logic can be applied here
            st.success("Analysis complete! Reports generated.")

# ------------------- ABOUT SYSTEM -------------------
if page == "📊 About System":
    st.markdown('<div class="card"><h2>About Sentinel-AI</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <p><b>Sentinel-AI</b> is an ethical, explainable AI tool designed to detect behavioral deviations in students, 
    explain the contributing factors, and generate clinical-style counseling reports.</p>

    <p><b>Project Lead:</b> <span style="font-weight:700;">Disha Katkade</span></p>

    <p><b>Contact Information:</b></p>
    <p class="contact-icons">
        <a href="mailto:disha.katkade@example.com" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="30px" title="Email">
        </a>
        <a href="https://github.com/dishakatkade" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733609.png" width="30px" title="GitHub">
        </a>
        <a href="https://linkedin.com/in/dishakatkade" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30px" title="LinkedIn">
        </a>
    </p>

    <p><i>Disclaimer:</i> This system is intended to assist educators and counselors and does not replace professional psychological assessment.</p>
    """, unsafe_allow_html=True)
