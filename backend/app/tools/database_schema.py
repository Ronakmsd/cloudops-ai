import os
from typing import Any

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cloudops:cloudops_dev_password@127.0.0.1:5432/cloudops",
)


def get_database_schema() -> dict[str, Any]:
    """
    Return the PostgreSQL schema available to the Data Agent.
    Read-only metadata inspection.
    """
    query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            return {
                "success": True,
                "tables": [
                    {
                        "table": row[0],
                        "column": row[1],
                        "data_type": row[2],
                    }
                    for row in rows
                ],
            }
