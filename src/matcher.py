
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Standard skill names and their commonly used alternatives
SKILL_SYNONYMS = {
    "python": ["python", "python programming"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": [
        "natural language processing",
        "nlp",
        "text processing"
    ],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": [
        "data visualization",
        "data viz"
    ],
    "scikit-learn": [
        "scikit-learn",
        "sklearn",
        "scikit learn"
    ],
    "rest api": [
        "rest api",
        "restful api",
        "rest apis",
        "restful apis"
    ],
    "javascript": ["javascript", "js"],
    "c++": ["c++", "cpp"],
    "sql": ["sql", "structured query language"],
    "power bi": ["power bi", "powerbi"],
    "communication": [
        "communication",
        "verbal communication"
    ],
    "problem solving": [
        "problem solving",
        "problem-solving"
    ],
    "git": ["git", "version control"],
    "excel": ["excel", "microsoft excel"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"]
}


def normalize(text: str) -> str:
    """Normalize text for consistent comparison."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_term(text: str, term: str) -> bool:
    """Check for a complete term rather than a partial match."""
    pattern = (
        r"(?<![a-z0-9+#])"
        + re.escape(term.lower())
        + r"(?![a-z0-9+#])"
    )
    return bool(re.search(pattern, text))


def extract_skills(text: str) -> set:
    """Extract skills and map synonyms to standard skill names."""
    normalized = normalize(text)
    found = set()

    for standard_skill, aliases in SKILL_SYNONYMS.items():
        for alias in aliases:
            if contains_term(normalized, alias):
                found.add(standard_skill)
                break

    return found


def extract_experience(text: str):
    """
    Detect explicitly stated years of professional experience.
    Returns the largest detected number of years.
    """
    normalized = normalize(text)

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+experience",
        r"experience\s+of\s+(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s+of\s+experience"
    ]

    detected = []

    for pattern in patterns:
        matches = re.findall(pattern, normalized)
        detected.extend(float(value) for value in matches)

    return max(detected) if detected else None


def analyze_resume(job_description: str, resume_text: str,
                   weights=(40, 40, 20)):

    if not resume_text.strip():
        raise ValueError("No readable text was extracted.")

    jd = normalize(job_description)
    resume = normalize(resume_text)

    # 1. Keyword matching
    jd_words = set(re.findall(r"\b[a-z][a-z0-9+#.-]*\b", jd))
    resume_words = set(re.findall(r"\b[a-z][a-z0-9+#.-]*\b", resume))

    keyword_score = (
        100 * len(jd_words & resume_words) / max(len(jd_words), 1)
    )

    # 2. Skill matching with synonym recognition
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched = sorted(jd_skills & resume_skills)
    missing = sorted(jd_skills - resume_skills)

    skill_score = (
        100 * len(matched) / max(len(jd_skills), 1)
    )

    # 3. TF-IDF similarity
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform([jd, resume])

    tfidf_score = (
        100 * float(
            cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        )
    )

    # 4. Weighted overall score
    total_weight = sum(weights)

    if total_weight <= 0:
        raise ValueError("At least one scoring weight must be positive.")

    normalized_weights = [w / total_weight for w in weights]

    overall = (
        keyword_score * normalized_weights[0]
        + skill_score * normalized_weights[1]
        + tfidf_score * normalized_weights[2]
    )

    # 5. Experience extraction
    detected_experience = extract_experience(resume_text)

    return {
        "overall_score": round(overall, 2),
        "keyword_score": round(keyword_score, 2),
        "skill_score": round(skill_score, 2),
        "tfidf_score": round(tfidf_score, 2),
        "matched_skills": ", ".join(matched),
        "missing_skills": ", ".join(missing),
        "experience_years": detected_experience
    }
