import re


def parse_required_skills(skills_input):

    if not skills_input:
        return []

    return [s.strip().lower() for s in skills_input.split(",")]


def evaluate_skills(cv_text, required_skills):

    cv_text_lower = cv_text.lower()
    results = []

    for skill in required_skills:

        pattern = r".{0,40}" + re.escape(skill) + r".{0,40}"
        match = re.search(pattern, cv_text_lower)

        if match:
            evidence = match.group()
            found = True
        else:
            evidence = "Not Found"
            found = False

        results.append({
            "skill": skill,
            "found": found,
            "evidence": evidence
        })

    match_count = sum(r["found"] for r in results)
    percentage = (match_count / len(required_skills)) * 100 if required_skills else 0

    return results, percentage


def highlight_skills(cv_text, required_skills):

    highlighted = cv_text

    for skill in required_skills:
        pattern = re.compile(skill, re.IGNORECASE)
        highlighted = pattern.sub(
            f"<mark>{skill}</mark>",
            highlighted
        )

    return highlighted