import re

def extract_required_skills(skills_input):
    if not skills_input:
        return []
    return [s.strip().lower() for s in skills_input.split(",")]


def match_skills(cv_text, required_skills):

    cv_text_lower = cv_text.lower()

    matched = []
    missing = []

    for skill in required_skills:
        if skill in cv_text_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    percentage = (len(matched) / len(required_skills)) * 100 if required_skills else 0

    return matched, missing, percentage


def highlight_skills(cv_text, skills):

    highlighted = cv_text

    for skill in skills:
        pattern = re.compile(skill, re.IGNORECASE)
        highlighted = pattern.sub(f"<mark>{skill}</mark>", highlighted)

    return highlighted