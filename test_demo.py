from modules.skill_extractor import extract_skills
from modules.role_analyzer import get_job_roles, get_role_skills
from modules.skill_gap import calculate_skill_gap


print("===== JOB ROLES =====")

roles = get_job_roles()

print("Total roles:", len(roles))

for role in roles[:5]:
    print(role)


print("\n===== TEST ROLE =====")

selected_role = next(
    (
        role
        for role in roles
        if role[1].lower() == "ict application developer"
    ),
    None
)

print("Selected role:", selected_role)


if selected_role is None:
    raise RuntimeError(
        "ICT application developer not found."
    )


print("\n===== ROLE SKILLS =====")

required_skills = get_role_skills(
    selected_role[0]
)

print(
    "Required skills:",
    len(required_skills)
)

for skill in required_skills[:10]:
    print(skill)


print("\n===== TEST RESUME =====")

sample_resume = """
Software developer with experience in Python,
Java, SQL and Git.

Worked on software development projects and
database applications.
"""


resume_skills = extract_skills(
    sample_resume
)

print("Detected skills:")

for skill in resume_skills:
    print("-", skill["skill_name"])


print("\n===== SKILL GAP =====")

result = calculate_skill_gap(
    resume_skills,
    required_skills
)

print(
    "Match:",
    result["match_percentage"],
    "%"
)

print(
    "Matched:",
    len(result["matched"])
)

print(
    "Missing:",
    len(result["missing"])
)

print("\nTop missing skills:")

for skill in result["missing"][:10]:
    print("-", skill["skill_name"])