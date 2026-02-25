# 🧠 Sentinel-AI  
### AI-Powered Psychological Risk Assessment & Counseling Assistant
 Sentinel-AI is a production-ready AI system for early psychological risk identification using ethical anomaly detection and professional counseling-style reports.

![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Machine Learning](https://img.shields.io/badge/ML-Anomaly%20Detection-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Sentinel-AI** is an end-to-end AI-powered system designed to assist educators, counselors, and institutions in identifying students who may benefit from early psychological or behavioral support.  
> The system combines **machine learning, ethical AI, explainability, and professional reporting** into a real-world deployable application.

---

## 🌐 Live Demo
🔗 **Streamlit App:**   https://sentinel-ai-bfkq7juefqcjaeebanztic.streamlit.app/

---

## 📌 Key Features

| Feature | Description |
|-------|------------|
| 🧠 AI Risk Detection | Identifies behavioral anomalies using a trained ML model |
| 🧾 PDF Report Generation | Generates professional Unicode-safe counseling reports |
| 🎨 Modern UI | Gradient-based, accessible Streamlit interface |
| 📂 File Upload | CSV upload support for batch assessment |
| ⚖️ Ethical AI | Assistive, non-diagnostic decision support system |
| ☁️ Cloud Deployment | Fully deployed on Streamlit Cloud |

---

## 📊 Machine Learning Overview

| Component | Details |
|---------|--------|
| Model | Isolation Forest |
| Learning Type | Unsupervised Anomaly Detection |
| Domain | Psychological & Behavioral Risk Analysis |
| Input | Encoded behavioral indicators |
| Output | Risk score & risk category |
| Explainability | Feature contribution logic |

---

## 🛠️ Tech Stack

### Core Technologies

| Python 3.10+ | Streamlit | Scikit-learn | Pandas & NumPy | Joblib | FPDF (Unicode-enabled with DejaVu fonts) |
|:-------------|:----------|:-------------|:---------------|:-------|:-----------------------------------------:|

### Deployment
- Streamlit Cloud
- GitHub

---

## 🚀 Installation & Local Execution

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/sentinel-ai.git
cd sentinel-ai
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
streamlit run app.py
```

### 📂 CSV Upload Format
| Column Name    | Description                  |
| -------------- | ---------------------------- |
| stress_score   | Encoded stress indicator     |
| support_score  | Social support level         |
| coping_score   | Coping mechanism indicator   |
| pressure_score | Academic/work pressure level |

⚠️ Feature order must match the trained model input format.

> ### 📌Note 
> Sentinel-AI is not a medical or diagnostic tool.
> It is intended to support early awareness and decision-making and must not replace professional psychological evaluation.
