import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def extract_skills_from_jd(job_desc):

    text = job_desc.lower()

    # 1️⃣ Extract tech-like tokens (Go, AWS, Docker, etc.)
    tech_pattern = r'\b[a-zA-Z0-9+#.]+\b'
    tokens = re.findall(tech_pattern, text)

    # 2️⃣ Remove stopwords + short words
    filtered = [
        word for word in tokens
        if word not in ENGLISH_STOP_WORDS
        and len(word) > 2
    ]

    # 3️⃣ Detect common tech phrases (n-grams)
    bigrams = re.findall(r'\b[a-zA-Z]+\s+[a-zA-Z]+\b', text)

    # Keep meaningful bigrams like "google cloud", "problem solving"
    meaningful_bigrams = [
        phrase for phrase in bigrams
        if all(w not in ENGLISH_STOP_WORDS for w in phrase.split())
    ]

    # 4️⃣ Combine & deduplicate
    all_skills = set(filtered + meaningful_bigrams)

    # 5️⃣ Remove very generic words
    blacklist = {
        "years", "degree", "experience", "field",
        "professional", "strong", "ability",
        "understanding", "developing", "services"
    }

    cleaned = [
        skill for skill in all_skills
        if skill not in blacklist
    ]

    return ", ".join(sorted(list(cleaned)))