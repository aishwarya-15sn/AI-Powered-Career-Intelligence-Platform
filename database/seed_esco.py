import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "placify.db"
ESCO_DIR = BASE_DIR / "data" / "esco"


def main():
    print("Loading ESCO files...")

    skills = pd.read_csv(
        ESCO_DIR / "skills_en.csv",
        encoding="utf-8-sig",
        low_memory=False
    )

    occupations = pd.read_csv(
        ESCO_DIR / "occupations_en.csv",
        encoding="utf-8-sig",
        low_memory=False
    )

    relations = pd.read_csv(
        ESCO_DIR / "occupationSkillRelations_en.csv",
        encoding="utf-8-sig",
        low_memory=False
    )

    print(f"Skills loaded: {len(skills)}")
    print(f"Occupations loaded: {len(occupations)}")
    print(f"Relations loaded: {len(relations)}")

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        # --------------------------------------------------------
        # 1. SEED SKILL
        # --------------------------------------------------------

        print("\nSeeding SKILL...")

        skill_rows = []

        for _, row in skills.iterrows():
            skill_rows.append(
                (
                    row["conceptUri"],
                    row["preferredLabel"],
                    row["skillType"],
                    row["altLabels"] if pd.notna(row["altLabels"]) else None,
                    row["description"] if pd.notna(row["description"]) else None,
                    row["definition"] if pd.notna(row["definition"]) else None,
                    "ESCO"
                )
            )

        connection.executemany(
            """
            INSERT OR IGNORE INTO SKILL
            (
                esco_uri,
                skill_name,
                skill_type,
                alternative_labels,
                description,
                definition,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            skill_rows
        )

        connection.commit()

        print(
            "SKILL rows in database:",
            connection.execute(
                "SELECT COUNT(*) FROM SKILL"
            ).fetchone()[0]
        )

        # --------------------------------------------------------
        # 2. SEED JOB_ROLE
        # --------------------------------------------------------

        print("\nSeeding JOB_ROLE...")

        occupation_rows = []

        for _, row in occupations.iterrows():
            occupation_rows.append(
                (
                    row["conceptUri"],
                    row["preferredLabel"],
                    row["altLabels"] if pd.notna(row["altLabels"]) else None,
                    row["description"] if pd.notna(row["description"]) else None,
                    str(row["iscoGroup"]) if pd.notna(row["iscoGroup"]) else None,
                    row["code"] if pd.notna(row["code"]) else None,
                    "ESCO"
                )
            )

        connection.executemany(
            """
            INSERT OR IGNORE INTO JOB_ROLE
            (
                esco_uri,
                role_name,
                alternative_labels,
                description,
                isco_group,
                occupation_code,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            occupation_rows
        )

        connection.commit()

        print(
            "JOB_ROLE rows in database:",
            connection.execute(
                "SELECT COUNT(*) FROM JOB_ROLE"
            ).fetchone()[0]
        )

        # --------------------------------------------------------
        # 3. SEED JOB_ROLE_SKILL
        # --------------------------------------------------------

        print("\nSeeding JOB_ROLE_SKILL...")

        relation_rows = []

        for _, row in relations.iterrows():

            job_role_id = connection.execute(
                """
                SELECT job_role_id
                FROM JOB_ROLE
                WHERE esco_uri = ?
                """,
                (row["occupationUri"],)
            ).fetchone()

            skill_id = connection.execute(
                """
                SELECT skill_id
                FROM SKILL
                WHERE esco_uri = ?
                """,
                (row["skillUri"],)
            ).fetchone()

            if job_role_id is None or skill_id is None:
                raise RuntimeError(
                    "ESCO relationship references a missing "
                    "occupation or skill."
                )

            relation_rows.append(
                (
                    job_role_id[0],
                    skill_id[0],
                    row["relationType"],
                    row["skillType"]
                )
            )

        connection.executemany(
            """
            INSERT OR IGNORE INTO JOB_ROLE_SKILL
            (
                job_role_id,
                skill_id,
                relation_type,
                skill_type
            )
            VALUES (?, ?, ?, ?)
            """,
            relation_rows
        )

        connection.commit()

        print(
            "JOB_ROLE_SKILL rows in database:",
            connection.execute(
                "SELECT COUNT(*) FROM JOB_ROLE_SKILL"
            ).fetchone()[0]
        )

        # --------------------------------------------------------
        # 4. FINAL VERIFICATION
        # --------------------------------------------------------

        print("\n===== ESCO SEEDING COMPLETE =====")

        counts = {
            "SKILL": connection.execute(
                "SELECT COUNT(*) FROM SKILL"
            ).fetchone()[0],

            "JOB_ROLE": connection.execute(
                "SELECT COUNT(*) FROM JOB_ROLE"
            ).fetchone()[0],

            "JOB_ROLE_SKILL": connection.execute(
                "SELECT COUNT(*) FROM JOB_ROLE_SKILL"
            ).fetchone()[0],
        }

        for table, count in counts.items():
            print(f"{table}: {count}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()