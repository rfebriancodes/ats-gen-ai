def combine_scores(semantic_score, skill_percentage):

    skill_score = skill_percentage / 100

    final_score = (0.7 * semantic_score) + (0.3 * skill_score)

    return final_score