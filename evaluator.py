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

    # 1. Urutkan skill dari yang terpanjang ke terpendek.
    # Ini penting agar "C++" di-highlight duluan sebelum "C", 
    # atau "React Native" duluan sebelum "React".
    sorted_skills = sorted(required_skills, key=len, reverse=True)

    for skill in sorted_skills:
        # 2. re.escape(skill): Mengubah '+' atau '#' jadi teks biasa, bukan rumus regex.
        # 3. (?<!\w) dan (?!\w): Ini adalah "Smart Word Boundary". 
        # Memastikan dia tidak me-replace kata di TENGAH kata lain (misal mencari "go" di dalam "algoritma").
        pola_regex = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        pattern = re.compile(pola_regex, re.IGNORECASE)
        
        # 4. match.group(0): Mempertahankan huruf besar/kecil ASLI dari CV pelamar.
        # (Kalau CV nulis "JavaScript", hasilnya tetap "JavaScript", bukan "javascript").
        highlighted = pattern.sub(
            lambda match: f"<mark>{match.group(0)}</mark>", 
            highlighted
        )

    return highlighted