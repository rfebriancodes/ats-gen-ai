import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from generator import generate_evaluation
from sklearn.metrics.pairwise import cosine_similarity

from model import get_model
from utils import extract_text_from_pdf, extract_contact_info
from skill_extractor import extract_skills_with_gemini
from evaluator import (
    parse_required_skills,
    evaluate_skills,
    highlight_skills
)
from scorer import combine_scores


st.set_page_config(page_title="Intelligent ATS", layout="wide")

st.title("🤖 Intelligent ATS: Contextual CV Evaluation using Hybrid AI")

# Load model
@st.cache_resource
def load_model():
    return get_model()

model = load_model()

# Sidebar
st.sidebar.header("📂 Upload CV (PDF)")
uploaded_files = st.sidebar.file_uploader(
    "Upload CV files",
    type=["pdf"],
    accept_multiple_files=True
)

st.sidebar.header("📝 Job Description")
job_desc = st.sidebar.text_area("Paste Job Description")

# Auto Extract Skills
if st.sidebar.button("Auto Extract Skills from JD"):
    if job_desc:
        extracted = extract_skills_with_gemini(job_desc)
        st.sidebar.write("Detected Skills:")
        st.sidebar.write(extracted)

st.sidebar.header("🛠 Required Skills (comma separated)")
skills_input = st.sidebar.text_input(
    "Example: go, aws, docker, agile"
)

# Evaluate Button
if st.sidebar.button("🚀 Evaluate Candidates"):

    if not uploaded_files or not job_desc:
        st.warning("Upload CV and provide Job Description first.")
        st.stop()

    required_skills = parse_required_skills(skills_input)

    job_embedding = model.encode([job_desc])

    results = []

    for file in uploaded_files:

        cv_text = extract_text_from_pdf(file)

        # Semantic similarity
        cv_embedding = model.encode([cv_text])
        semantic_score = cosine_similarity(
            job_embedding,
            cv_embedding
        )[0][0]

        # Skill evaluation
        skill_results, skill_percentage = evaluate_skills(
            cv_text,
            required_skills
        )

        # Hybrid score
        final_score = combine_scores(
            semantic_score,
            skill_percentage
        )

        results.append({
            "name": file.name,
            "semantic": semantic_score,
            "skill_percentage": skill_percentage,
            "final": final_score,
            "skill_results": skill_results,
            "cv_text": cv_text
        })

    # Sort by final score
    results = sorted(results, key=lambda x: x["final"], reverse=True)

    st.success("✅ Evaluation Completed")

    # Display Results
    for idx, candidate in enumerate(results, 1):
        st.subheader(f"{idx}. {candidate['name']}")

        st.write(f"Semantic Score: {round(candidate['semantic'],3)}")
        st.write(f"Skill Match: {round(candidate['skill_percentage'],1)}%")
        st.write(f"Final Score: {round(candidate['final'],3)}")

        # Skill table
        df_skill = pd.DataFrame(candidate["skill_results"])
        st.table(df_skill)

        # Radar Chart
        labels = ["Semantic", "Skill", "Final"]
        values = [
            candidate["semantic"],
            candidate["skill_percentage"] / 100,
            candidate["final"]
        ]

        contact_info = extract_contact_info(candidate['cv_text'])

        st.write(f"📧 Email: {contact_info['email']}")
        st.write(f"📱 Phone: {contact_info['phone']}")
        st.write(f"🔗 LinkedIn: {contact_info['linkedin']}")

        values += values[:1]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))

        fig, ax = plt.subplots(
            figsize=(2,2),
            subplot_kw=dict(polar=True)
        )

        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title(candidate["name"])

        st.pyplot(fig)

        # Highlight CV
        if required_skills:
            st.write("📄 Highlighted CV Preview")
            highlighted = highlight_skills(
                candidate["cv_text"],
                required_skills
            )
            st.markdown(
                highlighted[:2000],
                unsafe_allow_html=True
            )

        st.markdown("---")

        with st.spinner("Generating evaluation..."):

            explanation = generate_evaluation(
                job_desc,
                candidate["cv_text"][:4000],  # limit tokens
                candidate["skill_percentage"],
                candidate["semantic"],
                1  # or your exp_score if available
            )

        st.write(explanation)

    # Ranking overview chart
    df_final = pd.DataFrame(results)
    st.subheader("📊 Final Ranking Overview")
    st.bar_chart(df_final.set_index("name")["final"])


