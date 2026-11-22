# Automated Resume Screening Tool

A student-built, ATS-style resume matching application using Python, Streamlit and NLP.
It accepts PDF, DOCX and TXT resumes, compares them with a job description, ranks documents
using transparent relevance signals, explains matched/missing skills, and exports CSV results.

> **Disclaimer:** This is an educational simulation, not a real ATS and not a validated hiring
> assessment. Scores measure textual similarity to a supplied job description. They do not
> measure a person's ability, potential, credibility, or job performance.

## Features
- Multiple PDF, DOCX and TXT resume uploads
- Text extraction using `pypdf` and `python-docx`
- Skill/keyword detection using a configurable vocabulary
- TF-IDF vectorization and cosine similarity
- Configurable weighted relevance score
- Candidate ranking and skill-gap explanation
- CSV export
- Synthetic sample resumes and automated tests

## Scoring model

The default weights are 40% keyword overlap, 40% detected skill overlap and 20% TF-IDF cosine
similarity. The UI lets the user change these weights; they are normalized to total 100%.

`Overall = w1 × Keyword + w2 × Skills + w3 × TF-IDF`

This is a project-defined heuristic, not an industry-standard ATS formula. A missing skill may
be expressed using a synonym or in a way the vocabulary does not recognize. Review source
documents and use human judgment.

## Project structure

```text
automated_resume_screening_tool/
├── app.py
├── src/
│   ├── __init__.py
│   ├── extractors.py
│   └── matcher.py
├── sample_data/
│   ├── job_description.txt
│   └── resumes/
├── tests/
│   └── test_matcher.py
├── requirements.txt
└── README.md
```

## Run locally

1. Install Python 3.10 or newer.
2. Clone this repository and open its directory.
3. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Launch:
   ```bash
   streamlit run app.py
   ```
6. Paste the sample job description from `sample_data/job_description.txt` and upload
   the three sample `.txt` resumes in `sample_data/resumes/`.

## Run tests

```bash
pytest -q
```

## Suggested demo workflow

1. Use the included Python Developer Intern job description.
2. Upload all three synthetic resumes.
3. Observe how the Python-focused resume ranks relative to the data analyst and Java resumes.
4. Open each candidate explanation to inspect matched and missing skills.
5. Download the CSV report.
6. Change the weights and run the same experiment again. Explain why rankings can change.

## Screenshots for GitHub

Capture your own screenshots after running the app:
- `docs/screenshots/home.png` – empty application and job-description input
- `docs/screenshots/results.png` – ranked candidates table
- `docs/screenshots/explanation.png` – candidate matched/missing skills
- `docs/screenshots/csv-export.png` – downloaded report (optional)

Add them to this README with Markdown image links once captured. Do not use fabricated screenshots.

## Limitations and responsible use

- Scoring is based on text, not verified qualifications or candidate performance.
- The skill vocabulary is deliberately small and should be expanded for each job family.
- Synonyms, abbreviations, spelling variants, tables, columns, scanned PDFs and image-only
  documents may not be handled correctly. OCR is not included in this version.
- Keyword matching can reward repetition or wording choices; TF-IDF is not semantic understanding.
- Do not use protected characteristics or proxies such as name, age, gender, religion, photo,
  address or graduation year to rank candidates.
- Do not make automated hiring decisions from this score. Keep a human reviewer in control.
- Use synthetic or consented data; avoid uploading sensitive personal data to public demos.

## Future improvements

- OCR for scanned PDFs
- Synonym dictionary and phrase-aware skill taxonomy
- Experience and education extraction with evidence snippets
- Semantic embeddings for contextual matching
- Database-backed candidate history and audit logs
- Role-specific evaluation and bias testing
- Unit tests for malformed and scanned documents
- Deployment with access controls and secure file handling

## Portfolio description

Built an ATS-style resume screening prototype in Python using Streamlit, PDF/DOCX parsing,
TF-IDF, cosine similarity and skill matching. Implemented explainable weighted scoring,
candidate ranking, skill-gap summaries, CSV export and synthetic test data.
