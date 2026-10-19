# 📄 Resume Match Lab — NLP Portfolio Project

Compare a resume and job description locally using TF-IDF and cosine similarity. Explore transparently detected skill overlap, missing job keywords, and truthful tailoring suggestions.

> **Important:** This is an educational NLP demonstration, **not** a trained hiring model, ATS score, job-fit assessment, or automated hiring decision system. Do not use it to screen, rank, reject or otherwise make employment decisions. Text similarity is not a reliable measure of competence. Skill detection uses a small fixed vocabulary and may miss synonyms or context.

## Features

- Streamlit app with paste or TXT/PDF/DOCX uploads (5MB limit)
- TF-IDF unigram/bigram vectors and cosine similarity
- Transparent skills dictionary with explicit matched/missing terms
- Export JSON report
- FastAPI `/analyze` and `/health` endpoints, interactive `/docs`
- Example documents, automated pytest tests and GitHub Actions CI
- Local processing; no external AI API keys or model downloads needed

## Quick start

Requires Python 3.10+ (3.11 recommended).

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Windows cmd: .venv\Scripts\activate.bat
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`. Paste the included `data/sample_resume.txt` and `data/sample_job.txt`, then click **Analyze match**.

## REST API

```bash
uvicorn api.main:app --reload
```

Browse `http://127.0.0.1:8000/docs` and try `POST /analyze`:

```json
{
  "resume": "I develop Python, SQL and FastAPI services, build REST API integrations and use Docker.",
  "job_description": "Seeking a Python developer with FastAPI, SQL, Docker, AWS and Kubernetes experience."
}
```

The response contains `text_similarity_percent`, `skill_coverage_percent`, `matched_skills`, `missing_skills`, and contextual suggestions. When no job terms from the skills dictionary are found, skill coverage is `null`.

## Tests

```bash
python -m pytest -q
```

## Structure

```text
ai_resume_matcher/
├── .github/workflows/tests.yml
├── api/main.py
├── app/streamlit_app.py
├── data/sample_resume.txt
├── data/sample_job.txt
├── src/matcher.py
├── src/parsers.py
├── tests/test_matcher.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## How it works

1. Parse TXT/PDF/DOCX or accept pasted text.
2. Convert both documents into TF-IDF feature vectors using 1–2 word n-grams and English stop word removal.
3. Calculate cosine similarity between the two vectors, presented as a percentage.
4. Search both texts for terms in a transparent technology-skills dictionary.
5. Report overlaps, JD skills absent from the resume text, and safe suggestions. Skill absence from text **does not mean** the applicant lacks the skill.

## Privacy and limitations

- The default application processes documents in memory locally; it does not intentionally save uploaded content.
- Avoid sending private resumes to public deployments you do not control.
- Scanned PDFs without a text layer are not OCR'd.
- There is no LLM, model training, historical hiring data, or calibrated statistical probability.
- The skill dictionary is deliberately limited, and exact matching can miss variants.
- No fairness, bias or real-world decision validation has been performed.

## GitHub repository details

**Suggested name:** `AI-Resume-Match-Lab`

**One-line description:** Privacy-friendly NLP app that compares resumes with job descriptions using TF-IDF, skill-gap analysis, Streamlit and FastAPI.

**Topics:** `python` `nlp` `scikit-learn` `streamlit` `fastapi` `resume-analysis` `machine-learning` `portfolio-project`

## License

MIT.
