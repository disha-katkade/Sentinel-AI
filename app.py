import streamlit as st
import joblib
import pandas as pd
import numpy as np
from fpdf import FPDF

# -----------------------------
# Load trained model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("trained_model.pkl")

iso_forest = load_model()

# -----------------------------
# PDF setup
# -----------------------------
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Add DejaVu fonts (download and place in project folder)
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
pdf.add_font("DejaVu", "I", "DejaVuSans-Oblique.ttf", uni=True)
pdf.add_font("DejaVu", "BI", "DejaVuSans-BoldOblique.ttf", uni=True)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Sentinel-AI | Psychological Assessment",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background: linear-gradient(135deg, #f4f8fb 0%, #e9f0f7 100%); color: #1e293b;}
[data-testid="stMain"] {background: transparent;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #0f172a, #1e293b);}
[data-testid="stSidebar"] * {color: #f8fafc !important;}
h1 {color: #0f172a; font-weight: 800;}
h2, h3, h4 {color: #1e293b; font-weight: 700;}
p, label, span, div {color: #1e293b; font-size: 15px;}
label {font-weight: 600;}
.card {background-color: #ffffff; padding: 26px; border-radius: 18px; box-shadow: 0px 10px 28px rgba(0,0,0,0.1); margin-bottom: 24px;}
.stButton > button {background: linear-gradient(135deg, #2563eb, #1e40af); color:white; border-radius:12px; font-weight:700; padding:0.6rem 1.4rem; border:none;}
.stButton > button:hover {background: linear-gradient(135deg, #1d4ed8, #1e3a8a);}
.risk-low {background-color: #22c55e; color:white; padding:6px 16px; border-radius:999px; font-weight:700;}
.risk-medium {background-color: #f59e0b; color:white; padding:6px 16px; border-radius:999px; font-weight:700;}
.risk-high {background-color: #ef4444; color:white; padding:6px 16px; border-radius:999px; font-weight:700;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Sentinel-AI 🧠")
st.sidebar.markdown("### Student Well-being System")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🧍 Manual Assessment", "📂 Upload File", "📊 About System"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "🏠 Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Sentinel-AI")
    st.subheader("AI-powered Behavioral Risk & Counseling Assistant")
    st.write("""
    Sentinel-AI is an ethical, explainable AI system designed to assist
    educators and counselors in identifying students who may benefit from
    early academic or emotional support.
    """)
    st.markdown("### 🔍 What Sentinel-AI Does")
    st.markdown("""
    - 📈 Detects behavioral deviations using AI  
    - 🧠 Explains *why* a student is at risk  
    - 📝 Generates clinical-style counseling reports  
    - ⚖️ Designed with ethics and interpretability in mind  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Manual Assessment
# -----------------------------
if page == "🧍 Manual Assessment":
    st.markdown('<div class="card"><h2>🧠 Psychological Well-being Assessment</h2><p>This short assessment helps understand behavioral patterns.</p></div>', unsafe_allow_html=True)

    # Stress
    st.markdown('<div class="card">', unsafe_allow_html=True)
    stress_level = st.radio(
        "How often do you feel mentally overwhelmed or emotionally drained?",
        ["Rarely or never","Occasionally","Frequently","Almost all the time"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    stress_map = {"Rarely or never":0,"Occasionally":1,"Frequently":2,"Almost all the time":3}
    stress_score = stress_map[stress_level]

    # Social support
    st.markdown('<div class="card">', unsafe_allow_html=True)
    social_support = st.radio(
        "Do you feel supported by friends, family, or people you trust?",
        ["Yes, strongly","Somewhat","Rarely","Not at all"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    support_map = {"Yes, strongly":0,"Somewhat":1,"Rarely":2,"Not at all":3}
    support_score = support_map[social_support]

    # Coping
    st.markdown('<div class="card">', unsafe_allow_html=True)
    coping = st.radio(
        "When under stress, how do you usually cope?",
        ["Healthy activities (exercise, talking, hobbies)","Distraction (sleep, entertainment)","Avoidance or isolation","Substances or harmful habits"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    coping_map = {
        "Healthy activities (exercise, talking, hobbies)":0,
        "Distraction (sleep, entertainment)":1,
        "Avoidance or isolation":2,
        "Substances or harmful habits":3
    }
    coping_score = coping_map[coping]

    # Pressure
    st.markdown('<div class="card">', unsafe_allow_html=True)
    pressure = st.radio(
        "How manageable do your academic or work responsibilities feel?",
        ["Very manageable","Somewhat manageable","Often stressful","Overwhelming"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    pressure_map = {"Very manageable":0,"Somewhat manageable":1,"Often stressful":2,"Overwhelming":3}
    pressure_score = pressure_map[pressure]

    # Compute overall risk score (example)
    risk_total = stress_score + support_score + coping_score + pressure_score
    if risk_total >= 9:
        risk_level = "HIGH"
    elif risk_total >= 5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    explanation = f"Assessment completed: Stress={stress_level}, Support={social_support}, Coping={coping}, Pressure={pressure}."

    st.markdown(f"<div class='card'><p><b>Risk Level:</b> <span class='risk-{risk_level.lower()}'>{risk_level}</span></p><p>{explanation}</p></div>", unsafe_allow_html=True)

    # -----------------------------
    # Generate PDF Button
    # -----------------------------
    def generate_pdf(report_text, risk_level, filename="assessment_report.pdf"):
        pdf.add_page()
        # Title
        pdf.set_font("DejaVu", "B", 16)
        pdf.cell(0, 10, "CONFIDENTIAL STUDENT WELL-BEING ASSESSMENT REPORT", ln=True, align="C")
        pdf.ln(10)
        # Risk
        risk_colors = {"LOW": (34,197,94), "MEDIUM": (245,158,11), "HIGH": (239,68,68)}
        color = risk_colors.get(risk_level, (0,0,0))
        pdf.set_font("DejaVu", "B", 14)
        pdf.set_text_color(0,0,0)
        pdf.cell(50,10,"Overall Risk Level:", ln=0)
        pdf.set_text_color(*color)
        pdf.cell(40,10,risk_level, ln=True)
        pdf.ln(5)
        pdf.set_text_color(0,0,0)
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0,10,"Observed Behavioral Patterns:", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0,8, report_text)
        pdf.ln(5)
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0,10,"Recommendations:", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0,8,"- Follow suggested strategies based on risk level.\n- Monitor behavior and academic engagement regularly.\n- Seek support if needed.")
        pdf.output(filename)
        return filename

    if st.button("Generate PDF Report"):
        pdf_file = generate_pdf(explanation, risk_level)
        with open(pdf_file, "rb") as f:
            st.download_button("Download Assessment Report PDF", f, "student_assessment_report.pdf", "application/pdf")

# -----------------------------
# Upload File Section
# -----------------------------
if page == "📂 Upload File":
    st.markdown('<div class="card"><h3>Upload Student CSV Data</h3></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(data.head())

# -----------------------------
# About System Section
# -----------------------------
if page == "📊 About System":
    st.markdown('<div class="card"><h2>About Sentinel-AI</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <p><b>Sentinel-AI</b> is an ethical, explainable AI tool designed to detect behavioral deviations in students, 
    explain the contributing factors, and generate clinical-style counseling reports.</p>

    <p><b>Project Lead:</b> <span style="font-weight:700;">Disha Katkade</span></p>

    <p><b>Contact Information:</b></p>
    <p>
        <a href="mailto:dishakatkade.work@gmail.com" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="25px" title="Email">
        </a> &nbsp;&nbsp;
        <a href="https://github.com/disha-katkade/Sentinel-AI" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733609.png" width="25px" title="GitHub">
        </a> &nbsp;&nbsp;
        <a href="https://www.linkedin.com/in/disha-k-0a6781344/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25px" title="LinkedIn">
        </a>
    </p>

    <p><i>Disclaimer:</i> This system is intended to assist educators and counselors and does not replace professional psychological assessment.</p>
    """, unsafe_allow_html=True)
