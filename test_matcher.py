from src.matcher import analyze_resume, extract_skills

def test_skill_extraction():
    skills = extract_skills("I use Python, SQL and Pandas.")
    assert {"python", "sql", "pandas"}.issubset(skills)

def test_scores_are_bounded():
    result = analyze_resume("Python SQL Pandas", "Python and Pandas projects")
    for key in ("overall_score", "keyword_score", "skill_score", "tfidf_score"):
        assert 0 <= result[key] <= 100

def test_empty_resume_rejected():
    try:
        analyze_resume("Python developer", " ")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
