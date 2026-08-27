import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "placify.db"


def get_job_roles():
    connection = sqlite3.connect(DB_PATH)

    try:
        return connection.execute(
            """
            SELECT job_role_id, role_name
            FROM JOB_ROLE
            ORDER BY role_name
            """
        ).fetchall()
    finally:
        connection.close()


def get_role_skills(job_role_id: int):
    connection = sqlite3.connect(DB_PATH)

    try:
        return connection.execute(
            """
            SELECT
                s.skill_id,
                s.skill_name,
                jrs.relation_type,
                jrs.skill_type
            FROM JOB_ROLE_SKILL AS jrs
            JOIN SKILL AS s
                ON s.skill_id = jrs.skill_id
            WHERE jrs.job_role_id = ?
            ORDER BY
                CASE
                    WHEN jrs.relation_type = 'essential' THEN 0
                    ELSE 1
                END,
                s.skill_name
            """,
            (job_role_id,)
        ).fetchall()
    finally:
        connection.close()