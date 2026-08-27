from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

COURSES_PATH = (
    BASE_DIR
    / "data"
    / "learning_resources"
    / "Online_Courses.csv"
)


def load_courses():

    if not COURSES_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(
        COURSES_PATH,
        encoding="utf-8-sig",
        low_memory=False
    )


def recommend_resources(missing_skills, limit=5):

    courses = load_courses()

    if courses.empty:
        return []

    skill_names = [
        skill["skill_name"]
        for skill in missing_skills
    ]

    recommendations = []

    text_columns = [
        column
        for column in courses.columns
        if courses[column].dtype == "object"
    ]

    for skill in skill_names:

        skill_lower = skill.lower()

        for _, row in courses.iterrows():

            searchable_text = " ".join(
                str(row[column])
                for column in text_columns
            ).lower()

            if skill_lower in searchable_text:

                recommendations.append(
                    {
                        "skill": skill,
                        "resource": row.to_dict()
                    }
                )

                break

        if len(recommendations) >= limit:
            break

    return recommendations