"""Explainable, local TF-IDF resume-to-job-description semantic matching.

This is a decision-support demo, not a hiring or rejection engine.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = (
    "python", "javascript", "typescript", "react", "next.js", "node.js", "fastapi",
    "django", "flask", "sql", "postgresql", "mongodb", "docker", "kubernetes",
    "aws", "azure", "git", "github actions", "machine learning", "nlp",
    "pandas", "scikit-learn", "tensorflow", "pytorch", "rest api", "graphql",
    "serviceNow", "n8n", "zapier", "databricks", "pyspark", "ci/cd", "testing",
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def extract_skills(text: str) -> list[str]:
    s = normalize(text)
    found = []
    for skill in SKILLS:
        key = skill.casefold()
        if re.search(r"(?<![\w])" + re.escape(key) + r"(?![\w])", s):
            found.append(skill)
    return sorted(found, key=str.casefold)


def analyze(resume: str, job: str) -> dict:
    if len(resume.strip()) < 15 or len(job.strip()) < 15:
        raise ValueError("Resume and job description must each contain at least 15 characters.")
    vect = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    matrix = vect.fit_transform([resume, job])
    similarity = float(cosine_similarity(matrix[0], matrix[1])[0, 0])
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job))
    matched = sorted(resume_skills & job_skills, key=str.casefold)
    missing = sorted(job_skills - resume_skills, key=str.casefold)
    suggestions = []
    if missing:
        suggestions.append("If you have experience with the missing skills, describe it accurately using concrete examples.")
    if similarity < .35:
        suggestions.append("Use specific, truthful project outcomes and relevant terminology from the job description.")
    suggestions.append("Review results manually; keyword similarity does not establish candidate suitability.")
    return {
        "text_similarity_percent": round(similarity * 100, 1),
        "skill_coverage_percent": round(100 * len(matched) / len(job_skills), 1) if job_skills else None,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills, key=str.casefold),
        "job_skills": sorted(job_skills, key=str.casefold),
        "suggestions": suggestions,
        "disclaimer": "Demo metrics only. Not an ATS score, hiring recommendation, or assessment of applicant ability."
    }
