from sklearn.metrics.pairwise import cosine_similarity

def rank_candidates(model, job_desc, cv_texts, cv_names):
    # Encode job description
    job_embedding = model.encode([job_desc])

    # Encode CVs
    cv_embeddings = model.encode(cv_texts)

    # Calculate cosine similarity
    similarities = cosine_similarity(job_embedding, cv_embeddings)[0]

    # Combine name + score
    results = list(zip(cv_names, similarities))

    # Sort descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results