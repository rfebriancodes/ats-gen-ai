import os
import google.generativeai as genai

def generate_evaluation(job_desc, cv_text, skill_score, semantic_score, exp_score):

    api_key = 'AIzaSyC-VS4pqSohcH5JYhBhRfnY7l-RTsB64Bg'
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an AI recruitment analyst.

Job Description:
{job_desc}

Candidate CV:
{cv_text[:4000]}

Scores:
- Semantic Similarity: {semantic_score}
- Skill Match: {skill_score}
- Experience Score: {exp_score}

Provide:
1. Strengths of the candidate
2. Missing requirements
3. Overall recommendation (Strong Fit / Moderate Fit / Weak Fit)
4. Short professional summary
"""

    response = model.generate_content(prompt)

    return response.text