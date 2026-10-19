import pytest
from src.matcher import analyze, extract_skills
from src.parsers import extract_document
from fastapi.testclient import TestClient
from api.main import app

R = "Software engineer proficient in Python, FastAPI, SQL and Docker. Built REST API services."
J = "Seeking a software engineer with Python, FastAPI, SQL and Kubernetes expertise."

def test_skills():
    assert 'python' in extract_skills('Python and React')
    assert 'react' in extract_skills('Python and React')

def test_comparison():
    result = analyze(R, J)
    assert 'python' in result['matched_skills']
    assert 'kubernetes' in result['missing_skills']
    assert 0 <= result['text_similarity_percent'] <= 100

def test_identical():
    result = analyze(R, R)
    assert result['text_similarity_percent'] == 100

def test_empty():
    with pytest.raises(ValueError):
        analyze('short', J)

def test_txt_parser():
    assert extract_document('cv.txt', b'Hello!') == 'Hello!'

def test_reject_extension():
    with pytest.raises(ValueError):
        extract_document('cv.exe', b'Hello!')

def test_health():
    assert TestClient(app).get('/health').json() == {"status": "ok"}

def test_api():
    response = TestClient(app).post('/analyze', json={'resume': R, 'job_description': J})
    assert response.status_code == 200
    assert 'missing_skills' in response.json()
