import io
import pandas as pd
import streamlit as st
from src.extractors import extract_text
from src.matcher import analyze_resume

st.set_page_config(page_title="Resume Screening Tool", page_icon="📄", layout="wide")
st.title("📄 Automated Resume Screening Tool")
st.caption("A transparent, simulated ATS-style resume matching application built with Python and NLP.")

with st.sidebar:
    st.header("Screening settings")
    keyword_weight = st.slider("Keyword weight", 0, 100, 40)
    skill_weight = st.slider("Skill weight", 0, 100, 40)
    tfidf_weight = st.slider("TF-IDF weight", 0, 100, 20)
    st.caption("Weights are normalized automatically. This is a portfolio simulation, not a hiring decision system.")

st.markdown("""
Enter a job description and upload resumes. The tool extracts text, compares relevant skills and language,
and produces an explainable relevance ranking. Review the original resumes before making any decision.
""")

job_description = st.text_area(
    "Job description",
    placeholder="Example: We are looking for a Python developer with Python, SQL, Pandas, Git, REST API and problem-solving skills...",
    height=180,
)

uploads = st.file_uploader(
    "Upload resumes (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if st.button("Analyze resumes", type="primary", use_container_width=True):
    if not job_description.strip():
        st.error("Please enter a job description.")
    elif not uploads:
        st.error("Please upload at least one resume.")
    else:
        weights = [keyword_weight, skill_weight, tfidf_weight]
        if sum(weights) == 0:
            st.error("At least one scoring weight must be greater than zero.")
        else:
            rows = []
            details = {}
            progress = st.progress(0)
            for index, upload in enumerate(uploads):
                try:
                    content = upload.getvalue()
                    resume_text = extract_text(upload.name, content)
                    result = analyze_resume(job_description, resume_text, weights)
                    result["filename"] = upload.name
                    rows.append(result)
                    details[upload.name] = result
                except Exception as exc:
                    st.warning(f"Could not process {upload.name}: {exc}")
                progress.progress((index + 1) / len(uploads))

            if rows:
                results = pd.DataFrame(rows).sort_values("overall_score", ascending=False).reset_index(drop=True)
                results.insert(0, "rank", range(1, len(results) + 1))
                results["experience_display"] = results["experience_years"].apply(
                    lambda x: f"{x:g} years" if pd.notna(x) else "Not detected"
                    )
                st.subheader("Screening results")
                c1, c2, c3 = st.columns(3)
                c1.metric("Resumes processed", len(results))
                c2.metric("Highest relevance score", f"{results.overall_score.max():.1f}/100")
                c3.metric("Average relevance score", f"{results.overall_score.mean():.1f}/100")

                st.dataframe(
                    results[["rank", "filename", "overall_score", "keyword_score", "skill_score",
                             "tfidf_score", "matched_skills", "missing_skills"]],
                    use_container_width=True,
                    hide_index=True,
                )
                csv = results.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download screening report (CSV)", csv,
                                   file_name="resume_screening_results.csv", mime="text/csv")

                st.subheader("Candidate-level explanation")
                for _, row in results.iterrows():
                    with st.expander(f"#{row['rank']} · {row['filename']} · {row['overall_score']:.1f}/100"):
                        st.write(f"**Matched skills:** {row['matched_skills'] or 'None detected'}")
                        st.write(f"**Missing job-description skills:** {row['missing_skills'] or 'None detected'}")
                        st.write(f"**Keyword score:** {row['keyword_score']:.1f}")
                        st.write(f"**Skill score:** {row['skill_score']:.1f}")
                        st.write(f"**TF-IDF similarity:** {row['tfidf_score']:.1f}")
                st.info("Use these scores only as decision-support signals. They can miss synonyms, context, experience quality, and qualifications.")
            else:
                st.error("No resumes could be processed. Check that files contain readable text.")
