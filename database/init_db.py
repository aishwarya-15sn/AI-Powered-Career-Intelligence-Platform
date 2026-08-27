import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "placify.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

connection = sqlite3.connect(DB_PATH)

try:
    connection.execute("PRAGMA foreign_keys = ON")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()

    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """).fetchall()

    print("Database created successfully.")
    print(f"Table count: {len(tables)}")
    print("\nTables:")

    for table in tables:
        print(f"- {table[0]}")

finally:
    connection.close()