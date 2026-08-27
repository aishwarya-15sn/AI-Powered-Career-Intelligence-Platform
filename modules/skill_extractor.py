import sqlite3
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "placify.db"


def load_esco_skills():
    """
    Load ESCO skills together with alternative labels,
    descriptions and definitions from the Placify database.
    """

    connection = sqlite3.connect(DB_PATH)

    try:
        rows = connection.execute(
            """
            SELECT
                skill_id,
                skill_name,
                alternative_labels,
                description,
                definition
            FROM SKILL
            WHERE skill_name IS NOT NULL
            """
        ).fetchall()

        return rows

    finally:
        connection.close()


def normalize_text(text: str) -> str:
    """
    Normalize text for skill matching.
    """

    if not text:
        return ""

    text = text.lower()

    # Normalize common separators
    text = text.replace("/", " ")
    text = text.replace("_", " ")
    text = text.replace("-", " ")

    # Keep letters, numbers, # and +
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_alternative_labels(labels):
    """
    Convert ESCO alternative labels into a list.
    """

    if not labels:
        return []

    # ESCO alternative labels are commonly separated
    # by commas, semicolons or line breaks.
    parts = re.split(r"[,\n;|]", str(labels))

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def extract_skills(resume_text: str):
    """
    Extract standardized ESCO skills from resume text.

    The Review-1 baseline checks:
    - ESCO preferred skill names
    - ESCO alternative labels
    - relevant multi-word phrases

    Returns:
        List of dictionaries containing matched ESCO skills.
    """

    normalized_resume = normalize_text(resume_text)

    if not normalized_resume:
        return []

    esco_skills = load_esco_skills()

    matched_skills = []
    matched_ids = set()

    for row in esco_skills:

        skill_id = row[0]
        skill_name = row[1]
        alternative_labels = row[2]
        description = row[3]
        definition = row[4]

        candidates = [skill_name]

        candidates.extend(
            split_alternative_labels(alternative_labels)
        )

        found = False

        for candidate in candidates:

            normalized_candidate = normalize_text(candidate)

            if not normalized_candidate:
                continue

            # Avoid matching extremely short words.
            words = normalized_candidate.split()

            if len(normalized_candidate) < 3:
                continue

            # Exact phrase / word-boundary matching.
            pattern = r"(?<!\w)" + re.escape(
                normalized_candidate
            ) + r"(?!\w)"

            if re.search(pattern, normalized_resume):
                found = True
                break

        if found and skill_id not in matched_ids:

            matched_skills.append(
                {
                    "skill_id": skill_id,
                    "skill_name": skill_name,
                    "alternative_labels": alternative_labels,
                    "description": description,
                    "definition": definition,
                }
            )

            matched_ids.add(skill_id)

    return matched_skills