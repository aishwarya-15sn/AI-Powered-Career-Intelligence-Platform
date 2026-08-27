import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "placify.db"

connection = sqlite3.connect(DB_PATH)

try:
    print("===== SAMPLE JOB ROLE =====")

    role = connection.execute(
        """
        SELECT job_role_id, role_name
        FROM JOB_ROLE
        WHERE role_name = ?
        """,
        ("ICT application developer",)
    ).fetchone()

    print("ROLE:", role)

    if role is None:
        raise RuntimeError("ICT application developer was not found.")

    print("\n===== SKILLS =====")

    rows = connection.execute(
        """
        SELECT
            s.skill_name,
            jrs.relation_type,
            jrs.skill_type
        FROM JOB_ROLE_SKILL AS jrs
        JOIN SKILL AS s
            ON s.skill_id = jrs.skill_id
        WHERE jrs.job_role_id = ?
        ORDER BY jrs.relation_type, s.skill_name
        LIMIT 20
        """,
        (role[0],)
    ).fetchall()

    for row in rows:
        print(row)

    total = connection.execute(
        """
        SELECT COUNT(*)
        FROM JOB_ROLE_SKILL
        WHERE job_role_id = ?
        """,
        (role[0],)
    ).fetchone()[0]

    print("\nTOTAL SKILLS FOR ROLE:", total)

finally:
    connection.close()