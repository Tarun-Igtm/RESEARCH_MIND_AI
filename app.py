import os
import streamlit as st

from utils.pdf_reader import extract_text, get_page_count
from utils.cleaner import clean_text
from utils.summarizer import summarize_text
from datetime import datetime
from utils.pdf_generator import create_pdf

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with st.sidebar:

    st.title("🧠 ResearchMind AI")

    st.markdown("---")

    st.write("### Features")

    st.write("✅ Research Paper Upload")
    st.write("✅ AI Summary")
    st.write("✅ Research Insights")
    st.write("✅ Viva Questions")
    st.write("✅ PDF Export")

    st.markdown("---")

    st.caption("Version 1.0")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "summary" not in st.session_state:
    st.session_state.summary = None

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "pdf_generated" not in st.session_state:
    st.session_state.pdf_generated = False

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

.block-container{

padding-top:2rem;
padding-bottom:2rem;
max-width:1200px;

}

/* Header */

.hero{

background:linear-gradient(135deg,#4F46E5,#7C3AED);

padding:35px;

border-radius:18px;

color:white;

margin-bottom:25px;

box-shadow:0px 8px 25px rgba(0,0,0,.20);

}

.hero h1{

margin:0;

font-size:42px;

font-weight:700;

}

.hero p{

margin-top:10px;

font-size:18px;

opacity:.95;

}

/* Card */

.card{

background:#1E1E2F;

padding:22px;

border-radius:16px;

border:1px solid #313244;

text-align:center;

box-shadow:0px 4px 12px rgba(0,0,0,.20);

}

.card h3{

margin:0;

font-size:18px;

color:#9CA3AF;

}

.card h2{

margin-top:12px;

font-size:26px;

color:white;

word-wrap:break-word;

}

/* Upload */

.upload-box{

padding:18px;

border-radius:16px;

border:1px solid #313244;

background:#1E1E2F;

margin-top:15px;

margin-bottom:25px;

}

/* Button */

.stButton>button{

width:100%;

height:58px;

font-size:20px;

font-weight:700;

border-radius:12px;

background:#4F46E5;

color:white;

border:none;

}

.stButton>button:hover{

background:#4338CA;

}

/* Divider */

hr{

margin-top:25px;

margin-bottom:25px;

}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DISPLAY AI REPORT
# --------------------------------------------------

def display_ai_report(report):

    sections = [
        "📑 Executive Summary",
        "🎯 Research Problem",
        "⚙️ Methodology",
        "🧠 Algorithms / Models Used",
        "📊 Results",
        "✅ Advantages",
        "❌ Limitations",
        "🚀 Future Scope",
        "❓ Viva Questions",
        "🧠 Research Insights",
    ]

    content = {}

    current = None

    for line in report.splitlines():

        line = line.strip()

        if line in sections:

            if line == "🧠 Research Insights":
                current = None
                continue

            current = line
            content[current] = []

        elif current:
            content[current].append(line)

    for section in sections:

        if section == "🧠 Research Insights":
            continue

        if section in content:

            with st.expander(
                section,
                expanded=(section == "📑 Executive Summary")
            ):

                st.markdown("\n".join(content[section]))

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""

<div class="hero">

<h1>🧠 ResearchMind AI</h1>

<p>
AI Powered Research Paper Analyzer using Google Gemini
</p>

</div>

""", unsafe_allow_html=True)

# --------------------------------------------------
# DEFAULT VALUES
# --------------------------------------------------

pdf_name = "No PDF Uploaded"
page_count = 0
word_count = 0
status = "Waiting"

cleaned_text = ""
uploaded_file_path = ""

file_size = "0 KB"
reading_time = "0 min"
character_count = 0
ai_model = "Gemini 2.5 Flash"

# --------------------------------------------------
# UPLOAD SECTION
# --------------------------------------------------

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📂 Upload your Research Paper",
    type=["pdf"]
)

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file is not None:

    os.makedirs("uploads", exist_ok=True)

    uploaded_file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:

        pdf_name = uploaded_file.name

        page_count = get_page_count(uploaded_file_path)

        raw_text = extract_text(uploaded_file_path)

        cleaned_text = clean_text(raw_text)

        word_count = len(cleaned_text.split())
        
        
        character_count = len(cleaned_text)

        file_size = f"{round(os.path.getsize(uploaded_file_path)/1024,2)} KB"

        reading_time = f"{max(1, round(word_count / 200))} min"
        
        file_size = round(
        os.path.getsize(uploaded_file_path) / 1024,
        2
        )

        reading_time = f"{max(1, word_count // 200)} min"

        upload_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        ai_model = "Gemini 2.5 Flash"

        status = "Ready ✅"

        st.session_state.uploaded = True

        st.success("✅ PDF Uploaded Successfully!")

    except Exception as e:

        st.error(f"❌ Error while reading PDF\n\n{e}")

        st.stop()

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="card">
        <h3>📄 PDF</h3>
        <h2>{pdf_name}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="card">
        <h3>📑 Pages</h3>
        <h2>{page_count}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="card">
        <h3>📖 Words</h3>
        <h2>{word_count:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:

    status_color = "#22C55E" if status == "Ready ✅" else "#F59E0B"

    st.markdown(f"""
    <div class="card">
        <h3>🤖 Status</h3>
        <h2 style="color:{status_color};">
            {status}
        </h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)

