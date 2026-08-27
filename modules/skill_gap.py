def calculate_skill_gap(resume_skills, required_skills):

    resume_skill_ids = {
        skill["skill_id"]
        for skill in resume_skills
    }

    matched = []
    missing = []

    for skill_id, skill_name, relation_type, skill_type in required_skills:

        skill_info = {
            "skill_id": skill_id,
            "skill_name": skill_name,
            "relation_type": relation_type,
            "skill_type": skill_type,
        }

        if skill_id in resume_skill_ids:
            matched.append(skill_info)
        else:
            missing.append(skill_info)

    total_required = len(required_skills)

    match_percentage = (
        len(matched) / total_required * 100
        if total_required
        else 0
    )

    return {
        "matched": matched,
        "missing": missing,
        "total_required": total_required,
        "match_percentage": round(match_percentage, 1),
    }