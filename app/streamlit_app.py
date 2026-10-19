"""Run: streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from src.matcher import analyze
from src.parsers import extract_document

st.set_page_config(page_title="Resume Match Lab", page_icon="📄", layout="wide")
st.title("📄 Resume Match Lab")
st.caption("Privacy-friendly, explainable NLP comparison. Runs locally. Not a hiring decision tool.")
st.info("The scores below describe text similarity and recognized skill overlap—not ATS rankings or candidate quality.")
a, b = st.columns(2)
with a:
    st.subheader("Resume")
    resume_upload = st.file_uploader("Upload resume (TXT, PDF, DOCX)", type=['txt','pdf','docx'])
    resume_input = st.text_area("Or paste resume text", height=260, key='resume')
with b:
    st.subheader("Job description")
    job_upload = st.file_uploader("Upload job description (TXT, PDF, DOCX)", type=['txt','pdf','docx'])
    job_input = st.text_area("Or paste job description", height=260, key='job')

def get_text(upload, pasted):
    return extract_document(upload.name, upload.getvalue()) if upload else pasted

if st.button("Analyze match", type="primary"):
    try:
        report = analyze(get_text(resume_upload, resume_input), get_text(job_upload, job_input))
        c, d = st.columns(2)
        c.metric("TF-IDF text similarity", f"{report['text_similarity_percent']}%")
        d.metric("Recognized skill coverage", "N/A" if report['skill_coverage_percent'] is None else f"{report['skill_coverage_percent']}%")
        st.success("Matched skills: " + (", ".join(report['matched_skills']) or "None identified"))
        st.warning("Job skills not detected in resume: " + (", ".join(report['missing_skills']) or "None identified"))
        st.subheader("Suggestions")
        for item in report['suggestions']:
            st.write("• " + item)
        st.download_button("Download JSON report", data=__import__('json').dumps(report, indent=2), file_name="match_report.json", mime="application/json")
    except Exception as exc:
        st.error(f"Unable to analyze: {exc}")