# -------------------------
# File Size
# -------------------------

with col5:

    st.markdown(f"""
    <div class="card">
        <h3>📦 File Size</h3>
        <h2>{file_size}</h2>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Reading Time
# -------------------------

with col6:

    st.markdown(f"""
    <div class="card">
        <h3>⏱ Reading Time</h3>
        <h2>{reading_time}</h2>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# AI Model
# -------------------------

with col7:

    st.markdown(f"""
    <div class="card">
        <h3>🤖 AI Model</h3>
        <h2>{ai_model}</h2>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Characters
# -------------------------

with col8:

    st.markdown(f"""
    <div class="card">
        <h3>📝 Characters</h3>
        <h2>{character_count:,}</h2>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.session_state.uploaded:

    if st.button("🚀 Analyze Research Paper"):

        with st.spinner("🤖 Gemini AI is analyzing your paper..."):

            try:

                summary = summarize_text(cleaned_text)
                
                if summary.startswith("❌"):

                    st.error(summary)

                    st.stop()

                st.session_state.summary = summary
                st.session_state.pdf_generated = False
                st.success("✅ Research paper analyzed successfully!")
                st.balloons()

            except Exception as e:

                st.error(f"❌ {e}")
                

# --------------------------------------------------
# EXTRACT RESEARCH INSIGHTS
# --------------------------------------------------

def extract_insights(report):

    insights = {
        "Domain": "-",
        "Research Type": "-",
        "Complexity": "-",
        "AI Confidence": "-"
    }

    for line in report.splitlines():

        line = line.strip()

        if line.startswith("Domain:"):
            insights["Domain"] = line.replace("Domain:", "").strip()

        elif line.startswith("Research Type:"):
            insights["Research Type"] = line.replace("Research Type:", "").strip()

        elif line.startswith("Complexity:"):
            insights["Complexity"] = line.replace("Complexity:", "").strip()

        elif line.startswith("AI Confidence:"):
            insights["AI Confidence"] = line.replace("AI Confidence:", "").strip()

    return insights                

# --------------------------------------------------
# SHOW RESULT
# --------------------------------------------------

if st.session_state.summary is not None:

    st.markdown("---")

    st.subheader("📑 AI Analysis Report")

    st.info(
        "The report below is generated using Google Gemini AI."
    )

    # -------------------------------
    # Research Insights
    # -------------------------------

    insights = extract_insights(st.session_state.summary)

    st.subheader("🧠 Research Insights")

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("📚 Domain", insights["Domain"]),
        ("🎯 Research Type", insights["Research Type"]),
        ("📊 Complexity", insights["Complexity"]),
        ("🤖 AI Confidence", insights["AI Confidence"]),
    ]

    for col, (title, value) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{title}</h4>
                    <p style="font-size:16px; font-weight:600;">
                        {value}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Full AI Report
    display_ai_report(st.session_state.summary)

    st.markdown("---")


# --------------------------------------------------
# DOWNLOAD PDF REPORT
# --------------------------------------------------

if st.session_state.summary:

    os.makedirs("output", exist_ok=True)

    pdf_path = os.path.join(
        "output",
        "ResearchMind_AI_Report.pdf"
    )

    try:

        if not st.session_state.pdf_generated:

            create_pdf(
                st.session_state.summary,
                pdf_path
            )
            

            st.session_state.pdf_generated = True

        with open(pdf_path, "rb") as pdf_file:

            pdf_bytes = pdf_file.read()

        st.markdown("---")
        st.subheader("📥 Export Report")

        st.caption(
            "Download the AI-generated research analysis as a PDF report."
        )

        st.download_button(

            label="📥 Download PDF Report",

            data=pdf_bytes,

            file_name="ResearchMind_AI_Report.pdf",

            mime="application/pdf"

        )

    except Exception as e:

        st.error(f"Error generating PDF: {e}")


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

st.markdown("---")

with st.expander("ℹ️ About ResearchMind AI"):

    st.markdown("""

### 🧠 ResearchMind AI

ResearchMind AI is an AI-powered research paper summarizer built using Python, Streamlit and Google Gemini.

### ✨ Features

- 📄 Upload Research Papers
- 🤖 AI Generated Summary
- 🎯 Research Problem
- ⚙️ Methodology
- 🧠 Algorithms Used
- 📊 Results
- ✅ Advantages
- ❌ Limitations
- 🚀 Future Scope
- ❓ Viva Questions

### 🛠 Tech Stack

- Python
- Streamlit
- Google Gemini API
- PyMuPDF
- Prompt Engineering

""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.caption(
    "© 2026 ResearchMind AI | Built with ❤️ using Streamlit & Google Gemini"
)


